import frappe
from frappe.utils.background_jobs import enqueue
from frappe.utils import now_datetime

# --------------------------------------------------
# Phase 1: Fast entry point — save payload and return
# --------------------------------------------------
@frappe.whitelist(allow_guest=True)
def read_data():
    try:
        json_data = frappe.request.json
        device_key = json_data.get("device_key")

        if not device_key:
            return {"status": "error", "message": "Missing device_key"}

        # Step 1: enqueue background insert
        enqueue(
            method="beetwin_iot.beetwin_iot.api.read_data.store_device_data",
            queue='long',  # long queue recommended for high volume
            job_name=f"device_data_{device_key}",
            json_data=json_data
        )

        return {"status": "queued", "message": "Data accepted for processing"}

    except Exception as e:
        frappe.log_error(message=str(e), title="Device Data Queue Error")
        return {"status": "error", "message": str(e)}


# --------------------------------------------------
# Phase 2: Background worker inserts data safely
# --------------------------------------------------
def store_device_data(json_data):
    try:
        device_key = json_data.get("device_key")
        doc = frappe.get_doc({
            "doctype": "Device Data Queue",
            "device_key": device_key,
            "payload_json": frappe.as_json(json_data, indent=None),
            "received_at": now_datetime(),
            "status": "Queued",
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

    except Exception as e:
        frappe.log_error(message=str(e), title="Device Data Save Failed")

