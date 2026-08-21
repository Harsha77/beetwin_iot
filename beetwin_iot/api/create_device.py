# -------------------------------------------------------------------
# Module: Device Management API
# Description:
#     This module defines an API endpoint to bulk-insert device records
#     into the "Device" DocType in Frappe via a POST request.
#     The endpoint is guest-accessible and accepts JSON payloads.
# -------------------------------------------------------------------

import frappe
import json
from frappe.model.document import Document
from frappe import _

# -------------------------------------------------------------------
# Function: add_device
# Access: Public (allow_guest=True)
# Description:
#     Accepts a JSON array of device records via POST and inserts
#     each record as a new "Device" document in Frappe.
#
# Returns:
#     dict: A success message on successful insertion or
#           an error message with details on failure.
# -------------------------------------------------------------------
@frappe.whitelist(allow_guest=True)
def add_device():
    try:
        # Get the request payload as plain text
        data = frappe.request.get_data(as_text=True)

        # Parse the JSON string into a Python object (list of dicts)
        data = json.loads(data)

        # Iterate through each item in the list to create new Device docs
        for item in data:
            device = frappe.get_doc({
                "doctype": "Device",  # DocType where the record will be inserted
                "imei_number": item.get("imei_number"),  # IMEI Number of device
                "name1": item.get("name"),               # Custom field for name
                "device_category": item.get("device_category"),  # Category
                "is_set_keys": item.get("is_set_keys"),          # Boolean flag
                "device_key": item.get("device_key"),            # Device Key
                "device_group": item.get("device_group")         # Assigned group
            })

            # Insert the document into the database ignoring permission checks
            device.insert(ignore_permissions=True)

            # Commit the change immediately to the database
            frappe.db.commit()

        # Return a success response if all records were inserted
        return {"status": "success", "message": "Devices added successfully"}

    except Exception as e:
        # Log the complete traceback in Frappe error logs
        frappe.log_error(frappe.get_traceback(), "Device Insert API Error")

        # Return an error response with the exception message
        return {"status": "error", "message": str(e)}
