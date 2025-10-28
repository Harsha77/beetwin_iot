import frappe
from datetime import datetime, timedelta
from pytz import timezone as pytz_timezone

# ===== CONFIG =====
IST = pytz_timezone("Asia/Kolkata")

BATCH_SIZE        = 300        # queue rows per run
CHILD_CHUNK       = 1000       # bulk chunk size for child rows
ACCEPT_PAST_DAYS  = 365        # ts >= now-365d
ACCEPT_FUTURE_MIN = 1440       # ts <= now+1d

# ===== time & helpers =====
def ms_to_ist_naive(ts_ms: int) -> datetime:
    return datetime.fromtimestamp(ts_ms / 1000.0, tz=IST).replace(tzinfo=None)

def now_utc_ms() -> int:
    return int(datetime.utcnow().timestamp() * 1000)

def normalize_keys(d: dict) -> dict:
    out = {}
    for k, v in (d or {}).items():
        out[k.replace("-", "_")] = v
    return out

def _num(v, default=None):
    try:
        return float(v)
    except Exception:
        return default

# ===== validation =====
def validate_record(rec, errors, idx):
    """
    Validate one item in data[]: {"ts": <int ms>, "values": {...}}
    Returns (ok, cleaned_values).
    """
    ok = True
    if "ts" not in rec or "values" not in rec:
        errors.append((idx, "BAD_SCHEMA", "Each item must contain 'ts' and 'values'"))
        return False, {}

    ts_ms = rec["ts"]
    if not isinstance(ts_ms, int):
        errors.append((idx, "TS_NOT_INT", f"ts not int: {ts_ms}"))
        return False, {}

    now = now_utc_ms()
    min_ms = now - ACCEPT_PAST_DAYS * 86400 * 1000
    max_ms = now + ACCEPT_FUTURE_MIN * 60 * 1000
    if not (min_ms <= ts_ms <= max_ms):
        errors.append((idx, "TS_OUT_OF_RANGE", f"ts={ts_ms}"))
        ok = False

    values = normalize_keys(rec.get("values", {}))

    # example sanity checks (extend as needed)
    if "lat" in values:
        lat = _num(values["lat"])
        if lat is None or lat < -90 or lat > 90:
            errors.append((idx, "LAT_INVALID", f"lat={values['lat']}"))
            ok = False
    if "long" in values:
        lng = _num(values["long"])
        if lng is None or lng < -180 or lng > 180:
            errors.append((idx, "LONG_INVALID", f"long={values['long']}"))
            ok = False
    if "bt" in values:
        bt = _num(values["bt"])
        if bt is None or bt < 0 or bt > 100:
            errors.append((idx, "BT_RANGE", f"bt={values['bt']}"))
            ok = False

    values.pop("im", None)  # drop bulky fields you don't want
    return ok, values

# ===== telemetry helpers =====
def fetch_or_create_telemetry(device_name: str):
    parent_name = frappe.db.get_value("Device Telemetry", {"device_id": device_name}, "name")
    if parent_name:
        return frappe.get_doc("Device Telemetry", parent_name)
    doc = frappe.get_doc({
        "doctype": "Device Telemetry",
        "device_id": device_name,
        "device_telemetry_data": [],   # child table fieldname (EXACT)
    })
    doc.insert(ignore_permissions=True)
    return doc

def load_telem_map(device_name: str):
    """Return key -> (ts_ms, ts_dt, value) map of current telemetry."""
    parent_name = frappe.db.get_value("Device Telemetry", {"device_id": device_name}, "name")
    if not parent_name:
        return {}
    rows = frappe.db.sql(
        """
        SELECT `key`, `timestamp`, `value`
        FROM `tabDevice Telemetry Key-Value`
        WHERE parent = %s
        """,
        (parent_name,),
        as_dict=True
    )
    m = {}
    for r in rows:
        ts_dt = r["timestamp"]
        ts_ms = int(IST.localize(ts_dt).timestamp() * 1000)
        m[r["key"]] = (ts_ms, ts_dt, r["value"])
    return m

def upsert_telemetry_latest(device_name: str, incoming_pairs: list):
    """
    incoming_pairs: list[(key, ts_ms, value)]
    Keep only latest per key for this device.
    """
    parent = fetch_or_create_telemetry(device_name)
    current = load_telem_map(device_name)

    for k, ts_ms, v in incoming_pairs:
        if k not in current or ts_ms > current[k][0]:
            current[k] = (ts_ms, ms_to_ist_naive(ts_ms), v)

    parent.set("device_telemetry_data", [])  # overwrite snapshot
    for k, (_, ts_dt, v) in current.items():
        parent.append("device_telemetry_data", {
            "key": k,
            "value": v,
            "timestamp": ts_dt
        })
    parent.save(ignore_permissions=True)

# ===== diagnostics =====
def create_diagnostic(queue_row_name, device_key, errors, payload_json, severity="error"):
    reason_codes = ",".join(sorted({code for _, code, _ in errors})) or "UNKNOWN"
    detail_lines = [f"idx={i} code={c} msg={m}" for i, c, m in errors]
    detail = "\n".join(detail_lines)[:2000]
    frappe.get_doc({
        "doctype": "Device Ingest Diagnostic",
        "queue_row": queue_row_name,
        "device_key": device_key or "",
        "severity": severity,
        "reason_code": reason_codes,
        "reason_detail": detail,
        "payload_json": payload_json,
        "received_at": frappe.db.get_value("Device Data Queue", queue_row_name, "received_at"),
        "processed_at": datetime.now(IST).replace(tzinfo=None),
        "retry_count": 0
    }).insert(ignore_permissions=True)

# ===== core =====
def _fetch_queued_rows(batch_size: int, hours_window=None):
    if hours_window and hours_window > 0:
        start = datetime.utcnow() - timedelta(hours=hours_window)
        return frappe.db.sql(
            """
            SELECT name, device_key, payload_json
            FROM `tabDevice Data Queue`
            WHERE TRIM(IFNULL(status,'')) = 'Queued'
              AND received_at >= %s
            ORDER BY creation ASC
            LIMIT %s
            """,
            (start, batch_size),
            as_dict=True
        )
    return frappe.db.sql(
        """
        SELECT name, device_key, payload_json
        FROM `tabDevice Data Queue`
        WHERE TRIM(IFNULL(status,'')) = 'Queued'
        ORDER BY creation ASC
        LIMIT %s
        """, (batch_size,), as_dict=True
    )

def process_queue(batch_size=BATCH_SIZE, tolerant_mode=True, hours_window=None):
    rows = _fetch_queued_rows(batch_size, hours_window)
    if not rows:
        return {"processed_rows": 0, "diagnosed_rows": 0, "parents_inserted": 0, "children_inserted": 0}

    parent_keyset = set()      # (device_id, timestamp)
    reading_parents = []       # to create Device Reading parents
    child_temp = []            # (device_id, ts_dt, key, value)
    telemetry_bucket = {}      # device_name -> [(key, ts_ms, value)]
    to_processed, to_failed = [], []
    processed = diagnosed = 0

    try:
        for q in rows:
            errors = []
            try:
                payload = frappe.parse_json(q["payload_json"])
                device_key = payload.get("device_key")
                data_list = payload.get("data", [])

                if not device_key:
                    errors.append((-1, "MISSING_DEVICE_KEY", "device_key not found"))
                if not isinstance(data_list, list) or len(data_list) == 0:
                    errors.append((-1, "EMPTY_OR_BAD_DATA", "data[] missing or empty"))

                # ensure device exists
                device_name = None
                if not errors:
                    device_name = frappe.db.get_value("Device", {"device_key": device_key}, "name")
                    if not device_name:
                        errors.append((-1, "DEVICE_NOT_FOUND", f"device_key={device_key}"))

                valid_count = 0
                if device_name and not errors:
                    for idx, rec in enumerate(data_list):
                        ok, cleaned = validate_record(rec, errors, idx)
                        if not ok:
                            continue

                        ts_ms = int(rec["ts"])
                        ts_dt = ms_to_ist_naive(ts_ms)

                        # Device Reading parent (dedup per device+timestamp)
                        pk = (device_name, ts_dt)
                        if pk not in parent_keyset:
                            parent_keyset.add(pk)
                            reading_parents.append({"device_id": device_name, "timestamp": ts_dt})

                        # children stage (parent resolved later)
                        for k, v in cleaned.items():
                            child_temp.append((device_name, ts_dt, k, v))

                        # telemetry candidates
                        bucket = telemetry_bucket.setdefault(device_name, [])
                        for k, v in cleaned.items():
                            bucket.append((k, ts_ms, v))

                        valid_count += 1

                # diagnostics routing
                if (not tolerant_mode and errors) or (tolerant_mode and valid_count == 0):
                    create_diagnostic(q["name"], device_key, errors, q["payload_json"], "error")
                    diagnosed += 1
                    to_processed.append(q["name"])
                else:
                    if tolerant_mode and errors:
                        create_diagnostic(q["name"], device_key, errors, q["payload_json"], "warning")
                        diagnosed += 1
                    to_processed.append(q["name"])

                processed += 1

            except Exception:
                to_failed.append(q["name"])
                frappe.log_error(frappe.get_traceback(), "Queue row normalize failure")

        # ===== WRITE =====

        # 1) Parents (ORM insert so names are generated)
        parent_lookup = {}
        parents_created = 0
        for rp in reading_parents:
            try:
                pdoc = frappe.get_doc({
                    "doctype": "Device Reading",
                    "device_id": rp["device_id"],
                    "timestamp": rp["timestamp"],
                })
                pdoc.insert(ignore_permissions=True)
                parent_lookup[(rp["device_id"], rp["timestamp"])] = pdoc.name
                parents_created += 1
            except Exception:
                frappe.log_error(frappe.get_traceback(), "Parent insert failed (Device Reading)")

        # 2) Children → Device Reading Key-Value (parentfield = reading)
        child_keyset, final_children = set(), []
        for device_id, ts_dt, k, v in child_temp:
            parent_name = parent_lookup.get((device_id, ts_dt))
            if not parent_name:
                continue
            uk = (parent_name, k)
            if uk in child_keyset:
                continue
            child_keyset.add(uk)
            final_children.append({
                "parent": parent_name,
                "parenttype": "Device Reading",
                "parentfield": "reading",   # EXACT fieldname in your doctype
                "key": k,
                "value": v
            })

        children_inserted = 0
        if final_children:
            for i in range(0, len(final_children), CHILD_CHUNK):
                chunk = final_children[i:i+CHILD_CHUNK]
                frappe.db.bulk_insert("Device Reading Key-Value", chunk)
                children_inserted += len(chunk)

        # 3) Telemetry latest per key
        for device_name, pairs in telemetry_bucket.items():
            try:
                upsert_telemetry_latest(device_name, pairs)
            except Exception:
                frappe.log_error(frappe.get_traceback(), f"Telemetry upsert failed ({device_name})")

        # 4) Mark queue rows
        if to_processed:
            frappe.db.sql(
                """UPDATE `tabDevice Data Queue` SET status='Processed'
                   WHERE name IN ({})""".format(", ".join(["%s"]*len(to_processed))),
                tuple(to_processed)
            )
        if to_failed:
            frappe.db.sql(
                """UPDATE `tabDevice Data Queue` SET status='Failed'
                   WHERE name IN ({})""".format(", ".join(["%s"]*len(to_failed))),
                tuple(to_failed)
            )

        frappe.db.commit()
        return {
            "processed_rows": processed,
            "diagnosed_rows": diagnosed,
            "parents_inserted": parents_created,
            "children_inserted": children_inserted
        }

    except Exception:
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), "process_queue failed")
        return {"processed_rows": 0, "diagnosed_rows": 0, "parents_inserted": 0, "children_inserted": 0}

# ===== public endpoints =====
@frappe.whitelist()
def run_phase2_now():
    return process_queue(batch_size=BATCH_SIZE, tolerant_mode=True)

@frappe.whitelist()
def run_phase2_last24h():
    return process_queue(batch_size=BATCH_SIZE, tolerant_mode=True, hours_window=24)

@frappe.whitelist()
def run_phase2_debug_info():
    counts = frappe.db.sql("""
        select trim(ifnull(status,'')) as status, count(*) as c
        from `tabDevice Data Queue`
        group by trim(ifnull(status,''))
        order by c desc
    """, as_dict=True)
    rows = frappe.db.sql("""
        select name, concat('[', ifnull(status,''), ']') as status_exact,
               received_at, creation
        from `tabDevice Data Queue`
        order by creation desc
        limit 10
    """, as_dict=True)
    return {"counts_by_status": counts, "recent_rows": rows}

@frappe.whitelist()
def run_phase2_trace(limit_rows: int = 20):
    """Dry-run style visibility for queued rows."""
    rows = frappe.db.sql(
        """
        SELECT name, device_key, payload_json
        FROM `tabDevice Data Queue`
        WHERE TRIM(IFNULL(status,''))='Queued'
        ORDER BY creation ASC
        LIMIT %s
        """,
        (limit_rows,), as_dict=True
    )
    trace = {"picked": len(rows), "rows": []}
    for q in rows:
        one = {"name": q["name"], "device_key": q["device_key"], "decisions": []}
        try:
            payload = frappe.parse_json(q["payload_json"])
            dk = payload.get("device_key"); data = payload.get("data", [])
            if not dk:
                one["decisions"].append("MISSING_DEVICE_KEY")
            if not isinstance(data, list) or not data:
                one["decisions"].append("EMPTY_OR_BAD_DATA")
            name = frappe.db.get_value("Device", {"device_key": dk}, "name") if dk else None
            if not name:
                one["decisions"].append(f"DEVICE_NOT_FOUND: {dk}")
            valid_cnt = 0
            if name and isinstance(data, list):
                for idx, rec in enumerate(data):
                    errs = []
                    ok, _ = validate_record(rec, errs, idx)
                    if ok: valid_cnt += 1
            if name and valid_cnt > 0:
                one["decisions"].append(f"OK: device={name}, valid_items={valid_cnt}")
            elif name and valid_cnt == 0:
                one["decisions"].append("ALL_ITEMS_INVALID")
        except Exception as e:
            one["decisions"].append(f"BAD_JSON: {e}")
        trace["rows"].append(one)
    return trace

# ===== deep debug helpers =====
@frappe.whitelist()
def debug_fingerprint():
    """See which site you're on + quick queue visibility."""
    site = frappe.local.site
    db  = frappe.conf.db_name
    statuses = frappe.db.sql("""
        SELECT TRIM(IFNULL(status,'')) AS status, COUNT(*) c
        FROM `tabDevice Data Queue`
        GROUP BY TRIM(IFNULL(status,''))
        ORDER BY c DESC
    """, as_dict=True)
    recent = frappe.db.sql("""
        SELECT name, status, received_at, creation
        FROM `tabDevice Data Queue`
        ORDER BY creation DESC
        LIMIT 5
    """, as_dict=True)
    return {"site": site, "db": db, "queue_counts": statuses, "recent_rows": recent}

@frappe.whitelist()
def debug_where_am_i():
    import inspect, sys
    mod = sys.modules[__name__]
    return {"module": __name__, "file": inspect.getsourcefile(mod)}