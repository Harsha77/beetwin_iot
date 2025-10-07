import frappe
import json
from frappe.model.document import Document
from frappe import _


@frappe.whitelist(allow_guest=True)
def add_device():
    try:
        # Get the request data
        data = frappe.request.get_data(as_text=True)
        data = json.loads(data)  # Parse JSON data

        # Iterate over JSON and create new documents
        for item in data:
            device = frappe.get_doc({
                "doctype": "Device",  # Replace with actual DocType name
                "imei_number": item.get("imei_number"),
                "name1": item.get("name"),
                "device_category": item.get("device_category"),
                "is_set_keys": item.get("is_set_keys"),
                "device_key": item.get("device_key"),
                "device_group": item.get("device_group")
            })
            device.insert(ignore_permissions=True)  # Insert into the database
            frappe.db.commit()  # Commit the changes

        return {"status": "success", "message": "Devices added successfully"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Device Insert API Error")
        return {"status": "error", "message": str(e)}
