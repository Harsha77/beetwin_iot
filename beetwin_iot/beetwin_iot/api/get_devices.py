import frappe


@frappe.whitelist(allow_guest=True)
def get_user_devices(user=None):
    if not user:
        user = frappe.session.user  # Default to the logged-in user

    devices = frappe.get_all(
        "User Device Mapping",
        filters={"user": user},
        fields=["device as device_id", "device.device_name"]
    )

    return devices if devices else []


import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_devices():
    try:
        devices = frappe.get_all("Device Telemetry", fields=["device_id", "name"])
        return {"success": True, "data": devices}
    except Exception as e:
        return {"success": False, "error": str(e)}

