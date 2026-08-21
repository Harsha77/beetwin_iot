import frappe
from datetime import datetime
from pytz import timezone

# NEW: validator/diagnostics helpers (no change to your processor/scheduler)
from beetwin_iot.beetwin_iot.api.validators_and_diagnostics import (
    split_clean_and_invalid, log_diagnostic
)

import frappe
from datetime import datetime
from pytz import timezone

from beetwin_iot.beetwin_iot.api.validators_and_diagnostics import (
    split_clean_and_invalid, log_diagnostic
)

# ---------------------------------------------------
# Function to process telemetry data for a device.
# - Uses your existing working logic (device_telemetry_data)
# - Adds validation: invalid records -> Device Diagnostics
# - Only clean records are merged into telemetry
# ---------------------------------------------------
def receive_telemetry(json_data):
    try:
        ist = timezone("Asia/Kolkata")

        device_key = json_data.get("device_key")
        if not device_key:
            return {"status": "error", "message": "Missing device_key"}

        # Get Device document
        device = frappe.get_doc("Device", {"device_key": device_key})

        # ---- NEW: validate incoming records first ----
        incoming = json_data.get("data") or []
        clean, invalid = split_clean_and_invalid(incoming)
        queue_row = json_data.get("_queue_row")

        # Log invalid records into Device Diagnostics
        for inv in invalid:
            log_diagnostic(device_key, inv, where="receive_telemetry", queue_row=queue_row)

        # If nothing valid left, stop here
        if not clean:
            return {
                "status": "skipped",
                "message": f"0 valid telemetry; {len(invalid)} invalid logged"
            }

        # From here, logic is same as your original WORKING code,
        # but it runs only on 'clean' records instead of all 'data'
        telemetry_data = {}

        # Check if telemetry document already exists for this device
        parent_doc_name = frappe.db.get_value(
            "Device Telemetry",
            {"device_id": device.name},
            "name"
        )

        # Load existing document if available
        if parent_doc_name:
            telemetry_doc = frappe.get_doc("Device Telemetry", parent_doc_name)
            for entry in telemetry_doc.device_telemetry_data:
                key = entry.key
                ts_ms = int(entry.timestamp.replace(tzinfo=ist).timestamp() * 1000)

                value = entry.value
                telemetry_data[key] = {
                    "ts": ts_ms,
                    "timestamp": entry.timestamp,
                    "value": value
                }
        else:
            # Create new telemetry document
            telemetry_doc = frappe.get_doc({
                "doctype": "Device Telemetry",
                "device_id": device.name,
                "device_telemetry_data": [],
            })

        # Merge incoming telemetry values, preserving latest timestamp
        for record in clean:     # NOTE: use 'clean' instead of original 'data'
            ts = record.get("ts")
            if not ts:
                continue

            timestamp = datetime.fromtimestamp(ts / 1000.0, tz=ist).replace(tzinfo=None)
            values = format_field_names(record.get("values", {}))
            values.pop("im", None)  # Remove image data or irrelevant key

            for key, value in values.items():
                if key not in telemetry_data or ts > telemetry_data[key]["ts"]:
                    telemetry_data[key] = {
                        "ts": ts,
                        "timestamp": timestamp,
                        "value": value
                    }

        # Clear existing telemetry child entries and append fresh ones
        telemetry_doc.set("device_telemetry_data", [])

        for key, entry in telemetry_data.items():
            telemetry_doc.append("device_telemetry_data", {
                "timestamp": entry["timestamp"],
                "key": key,
                "value": entry["value"],
            })

        # Update document datetime and save changes
        if hasattr(telemetry_doc, "datetime"):
            telemetry_doc.datetime = datetime.now(ist).replace(tzinfo=None)

        telemetry_doc.save()
        frappe.db.commit()

        note = f" ({len(invalid)} invalid skipped)" if invalid else ""
        return {"status": "success", "message": "Telemetry data recorded successfully" + note}

    except Exception as e:
        frappe.log_error(message=frappe.get_traceback(), title="Telemetry Processing Error")
        return {"status": "error", "message": str(e)}


def format_field_names(values):
    """Format field names to ensure they are valid for Frappe and match the JSON data keys."""
    formatted_values = {}
    for key, value in values.items():
        formatted_key = key.replace("-", "_")  # Replace hyphen with underscore
        formatted_values[formatted_key] = value
    return formatted_values




def receive_reading(json_data):
    """
    Validates incoming records:
      - Logs any invalid items (e.g., pv='??.000') to Device Diagnostics (or Error Log)
      - Inserts ONLY the clean items into Device Reading
    """
    try:
        ist = timezone("Asia/Kolkata")

        device_key = json_data.get('device_key')
        if not device_key:
            return {"status": "error", "message": "Missing device_key"}

        device = frappe.get_doc("Device", {"device_key": device_key})

        incoming = json_data.get("data") or []
        clean, invalid = split_clean_and_invalid(incoming)

        queue_row = json_data.get("_queue_row")

        for inv in invalid:
            log_diagnostic(device_key, inv, where="receive_reading", queue_row=queue_row)

        if not clean:
            return {"status": "skipped", "message": f"0 valid readings; {len(invalid)} invalid logged"}

        for record in clean:
            ts = record.get("ts")
            timestamp = datetime.fromtimestamp(ts / 1000.0).astimezone(ist).replace(tzinfo=None)
            values = record.get("values", {}) or {}

            doc = frappe.get_doc({
                "doctype": "Device Reading",
                "device_id": device.name,
                "timestamp": timestamp,
            })
            doc.insert(ignore_permissions=True)

            for key, value in values.items():
                doc.append("reading", {"key": key, "value": value})

            doc.save()

        frappe.db.commit()
        note = f" ({len(invalid)} invalid skipped)" if invalid else ""
        return {"status": "success", "message": "Readings saved" + note}

    except Exception as e:
        frappe.log_error(message=str(e), title="Reading Processing Error")
        return {"status": "error", "message": str(e)}


