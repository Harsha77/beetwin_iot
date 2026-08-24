# ============================================================
# BTX-PP Timeseries Data Table
# ============================================================

import frappe

from datetime import datetime, timedelta, time
from frappe.utils import getdate, now_datetime


# ------------------------------------------------------------
# Supported telemetry keys
# ------------------------------------------------------------

KEY_FIELD_MAP = {
    # New MQTT keys
    "flowrate": "flowrate",
    "flow_rate": "flowrate",

    "total": "totaliser",
    "totaliser": "totaliser",
    "totalizer": "totaliser",

    # Old keys retained for backward compatibility
    "pv": "flowrate",
    "bt": "totaliser",

    # Other telemetry
    "ht": "ht",
    "lat": "lat",
    "latitude": "lat",
    "long": "long",
    "longitude": "long",
    "rssi": "rssi",
}


# ------------------------------------------------------------
# Report columns
# ------------------------------------------------------------

def get_columns():
    return [
        {
            "label": "Timestamp",
            "fieldname": "timestamp",
            "fieldtype": "Datetime",
            "width": 200,
        },
        {
            "label": "Flowrate",
            "fieldname": "flowrate",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": "Totaliser",
            "fieldname": "totaliser",
            "fieldtype": "Float",
            "width": 150,
        },
    ]


# ------------------------------------------------------------
# Date-range helper
# ------------------------------------------------------------

def get_date_range(from_date=None, to_date=None):
    """
    Return a complete datetime range.

    If dates are not provided, return data from the last seven days.
    """

    current_datetime = now_datetime()

    if from_date and to_date:
        start_date = datetime.combine(
            getdate(from_date),
            time.min,
        )

        end_date = datetime.combine(
            getdate(to_date),
            time.max,
        )
    else:
        start_date = (
            current_datetime - timedelta(days=7)
        ).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        end_date = current_datetime.replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=999999,
        )

    return start_date, end_date


# ------------------------------------------------------------
# Value conversion
# ------------------------------------------------------------

def convert_value(fieldname, value):
    """
    Convert database string values into appropriate API values.
    """

    if value is None:
        return None

    value_string = str(value).strip()

    if value_string == "" or value_string.lower() in {
        "null",
        "none",
        "nan",
    }:
        return None

    try:
        if fieldname in {
            "flowrate",
            "totaliser",
            "lat",
            "long",
            "rssi",
        }:
            return float(value_string)

        if fieldname == "ht":
            numeric_value = float(value_string)

            if numeric_value == 1:
                return "Healthy"

            if numeric_value == 0:
                return "Open"

            return value_string

        return value_string

    except (ValueError, TypeError):
        return None


# ------------------------------------------------------------
# Initialize response row
# ------------------------------------------------------------

def create_empty_row(timestamp, device_id=None):
    """
    Create a telemetry row with all supported fields.
    """

    return {
        "device_id": device_id,
        "timestamp": timestamp,

        # New field names
        "flowrate": None,
        "totaliser": None,

        # Old aliases for backward compatibility
        "pv": None,
        "bt": None,

        # Additional telemetry
        "ht": None,
        "lat": None,
        "long": None,
        "rssi": None,
    }


# ------------------------------------------------------------
# Fetch and organize telemetry
# ------------------------------------------------------------

def fetch_telemetry_data(
    device_data,
    start_date,
    end_date,
):
    """
    Fetch Device Reading and Key-Value data using one joined query.
    """

    conditions = [
        "dr.timestamp BETWEEN %(start_date)s AND %(end_date)s"
    ]

    query_values = {
        "start_date": start_date,
        "end_date": end_date,
    }

    if device_data and device_data != "ALL":
        conditions.append(
            "dr.device_id = %(device_data)s"
        )

        query_values["device_data"] = device_data

    where_clause = " AND ".join(conditions)

    readings = frappe.db.sql(
        f"""
        SELECT
            dr.name AS reading_name,
            dr.device_id,
            dr.timestamp,
            kv.`key` AS telemetry_key,
            CAST(kv.`value` AS CHAR) AS telemetry_value
        FROM `tabDevice Reading` dr
        LEFT JOIN `tabDevice Reading Key-Value` kv
            ON kv.parent = dr.name
        WHERE {where_clause}
        ORDER BY
            dr.timestamp DESC,
            kv.idx ASC
        """,
        query_values,
        as_dict=True,
    )

    data_dict = {}

    for reading in readings:
        timestamp = reading.get("timestamp")
        device_id = reading.get("device_id")

        if not timestamp:
            continue

        # Device ID is included because two devices can
        # have readings with the same timestamp.
        row_identifier = (
            device_id,
            timestamp,
        )

        if row_identifier not in data_dict:
            data_dict[row_identifier] = create_empty_row(
                timestamp=timestamp,
                device_id=device_id,
            )

        raw_key = reading.get("telemetry_key")

        if not raw_key:
            continue

        normalized_key = str(raw_key).strip().lower()

        fieldname = KEY_FIELD_MAP.get(
            normalized_key
        )

        if not fieldname:
            continue

        converted_value = convert_value(
            fieldname,
            reading.get("telemetry_value"),
        )

        data_dict[row_identifier][fieldname] = (
            converted_value
        )

        # Keep old aliases populated so old Vue code
        # continues working during the transition.
        if fieldname == "flowrate":
            data_dict[row_identifier]["pv"] = (
                converted_value
            )

        elif fieldname == "totaliser":
            data_dict[row_identifier]["bt"] = (
                converted_value
            )

    return sorted(
        data_dict.values(),
        key=lambda row: row["timestamp"],
        reverse=True,
    )


# ------------------------------------------------------------
# Frappe report execute
# ------------------------------------------------------------

def execute(filters=None):
    columns = get_columns()

    if not filters:
        return columns, []

    device_data = filters.get("device_data")

    if not device_data:
        return columns, []

    start_date, end_date = get_date_range(
        filters.get("from_date"),
        filters.get("to_date"),
    )

    data = fetch_telemetry_data(
        device_data=device_data,
        start_date=start_date,
        end_date=end_date,
    )

    return columns, data


# ------------------------------------------------------------
# API: Tabular device report
# ------------------------------------------------------------

@frappe.whitelist(allow_guest=True)
def generate_device_report(
    device_data,
    from_date=None,
    to_date=None,
):
    """
    Return telemetry data for the selected device.
    """

    if not device_data:
        return {
            "data": [],
            "error": "Missing device_data parameter",
        }

    start_date, end_date = get_date_range(
        from_date,
        to_date,
    )

    frappe.logger().info(
        "Device report requested: "
        f"device={device_data}, "
        f"start={start_date}, "
        f"end={end_date}"
    )

    data = fetch_telemetry_data(
        device_data=device_data,
        start_date=start_date,
        end_date=end_date,
    )

    frappe.logger().info(
        f"Device report generated: {len(data)} rows"
    )

    return {
        "data": data,
    }


# ------------------------------------------------------------
# API: Graph device report
# ------------------------------------------------------------

@frappe.whitelist(allow_guest=True)
def generate_device_report_for_graph(
    device_data,
    from_date=None,
    to_date=None,
):
    """
    Return only rows containing useful telemetry.
    """

    if not device_data:
        return {
            "data": [],
            "error": "Missing device_data parameter",
        }

    start_date, end_date = get_date_range(
        from_date,
        to_date,
    )

    data = fetch_telemetry_data(
        device_data=device_data,
        start_date=start_date,
        end_date=end_date,
    )

    filtered_data = [
        row
        for row in data
        if any(
            row.get(fieldname) is not None
            for fieldname in [
                "flowrate",
                "totaliser",
                "ht",
                "lat",
                "long",
                "rssi",
            ]
        )
    ]

    frappe.logger().info(
        "Device graph report generated: "
        f"{len(filtered_data)} rows"
    )

    return {
        "data": filtered_data,
    }