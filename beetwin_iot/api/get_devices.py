import frappe

# ================================================================
# API Endpoint: get_user_devices
# ------------------------------------------------
# Description:
#   This function retrieves a list of devices assigned to a user.
#   If no user is explicitly provided, it defaults to the logged-in user.
# Parameters:
#   user (str, optional) - The user ID (email); if None, uses frappe.session.user
# Returns:
#   List of dictionaries with device_id and device_name for the user
# ================================================================
@frappe.whitelist(allow_guest=True)
def get_user_devices(user=None):
    if not user:
        user = frappe.session.user  # Default to the logged-in user

    devices = frappe.get_all(
        "User Device Mapping",
        filters={"user": user},
        fields=["device as device_id", "device.device_name"]
    )

    return devices if devices else []  # Return empty list if no devices found


import frappe
from frappe import _

# ================================================================
# API Endpoint: get_devices
# ------------------------------------------------
# Description:
#   Fetches all records from the "Device Telemetry" DocType.
#   Returns a list of devices with their unique ID and name.
# Returns:
#   A JSON response with a success flag and either:
#     - "data": list of devices on success
#     - "error": error message string on failure
# ================================================================
@frappe.whitelist(allow_guest=True)
def get_devices():
    try:
        devices = frappe.get_all("Device Telemetry", fields=["device_id", "name"])
        return {"success": True, "data": devices}
    except Exception as e:
        return {"success": False, "error": str(e)}
