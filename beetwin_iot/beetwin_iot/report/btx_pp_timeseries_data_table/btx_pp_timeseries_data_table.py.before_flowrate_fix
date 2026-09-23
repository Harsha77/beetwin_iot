
import frappe
from datetime import datetime, timedelta

def execute(filters=None):
    columns = [
        {"label": "Timestamp", "fieldname": "timestamp", "fieldtype": "Datetime", "width": 200},  # X-axis
        {"label": "Pressure (bar)", "fieldname": "pv", "fieldtype": "Float", "width": 120},  # Y-axis
        {"label": "Battery (%)", "fieldname": "bt", "fieldtype": "Int", "width": 100},  # Y-axis
        {"label": "Sensor Health", "fieldname": "ht", "fieldtype": "Data", "width": 100},  # Y-axis (Modified to Data type)
        {"label": "Latitude", "fieldname": "lat", "fieldtype": "Data", "width": 150},  # Full precision
        {"label": "Longitude", "fieldname": "long", "fieldtype": "Data", "width": 150},   # Full precision
        {"label": "Signal Strength", "fieldname": "rssi", "fieldtype": "Data", "width": 150}   # Full precision
    ]

    if not filters or not filters.get("device_data"):
        return columns, []

    selected_device = filters.get("device_data")

    # Default last 7 days range (if no specific date filters are set)
    last_7_days = datetime.now() - timedelta(days=7)
    start_date = last_7_days.replace(hour=0, minute=0, second=0)
    end_date = datetime.now().replace(hour=23, minute=59, second=59)

    # Override default range if user selects from_date and to_date
    if filters.get("from_date") and filters.get("to_date"):
        start_date = datetime.strptime(filters["from_date"], "%Y-%m-%d").replace(hour=0, minute=0, second=0)
        end_date = datetime.strptime(filters["to_date"], "%Y-%m-%d").replace(hour=23, minute=59, second=59)

    # Fetch data based on selected IMEI or all devices
    if selected_device == "ALL":
        devices = frappe.db.sql("""
            SELECT DISTINCT imei_number FROM `tabDevice` 
            WHERE imei_number IS NOT NULL AND imei_number != ''
        """, as_dict=1)

        device_imeis = [device["imei_number"] for device in devices]

        if not device_imeis:
            return columns, []

        placeholders = ', '.join(['%s'] * len(device_imeis))

        readings = frappe.db.sql(f"""
            SELECT dr.timestamp, kv.key, CAST(kv.value AS CHAR) as value, dr.device_id
            FROM `tabDevice Reading` dr
            JOIN `tabDevice Reading Key-Value` kv ON kv.parent = dr.name
            WHERE dr.device_id IN ({placeholders}) 
            AND dr.timestamp BETWEEN %s AND %s
            ORDER BY dr.timestamp DESC
        """, tuple(device_imeis) + (start_date, end_date), as_dict=1)

    else:
        readings = frappe.db.sql("""
            SELECT dr.timestamp, kv.key, CAST(kv.value AS CHAR) as value
            FROM `tabDevice Reading` dr
            JOIN `tabDevice Reading Key-Value` kv ON kv.parent = dr.name
            WHERE dr.device_id = %s 
            AND dr.timestamp BETWEEN %s AND %s
            ORDER BY dr.timestamp DESC
        """, (selected_device, start_date, end_date), as_dict=1)

    # Organize data
    data_dict = {}
    for row in readings:
        timestamp = row["timestamp"]
        key = row["key"]
        value = row["value"]

        if timestamp not in data_dict:
            data_dict[timestamp] = {
                "timestamp": timestamp,
                "bt": None,
                "pv": None,
                "ht": None,
                "lat": None,
                "long": None,
                "rssi": None
            }

        field_map = {
            "pv": "pv",
            "bt": "bt",
            "ht": "ht",
            "lat": "lat",
            "long": "long",
            "rssi": "rssi"
        }

        if key in field_map:
            try:
                if key == "ht":
                    value = float(value)
                    value = "Healthy" if value == 1.000 else "Open" if value == 0.000 else value
                elif key == "pv":
                    value = float(value)
                elif key == "bt":
                    value = int(float(value))
                elif key in ["lat", "long"]:
                    value = str(value)
            except ValueError:
                value = None

            data_dict[timestamp][field_map[key]] = value

    data = sorted(data_dict.values(), key=lambda x: x["timestamp"], reverse=True)

    return columns, data



@frappe.whitelist(allow_guest=True)
def generate_device_report(device_data, from_date=None, to_date=None):
    frappe.logger().info(f"🔍 API Called - Device: {device_data}, From: {from_date}, To: {to_date}")

    if not device_data:
        return {"error": "Missing device_data parameter"}

    # Default last 7 days range if no specific date filters are provided
    last_7_days = datetime.now() - timedelta(days=7)
    start_date = last_7_days.replace(hour=0, minute=0, second=0).strftime('%Y-%m-%d %H:%M:%S')
    end_date = datetime.now().replace(hour=23, minute=59, second=59).strftime('%Y-%m-%d %H:%M:%S')

    # Override default range if user selects specific from_date and to_date
    if from_date and to_date:
        # start_date = datetime.strptime(from_date, '%Y-%m-%d').replace(hour=0, minute=0, second=0).strftime('%Y-%m-%d %H:%M:%S')
        start_date = from_date if from_date else (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        # end_date = (datetime.strptime(to_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S') if to_date else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(to_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59).strftime('%Y-%m-%d %H:%M:%S') if to_date else datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    device_readings = frappe.db.sql("""
        SELECT name, timestamp FROM `tabDevice Reading`
        WHERE device_id = %s AND timestamp BETWEEN %s AND %s
    """, (device_data, start_date, end_date), as_dict=True)

    frappe.logger().info(f"📌 Device Readings Count: {len(device_readings)}")

    if not device_readings:
        return {"message": "No readings found"}

    reading_names = [d["name"] for d in device_readings]
    if len(reading_names) == 1:
        reading_names_tuple = (reading_names[0],)
    else:
        reading_names_tuple = tuple(reading_names)

    key_values = frappe.db.sql("""
        SELECT parent, `key`, `value`
        FROM `tabDevice Reading Key-Value`
        WHERE parent IN %s
    """, (reading_names_tuple,), as_dict=True)

    frappe.logger().info(f"📌 Key-Value Count: {len(key_values)}")

    data_dict = {}
    for row in key_values:
        timestamp = frappe.db.get_value("Device Reading", row["parent"], "timestamp")
        key, value = row["key"], row["value"]

        if timestamp not in data_dict:
            data_dict[timestamp] = {
                "timestamp": timestamp, "bt": None, "pv": None, "ht": None,
                "lat": None, "long": None, "rssi": None
            }

        field_map = {"pv": "pv", "bt": "bt", "ht": "ht", "lat": "lat", "long": "long", "rssi": "rssi"}

        if key in field_map:
            try:
                if key == "ht":
                    value = "Healthy" if float(value) == 1.000 else "Open" if float(value) == 0.000 else value
                elif key == "pv":
                    value = float(value)
                elif key == "bt":
                    value = int(float(value))
                elif key in ["lat", "long"]:
                    value = float(value) if value else None
            except ValueError:
                value = None

            data_dict[timestamp][field_map[key]] = value

    sorted_data = sorted(data_dict.values(), key=lambda x: x["timestamp"], reverse=True)

    frappe.logger().info(f"✅ Final Data Sent: {len(sorted_data)} rows")
    return {"data": sorted_data}




@frappe.whitelist(allow_guest=True)
def generate_device_report_for_graph(device_data, from_date=None, to_date=None):
    frappe.logger().info(f"🔍 API Called - Device: {device_data}, From: {from_date}, To: {to_date}")

    if not device_data:
        return {"error": "Missing device_data parameter"}

    # Default last 7 days range if no specific date filters are provided
    last_7_days = datetime.now() - timedelta(days=7)
    start_date = last_7_days.replace(hour=0, minute=0, second=0).strftime('%Y-%m-%d %H:%M:%S')
    end_date = datetime.now().replace(hour=23, minute=59, second=59).strftime('%Y-%m-%d %H:%M:%S')
   #end_date = (datetime.strptime(to_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S') if to_date else datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Override default range if user selects specific from_date and to_date
    if from_date and to_date:
        start_date = from_date if from_date else (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        end_date = (datetime.strptime(to_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S') if to_date else datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    device_readings = frappe.db.sql("""
        SELECT name, timestamp FROM `tabDevice Reading`
        WHERE device_id = %s AND timestamp BETWEEN %s AND %s
    """, (device_data, start_date, end_date), as_dict=True)

    frappe.logger().info(f"📌 Device Readings Count: {len(device_readings)}")

    if not device_readings:
        return {"message": "No readings found"}

    reading_names = [d["name"] for d in device_readings]
    if len(reading_names) == 1:
        reading_names_tuple = (reading_names[0],)
    else:
        reading_names_tuple = tuple(reading_names)

    key_values = frappe.db.sql("""
        SELECT parent, `key`, `value`
        FROM `tabDevice Reading Key-Value`
        WHERE parent IN %s
    """, (reading_names_tuple,), as_dict=True)

    frappe.logger().info(f"📌 Key-Value Count: {len(key_values)}")

    data_dict = {}
    for row in key_values:
        timestamp = frappe.db.get_value("Device Reading", row["parent"], "timestamp")
        key, value = row["key"], row["value"]

        if timestamp not in data_dict:
            data_dict[timestamp] = {
                "bt": None, "pv": None, "ht": None,
                "lat": None, "long": None, "rssi": None,
                "timestamp": timestamp  # Move timestamp to the end
            }

        field_map = {"pv": "pv", "bt": "bt", "ht": "ht", "lat": "lat", "long": "long", "rssi": "rssi"}

        if key in field_map:
            try:
                if key == "ht":
                    value = "Healthy" if float(value) == 1.000 else "Open" if float(value) == 0.000 else value
                elif key == "pv":
                    value = float(value)
                elif key == "bt":
                    value = int(float(value))
                elif key in ["lat", "long"]:
                    value = float(value) if value else None
            except ValueError:
                value = None

            data_dict[timestamp][field_map[key]] = value

    sorted_data = sorted(data_dict.values(), key=lambda x: x["timestamp"], reverse=True)

    # Filter out entries where pv, bt, and ht are all None
    sorted_data = [entry for entry in sorted_data if not (entry["pv"] is None and entry["bt"] is None and entry["ht"] is None)]

    frappe.logger().info(f"✅ Final Data Sent: {len(sorted_data)} rows")
    return {"data": sorted_data}
