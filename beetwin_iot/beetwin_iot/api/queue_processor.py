# beetwin_iot/beetwin_iot/api/queue_processor.py
import json
import frappe
from frappe.utils import now_datetime
from frappe.utils.background_jobs import enqueue

# IMPORTANT: we import the two processors you already have.
from beetwin_iot.beetwin_iot.api.read_data_Old import receive_telemetry, receive_reading



# -------------------------------
# Public helpers (manual triggers)
# -------------------------------
@frappe.whitelist()  # authenticated users only
def process_device_queue_now(limit: int = 50):
    """
    Manually process up to `limit` queued items, oldest first.
    Use: /api/method/beetwin_iot.beetwin_iot.api.queue_processor.process_device_queue_now?limit=25
    """
    count_ok, count_err = _process_batch(limit=limit)
    return {
        "status": "ok",
        "processed": count_ok,
        "failed": count_err,
    }

@frappe.whitelist()  # authenticated users only
def process_device_queue_async(limit: int = 100):
    """
    Enqueue background job to process queue. Call from scheduler or CLI.
    """
    enqueue(
        method="beetwin_iot.beetwin_iot.api.queue_processor._process_batch",
        queue="long",
        job_name="process_device_data_queue",
        limit=limit,
    )


# --------------------------
# Core batch processing logic
# --------------------------
def _process_batch(limit: int = 100):
    """
    Pick earliest 'Queued' items, mark each 'Processing', run handlers,
    then mark 'Done' or 'Failed' individually (commit per item).
    Returns (ok_count, err_count).
    """
    ok = err = 0

    # Fetch oldest queued records
    rows = frappe.get_all(
        "Device Data Queue",
        filters={"status": ("in", ["Queued", "QUEUED", "Pending"])},
        fields=["name"],
        limit_page_length=limit,
        order_by="creation asc",
    )

    for r in rows:
        try:
            doc = frappe.get_doc("Device Data Queue", r.name)

            # Double-check still queued
            if (doc.status or "").lower() not in ("queued", "pending"):
                continue

            # Mark as Processing
            doc.db_set("status", "Processing", update_modified=False)
            if hasattr(doc, "processing_started_at"):
                doc.db_set("processing_started_at", now_datetime(), update_modified=False)
            frappe.db.commit()

            # Parse JSON (payload_json is stored via frappe.as_json)
            payload = _safe_parse(doc.payload_json)

            # Call your existing processors
            telem_res = receive_telemetry(payload)
            read_res = receive_reading(payload)

            # Build a tiny summary message
            msg = f"telemetry={telem_res.get('status')}, reading={read_res.get('status')}"

            # Mark Done
            doc.db_set("status", "Done", update_modified=False)
            if hasattr(doc, "processed_at"):
                doc.db_set("processed_at", now_datetime(), update_modified=False)
            if hasattr(doc, "processing_note"):
                doc.db_set("processing_note", msg, update_modified=False)

            frappe.db.commit()
            ok += 1

        except Exception:
            # Mark Failed with traceback
            tb = frappe.get_traceback()
            try:
                doc = frappe.get_doc("Device Data Queue", r.name)
                doc.db_set("status", "Failed", update_modified=False)
                if hasattr(doc, "error"):
                    doc.db_set("error", tb[:2000], update_modified=False)  # avoid huge text
                frappe.db.commit()
            except Exception:
                frappe.db.rollback()

            frappe.log_error(tb, "Device Data Queue: Processing Failed")
            err += 1

    return ok, err


def _safe_parse(s: str):
    """Parse frappe.as_json string back to dict."""
    if isinstance(s, dict):
        return s
    try:
        return json.loads(s or "{}")
    except Exception:
        # Fallback if payload_json accidentally stored as Python repr
        return frappe.parse_json(s) if hasattr(frappe, "parse_json") else {}