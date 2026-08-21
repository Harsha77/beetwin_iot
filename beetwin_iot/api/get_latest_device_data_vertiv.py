
import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def get_filtered_device_data():
    """
    Fetch device telemetry data only for devices the user is allowed to access.
    """
    try:
        user = frappe.session.user  # Get the logged-in user

        # Check if the user is an administrator
        if "System Manager" in frappe.get_roles(user):
            return get_all_device_data()  # Return all device data without filtering

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
        device_data_response = get_all_device_data()

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


def filter_valid_telemetry(entries):
    """
    Ensure only valid telemetry keys are included, completely ignoring keys that start with 't'.
    """
    valid_keys = {"srno", "INPV", "INPI", "INF", "OPV", "OPI", "OPL", "OPVA", "OPW", "OPF", "BTV", "BTC", "BT", "ALINPVHI", "ALINPVLOW"}
    telemetry_map = {}

    for record in entries:
        key = record["key"]
        
        # Ignore any key that starts with 't'
        if key.startswith("t"):
            continue  # Completely skip this key

        if key in valid_keys:  # Only add explicitly allowed keys
            telemetry_map[key] = record["value"]

    return telemetry_map



from datetime import datetime

@frappe.whitelist(allow_guest=True)
def get_all_device_data():
    """
    Fetch the latest valid telemetry data for all devices.
    """
    try:
        # Fetch all telemetry records from the parent 'Device Telemetry' Doctype
        all_devices = frappe.get_all("Device Telemetry", fields=["name as device_id"])

        if not all_devices:
            return {"status": "error", "message": _("No devices found.")}

        # List to hold telemetry data for all devices
        all_telemetry_data = []

        current_year = datetime.now().year  # Get the current year

        for device in all_devices:
            device_id = device["device_id"]

            # Fetch telemetry key-value pairs ordered by timestamp (latest first)
            latest_entries = frappe.get_all(
                "Device Telemetry Key-Value",
                filters={"parent": device_id},
                order_by="timestamp DESC",
                fields=["timestamp", "key", "value"]
            )

            if not latest_entries:
                continue  # Skip if no telemetry data found for the device

            # Initialize telemetry data
            telemetry_data = {
                "Device ID": device_id,
                "Serial Number": None,
                "Timestamp": None,
                "Input Voltage": None,
                "Input Current": None,
                "Input Freq": None,
                "Output Voltage": None,
                "Output Current": None,
                "Output Load": None,  
                "Output VA": None, 
                "Watts": None, 
                "Output Freq": None, 
                "Battry Volatge": None, 
                "Battery Charge": None, 
                "Time Remaining": None, 
                "Input Volatge High": None, 
                "Input Volatge Low": None,   
            }

            latest_timestamp = None
            valid_timestamp = None

            # Apply the filtering function
            filtered_values = filter_valid_telemetry(latest_entries)

            # Assign filtered values to the telemetry_data dictionary
            telemetry_data["Serial Number"] = filtered_values.get("srno")
            telemetry_data["Input Voltage"] = filtered_values.get("INPV")
            telemetry_data["Input Current"] = filtered_values.get("INPI")
            telemetry_data["Input Freq"] = filtered_values.get("INF")
            telemetry_data["Output Voltage"] = filtered_values.get("OPV")
            telemetry_data["Output Current"] = filtered_values.get("OPI")
            telemetry_data["Output Load"] = filtered_values.get("OPL")
            
            telemetry_data["Output VA"] = filtered_values.get("OPVA")
            telemetry_data["Watts"] = filtered_values.get("OPW")
            telemetry_data["Output Freq"] = filtered_values.get("OPF")
            telemetry_data["Battry Volatge"] = filtered_values.get("BTV")
            telemetry_data["Battery Charge"] = filtered_values.get("BTC")
            telemetry_data["Time Remaining"] = filtered_values.get("BT")
            telemetry_data["Input Volatge High"] = filtered_values.get("ALINPVHI")
            telemetry_data["Input Volatge Low"] = filtered_values.get("ALINPVLOW")

            # Assign the most recent timestamp
            for record in latest_entries:
                if record["timestamp"] and not str(record["timestamp"]).startswith("1970"):
                    timestamp_year = record["timestamp"].year

                    # Ignore any timestamp beyond the current year
                    if timestamp_year > current_year:
                        continue

                    if latest_timestamp is None or record["timestamp"] > latest_timestamp:
                        latest_timestamp = record["timestamp"]

                    # Capture valid timestamp for lat, long, or rssi
                    if record["key"] in ["INPV", "INPI", "INF"] and not str(record["timestamp"]).startswith("2099"):
                        valid_timestamp = record["timestamp"]

            # Check if latest timestamp is a future date and replace it
            if latest_timestamp and str(latest_timestamp).startswith("2099") and valid_timestamp:
                latest_timestamp = valid_timestamp

            telemetry_data["Timestamp"] = latest_timestamp

            # Append only if at least one telemetry value (except Device ID and Timestamp) is non-null
            if telemetry_data["Timestamp"] and any(
                telemetry_data[key] not in [None, "", "null"]  # Checking for null, empty, or string "null"
                for key in ["Serial Number", "Input Voltage", "Input Current", "Input Freq", "Output Voltage", "Output Current", "Output Load", "Output VA", "Watts", "Output Freq", "Battry Volatge", "Battery Charge", "Time Remaining", "Input Volatge High", "Input Volatge Low"]
            ):
                all_telemetry_data.append(telemetry_data)

        return {"status": "success", "data": all_telemetry_data}

    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching all device telemetry data")

        filtered_telemetry_data = [
            device for device in all_telemetry_data 
            if any(
                device[key] not in [None, "", "null"]  # Ensuring values are not None, empty, or "null" string
                for key in ["Serial Number", "Input Voltage", "Input Current", "Input Freq", "Output Voltage", "Output Current", "Output Load", "Output VA", "Watts", "Output Freq", "Battry Volatge", "Battery Charge", "Time Remaining", "Input Volatge High", "Input Volatge Low"]
            )
        ]

        return {"status": "success", "data": filtered_telemetry_data}




