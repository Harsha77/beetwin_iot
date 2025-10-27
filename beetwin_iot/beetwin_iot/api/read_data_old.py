import frappe
from datetime import datetime
from pytz import timezone  # Import timezone for IST conversion

# -----------------------------------------
# Main entry point for receiving device data.
# This function:
# - Accepts a JSON payload from an API request.
# - Validates the device key.
# - Forwards the payload to telemetry and reading processors.
# - Returns a consolidated response.
# -----------------------------------------

@frappe.whitelist(allow_guest=True)
def read_data():
    try:
        # Extract JSON payload
        json_data = frappe.request.json
        # Validate device key
        device_key = json_data.get('device_key')
        if not device_key:
            return {"status": "error", "message": "Device key is required"}

        # Call receive_telemetry() and receive_reading() functions
        telemetry_result = receive_telemetry(json_data)
        reading_result = receive_reading(json_data)

        # Consolidate results
        return {
            "status": "success",
            "telemetry_result": telemetry_result,
            "reading_result": reading_result
        }

    except Exception as e:
        frappe.log_error(message=str(e), title="Read Data Error")
        return {"status": "error", "message": str(e)}
    
    
# ------------------------------------------------------------
    # Step 1: Log raw request and request metadata
    # - Capture the raw request body before parsing JSON.
    # - Collect headers, endpoint, IP, and body size for debugging.
    # - Attempt to parse JSON and store it in the log if available.
    # ------------------------------------------------------------
    # ------------------------------------------------------------
    # Step 2: Handle requests without valid JSON
    # - Log a "device connected" event without payload data.
    # - Return an error indicating no JSON was posted.
    # ------------------------------------------------------------
    # ------------------------------------------------------------
    # Step 3: Process valid JSON payload
    # - Validate required parameters (device_key).
    # - Forward payload to telemetry and reading processing functions.
    # - Count API hits (optional).
    # - Return processing results.
    # ------------------------------------------------------------    
# ------------------------------------------------------------
# @frappe.whitelist(allow_guest=True)
# def read_data():
#     try:
#         # --- Log raw request body (before JSON decoding) ---
#         request_body = frappe.request.get_data(as_text=True)
#         frappe.logger().info(f"Raw Request Body:\n{request_body}")

#         # --- Log API hit info (headers, IP, etc.) ---
#         info_dict = {
#             "info": "API endpoint hit (no guarantee of JSON)",
#             "endpoint": frappe.request.path,
#             "headers": dict(frappe.request.headers),
#             "ip": frappe.local.request_ip or frappe.request.environ.get('REMOTE_ADDR'),
#             "raw_body_length": len(request_body),
#         }

#         # Attempt to decode JSON from raw request
#         payload_json = None
#         try:
#             payload_json = frappe.request.json
#         except Exception as json_err:
#             payload_json = None
#             info_dict["json_error"] = str(json_err)

#         if payload_json:
#             info_dict["payload"] = payload_json

#         frappe.get_doc({
#             "doctype": "Error Log",
#             "method": "API Hit: read_data",
#             "error": frappe.as_json(info_dict),
#             "traceback": "",
#             "error_type": "API Info"
#         }).insert(ignore_permissions=True)

#     except Exception as log_err:
#         frappe.log_error(f"API logging failed: {log_err}", "API Hit Logging Error")

#     # --- Handle POSTs with no valid JSON ---
#     if not frappe.request.json:
#         try:
#             frappe.get_doc({
#                 "doctype": "Error Log",
#                 "method": "Connect with API",
#                 "error": frappe.as_json({
#                     "info": "Device connected (HTTP POST, no JSON)",
#                     "endpoint": frappe.request.path,
#                     "headers": dict(frappe.request.headers),
#                     "ip": frappe.local.request_ip or frappe.request.environ.get('REMOTE_ADDR'),
#                     "raw_body": request_body
#                 }),
#                 "traceback": "",
#                 "error_type": "Device Connect"
#             }).insert(ignore_permissions=True)
#         except Exception as log_err:
#             frappe.log_error(f"Connect with API log failed: {log_err}", "API Device Connect Logging Error")
#         return {"status": "error", "message": "Device connected, but no JSON posted."}

#     # --- Process valid JSON payload ---
#     try:
#         json_data = frappe.request.json

#         # API hit count (optional)
#         try:
#             api_hit_count = frappe.db.count("Error Log", filters={"method": "API Hit: read_data"})
#         except Exception:
#             api_hit_count = None

#         # Validate device key
#         device_key = json_data.get('device_key')
#         if not device_key:
#             return {"status": "error", "message": "Device key is required"}

#         # Process telemetry and reading
#         telemetry_result = receive_telemetry(json_data)
#         reading_result = receive_reading(json_data)

#         return {
#             "status": "success",
#             "telemetry_result": telemetry_result,
#             "reading_result": reading_result,
#             "api_hit_count": api_hit_count
#         }

#     except Exception as e:
#         frappe.log_error(message=str(e), title="Read Data Error")
#         return {"status": "error", "message": str(e)}


    

# ---------------------------------------------------
# Function to process telemetry data for a device.
# It does the following:
# - Loads or creates a Device Telemetry document.
# - Merges new telemetry data with existing records (if present).
# - Ensures only the latest data per key is saved.
# - Saves all data to child table: device_telemetry_data.
# ---------------------------------------------------
def receive_telemetry(json_data):
    try:
        ist = timezone("Asia/Kolkata")

        device_key = json_data.get("device_key")
        device = frappe.get_doc("Device", {"device_key": device_key})
        data = json_data.get("data")

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
        for record in data:
            ts = record.get("ts")
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
        telemetry_doc.datetime = datetime.now(ist).replace(tzinfo=None)

        telemetry_doc.save()
        frappe.db.commit()

        return {"status": "success", "message": "Telemetry data recorded successfully"}

    except Exception as e:
        frappe.log_error(message=str(e), title="Telemetry Processing Error")
        return {"status": "error", "message": str(e)}


# -----------------------------------------------------
# Function to process and store reading data per device.
# - For each telemetry record, a new 'Device Reading' is created.
# - Each reading has its own timestamp and child key-value pairs.
# - Data is committed individually for each entry to maintain integrity.
# -----------------------------------------------------
def receive_reading(json_data):
    try:
        # Define IST timezone
        ist = timezone("Asia/Kolkata")

        # Validate and process reading data
        device_key = json_data.get('device_key')
        device = frappe.get_doc("Device", {"device_key": device_key})
        data = json_data.get('data')

        for record in data:
            # Convert timestamp to IST and remove tzinfo for storage
            timestamp = datetime.fromtimestamp(record["ts"] / 1000.0).astimezone(ist).replace(tzinfo=None)
            values = record.get("values", {})

            # Always create a new "Device Reading" document
            device_reading_doc = frappe.get_doc({
                "doctype": "Device Reading",
                "device_id": device.name,
                "timestamp": timestamp,
            })
            device_reading_doc.insert(ignore_permissions=True)

            for key, value in values.items():
                # Always append new key-value pairs
                device_reading_doc.append("reading", {
                    "key": key,
                    "value": value
                })

            device_reading_doc.save()

        frappe.db.commit()
        return {"status": "success", "message": "Reading data recorded successfully"}

    except Exception as e:
        frappe.log_error(message=str(e), title="Reading Processing Error")
        return {"status": "error", "message": str(e)}


# -----------------------------------------------------
# Helper function to format incoming telemetry keys.
# - Replaces hyphens with underscores.
# - Ensures compatibility with Frappe's field naming rules.
# -----------------------------------------------------
def format_field_names(values):
    """Format field names to ensure they are valid for Frappe and match the JSON data keys."""
    formatted_values = {}
    for key, value in values.items():
        formatted_key = key.replace("-", "_")  # Replace hyphen with underscore and lowercase
        formatted_values[formatted_key] = value
    return formatted_values