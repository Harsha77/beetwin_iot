import re
import frappe
from datetime import datetime
from pytz import timezone   # ← add this import if not already there

IST = timezone("Asia/Kolkata")

# Accept ints/floats or numeric-like strings; reject '??.000', empty, NaN, etc.
_NUMERIC_RE = re.compile(r"^-?\d+(\.\d+)?$")

# keys we expect to be numeric-like
NUMERIC_KEYS = {
    "pv", "bt", "ht", "srno", "rssi", "ms", "rc", "sv", "rst", "lc", "sp", "lp",
    "lat", "long"
}

def is_numeric_like(v) -> bool:
    if isinstance(v, (int, float)):
        return True
    if isinstance(v, str):
        s = v.strip()
        if not s:
            return False
        return bool(_NUMERIC_RE.match(s))
    return False

def split_clean_and_invalid(records):
    """Return (clean_records, invalid_records) where invalid_records = [{'record':..., 'issues': {...}}]."""
    clean, invalid = [], []
    for rec in records or []:
        values = (rec or {}).get("values", {}) or {}
        issues = {}
        for k, v in values.items():
            if k in NUMERIC_KEYS and not is_numeric_like(v):
                issues[k] = v
        if issues:
            invalid.append({"record": rec, "issues": issues})
        else:
            clean.append(rec)
    return clean, invalid

def _to_dt_from_ms(ts_ms):
    """Convert epoch-ms to naive IST datetime (for display in logs/diagnostics)."""
    if not ts_ms:
        return None
    try:
        # Make it aware in IST, then drop tzinfo before saving to Datetime field
        dt_aware = datetime.fromtimestamp(int(ts_ms) / 1000.0, tz=IST)
        return dt_aware.replace(tzinfo=None)
    except Exception:
        return None

def log_diagnostic(device_key: str, invalid_item: dict, where: str, queue_row: str | None = None):
    """
    Prefer Device Diagnostics doctype if present; fallback to Error Log so we never lose signal.
    invalid_item = {'record': {...}, 'issues': {...}}
    """
    rec = invalid_item.get("record", {}) or {}
    issues = invalid_item.get("issues", {}) or {}
    values = rec.get("values", {}) or {}
    ts_ms = rec.get("ts")
    ts_dt = _to_dt_from_ms(ts_ms)

    # Try Device Diagnostics (if you created it in GUI as discussed)
    try:
        dd = frappe.get_doc({
            "doctype": "Device Diagnostics",
            "device_key": device_key or "",
            "ts": ts_dt,
            "invalid_fields": frappe.as_json(issues, indent=2),
            "values": frappe.as_json(values, indent=2),
            "where": where or "",
            "note": "Skipped from insertion due to invalid values",
            "queue_row": queue_row
        })
        dd.insert(ignore_permissions=True)
        frappe.db.commit()
        return
    except Exception as e:
        # Fallback to Error Log
        try:
            doc = frappe.get_doc({
                "doctype": "Error Log",
                "method": f"Diagnostics::{where}",
                "error_type": "Device Diagnostic",
                "error": frappe.as_json({
                    "device_key": device_key,
                    "ts": ts_ms,
                    "values": values,
                    "invalid_fields": issues,
                    "queue_row": queue_row,
                    "note": "Skipped from insertion due to invalid values",
                    "reason": f"Device Diagnostics insert failed: {e}"
                }, indent=2),
                "traceback": ""
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
        except Exception:
            frappe.log_error(
                message=frappe.as_json({
                    "device_key": device_key,
                    "invalid_item": invalid_item,
                    "where": where,
                    "queue_row": queue_row
                }, indent=2),
                title="Device Diagnostic (fallback)"
            )

