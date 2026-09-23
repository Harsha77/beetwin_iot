import frappe
from frappe import _
from datetime import datetime


# =============================================================================
# FUNCTION: get_filtered_device_data
# DESCRIPTION:
#   Main API endpoint to fetch telemetry data only for devices that the user 
#   has permission to access. System Managers can access all devices.
# RETURN:
#   JSON response with filtered telemetry data or error messages.
# =============================================================================
@frappe.whitelist(allow_guest=True)
def get_public_device_telemetry():
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

