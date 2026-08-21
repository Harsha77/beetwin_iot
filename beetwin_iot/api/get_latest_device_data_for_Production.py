


import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def get_filtered_device_data_for_production():
    """
    Fetch device telemetry data only for devices the user is allowed to access.
    """
    try:
        user = frappe.session.user  # Get the logged-in user

        # Check if the user is an administrator
        if "System Manager" in frappe.get_roles(user):
            return get_all_device_data_fro_production()  # Return all device data without filtering

        # Fetch the allowed device group for the user
        allowed_groups = frappe.get_all(
            "User Permission",
            filters={"user": user, "allow": "Device Group"},
            fields=["for_value"]
        )

        if not allowed_groups:
            return {"status": "error", "message": "No allowed device groups found."}

        allowed_group_values = [group["for_value"] for group in allowed_groups]

        # Fetch devices that belong to the allowed groups
        allowed_devices = frappe.get_all(
            "Device",
            filters={"device_group": ["in", allowed_group_values]},
            fields=["name"]
        )

        allowed_device_ids = {device["name"] for device in allowed_devices}

        # Get all device data
        device_data_response = get_all_device_data_fro_production()

        if device_data_response["status"] != "success":
            return device_data_response  # Return error if fetching failed

        # Filter devices based on allowed groups
        filtered_data = [
            device for device in device_data_response["data"]
            if device["Device ID"] in allowed_device_ids
        ]

        if not filtered_data:
            return {"status": "error", "message": "You are not allowed to view these devices."}

        return {"status": "success", "data": filtered_data}

    except Exception as e:
        frappe.log_error(message=str(e), title="Error filtering device telemetry data")
        return {"status": "error", "message": str(e)}


def filter_valid_telemetry_for_production(entries):
    """
    Ensure only telemetry keys that start with 't' are included.
    """
    telemetry_map = {}

    for record in entries:
        key = record["key"].lower()
        if key.startswith("t"):  # Include only keys that start with "t"
            telemetry_map[key] = record["value"]

    return telemetry_map



@frappe.whitelist(allow_guest=True)
def get_all_device_data_fro_production():
    """
    Fetch the latest valid telemetry data for all devices.
    """
    try:
        all_devices = frappe.get_all("Device Telemetry", fields=["name as device_id"])

        if not all_devices:
            return {"status": "error", "message": _("No devices found.")}

        all_telemetry_data = []

        for device in all_devices:
            device_id = device["device_id"]

            latest_entries = frappe.get_all(
                "Device Telemetry Key-Value",
                filters={"parent": device_id},
                order_by="timestamp DESC",
                fields=["timestamp", "key", "value"]
            )

            if not latest_entries:
                continue  # Skip if no telemetry data found for the device

            telemetry_data = {
                "Device ID": device_id,
                "Serial Number": None,
                "Timestamp": None,
                "Battery (%)": None,
                "Pressure (bar)": None,
                "Latitude": None,
                "Longitude": None,
                "RSSI Value": None
            }

            latest_timestamp = None

            filtered_values = filter_valid_telemetry_for_production(latest_entries)

            # Assign filtered values to telemetry_data dictionary
            telemetry_data["Serial Number"] = filtered_values.get("tsrno")
            telemetry_data["Latitude"] = filtered_values.get("tlat")
            telemetry_data["Longitude"] = filtered_values.get("tlong")
            telemetry_data["RSSI Value"] = filtered_values.get("trssi")
            telemetry_data["Pressure (bar)"] = filtered_values.get("tpv")
            telemetry_data["Battery (%)"] = filtered_values.get("tbt")

            for record in latest_entries:
                if record["timestamp"] and not str(record["timestamp"]).startswith("1970"):
                    if latest_timestamp is None or record["timestamp"] > latest_timestamp:
                        latest_timestamp = record["timestamp"]

            telemetry_data["Timestamp"] = latest_timestamp

            # ✅ Only append if at least one key has a non-null value
            if any([
                telemetry_data["Serial Number"],
                telemetry_data["Latitude"],
                telemetry_data["Longitude"],
                telemetry_data["RSSI Value"],
                telemetry_data["Pressure (bar)"],
                telemetry_data["Battery (%)"]
            ]):
                all_telemetry_data.append(telemetry_data)

        return {"status": "success", "data": all_telemetry_data}

    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching all device telemetry data")
        return {"status": "error", "message": str(e)}
