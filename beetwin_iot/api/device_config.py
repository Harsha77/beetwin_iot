import frappe
from datetime import datetime
from pytz import timezone  # Import timezone for IST conversion
import os
import shutil
import zipfile
import tempfile
import frappe

# ===========================================================
# API Endpoint: device_config
# ----------------------------
# This is a public API that receives configuration data for a device,
# processes and saves it into the "Device Config" DocType.
# ===========================================================
@frappe.whitelist(allow_guest=True)
def device_config():
    try:
        # Extract JSON payload
        json_data = frappe.request.json

        # Validate device key
        device_key = json_data.get('device_key')
        if not device_key:
            return {"status": "error", "message": "Device key is required"}

        # Call receive_device_config() function to handle the logic
        device_config_result = receive_device_config(json_data)

        # Consolidate and return response
        return {
            "status": "success",
            "telemetry_result": device_config_result,
        }

    except Exception as e:
        frappe.log_error(message=str(e), title="Read Data Error")
        return {"status": "error", "message": str(e)}


# ===========================================================
# Function: receive_device_config
# -------------------------------
# Parses and stores latest telemetry and read-only config data
# from a device. Updates existing "Device Config" or creates new.
# Input: JSON payload with device_key and telemetry data
# Output: Status message after save operation
# ===========================================================
def receive_device_config(json_data):
    try:
        # Define IST timezone
        ist = timezone("Asia/Kolkata")

        # Extract device details
        device_key = json_data.get("device_key")
        device = frappe.get_doc("Device", {"device_key": device_key})
        data = json_data.get("data")

        telemetry_data = {}
        desc_data = {}

        # Check if existing config record exists
        parent_doc_name = frappe.db.get_value(
            "Device Config",
            {"device_id": device.name},
            "name"
        )

        # Load existing or create new config doc
        if parent_doc_name:
            telemetry_doc = frappe.get_doc("Device Config", parent_doc_name)
        else:
            telemetry_doc = frappe.get_doc({
                "doctype": "Device Config",
                "device_id": device.name,
                "device_config_parameters": [],
                "device_desc_parameters": [],
            })

        # Process telemetry records from payload
        for record in data:
            ts = record.get("ts")
            timestamp = datetime.fromtimestamp(ts / 1000.0).astimezone(ist).replace(tzinfo=None)

            # Process read-only configuration values
            read_only_values = record.get("read_only_values", {})
            for key, value in read_only_values.items():
                if key not in desc_data or ts > desc_data[key]["ts"]:
                    desc_data[key] = {"ts": ts, "timestamp": timestamp, "value": value}

            # Process regular config/telemetry values
            values = record.get("values", {})
            formatted_values = format_field_names(values)
            for key, value in formatted_values.items():
                if key not in telemetry_data or ts > telemetry_data[key]["ts"]:
                    telemetry_data[key] = {"ts": ts, "timestamp": timestamp, "value": value}

        # Convert telemetry_data dict to list of dicts
        updated_telemetry_data = []
        for key, entry in telemetry_data.items():
            updated_telemetry_data.append({
                "timestamp": datetime.fromtimestamp(entry["ts"] / 1000.0).astimezone(ist).replace(tzinfo=None),
                "key": key,
                "value": entry["value"],
            })

        # Convert desc_data dict to list of dicts
        updated_desc_data = []
        for key, entry in desc_data.items():
            updated_desc_data.append({
                "timestamp": datetime.fromtimestamp(entry["ts"] / 1000.0).astimezone(ist).replace(tzinfo=None),
                "key": key,
                "value": entry["value"],
            })

        # Clear existing and append new config values
        telemetry_doc.device_config_parameters = []
        for entry in updated_telemetry_data:
            telemetry_doc.append("device_config_parameters", entry)

        telemetry_doc.device_desc_parameters = []
        for entry in updated_desc_data:
            telemetry_doc.append("device_desc_parameters", entry)

        # Save and commit
        telemetry_doc.save(ignore_permissions=True)
        frappe.db.commit()

        return {"status": "success", "message": "Device Configuration data recorded successfully"}

    except Exception as e:
        frappe.log_error(message=str(e), title="Device Configuration Data Processing Error")
        return {"status": "error", "message": str(e)}


# ===========================================================
# Helper Function: format_field_names
# -------------------------------
# Currently returns data unchanged; can be modified to normalize keys.
# Input: dict of values
# Output: same dict or formatted keys if needed
# ===========================================================
def format_field_names(values):
    formatted_values = {}
    for key, value in values.items():
        formatted_values[key] = value  
    return formatted_values


# ===========================================================
# Helper Function: safe_log_error
# -------------------------------
# Gracefully logs an error using frappe.log_error, with fallback
# ===========================================================
def safe_log_error(title, message):
    try:
        frappe.log_error(title=title, message=message)
    except Exception as e:
        frappe.log_error(title="Error in safe_log_error", message=str(e))


# ===========================================================
# API Endpoint: process_new_config_handle_request
# -------------------------------
# Handles device handshake request:
# - Sends config or OTA files if needed
# - Accepts ACKs and updates flags
# Input: JSON payload with flags and device_key
# Output: Response JSON with config/OTA/acknowledgment
# ===========================================================
# @frappe.whitelist(allow_guest=True)
# def process_new_config_handle_request():
#     try:
#         json_data = frappe.request.json

#         # Extract fields and flags from input
#         device_key = json_data.get('device_key')
#         is_config = int(json_data.get('is_config') or 0)
#         is_ota = int(json_data.get('is_ota') or 0)
#         ack = int(json_data.get('ACK') or 0)
#         cack = int(json_data.get('CACK') or 0)
#         oack = int(json_data.get('OACK') or 0)

#         # Sanitize device ID
#         device_id = device_key.replace("LSPL_", "", 1) if device_key and device_key.startswith("LSPL_") else device_key

#         # Check device in database
#         existing_device_id_in_device_config = frappe.db.exists('Device Config', {'device_id': device_id})
#         if not existing_device_id_in_device_config:
#             return {"message": "Device not found"}

#         device_doc = frappe.get_doc('Device Config', existing_device_id_in_device_config)

#         # Update acknowledgment flags
#         if cack == 1:
#             device_doc.is_new_config = 0
#             device_doc.acknowledge = 1
#         if oack == 1:
#             device_doc.is_new_ota = 0
#             device_doc.otaacknowledge = 1
#         if cack == 1 and oack == 1:
#             device_doc.is_new_config = 0
#             device_doc.is_new_ota = 0
#             device_doc.acknowledge = 1
#             device_doc.otaacknowledge = 1

#         device_doc.save(ignore_permissions=True)

#         # If nothing is to be sent, return blank
#         if not device_doc.is_new_config and not device_doc.is_new_ota:
#             return {}

#         # Prepare response
#         response_data = {
#             "device_key": device_key,
#             "name": device_doc.device_id,
#         }

#         # Add config parameters if required
#         if is_config == 1 and device_doc.is_new_config == 1:
#             values = {p.key: p.value for p in device_doc.device_config_parameters}
#             response_data["data"] = [{"values": values}]

#         # Handle OTA file and URL generation
#         if is_ota == 1 and device_doc.is_new_ota == 1:
#             ota_file_reference = device_doc.attach_yybs
#             if ota_file_reference:
#                 try:
#                     base_url = frappe.utils.get_url().replace("iotweet.cloud", "iotweet.io")
#                     ota_file_path = frappe.get_site_path("public", ota_file_reference.strip("/"))

#                     file_urls = []

#                     with tempfile.TemporaryDirectory() as temp_dir:
#                         if zipfile.is_zipfile(ota_file_path):
#                             with zipfile.ZipFile(ota_file_path, 'r') as zip_ref:
#                                 zip_ref.extractall(temp_dir)

#                             # Move all files to public and log
#                             for root, dirs, files in os.walk(temp_dir):
#                                 for file_name in files:
#                                     file_path = os.path.join(root, file_name)
#                                     if os.path.isfile(file_path):
#                                         target_path = frappe.get_site_path("public", "files", file_name)
#                                         try:
#                                             shutil.move(file_path, target_path)
#                                             file_urls.append(f"{base_url}/files/{file_name}")
#                                             safe_log_error("OTA File Extracted", f"Extracted file: {file_name}")
#                                         except Exception as move_error:
#                                             safe_log_error("File move error", str(move_error))

#                             if file_urls:
#                                 response_data["ota_file_url"] = file_urls
#                             else:
#                                 response_data["ota_message"] = "No files found in OTA archive."
#                         else:
#                             file_url = f"{base_url}/files/{os.path.basename(ota_file_path)}"
#                             response_data["ota_file_url"] = file_url
#                 except Exception as e:
#                     safe_log_error("OTA extract error", str(e))
#                     response_data["ota_message"] = "Failed to extract OTA files."
#             else:
#                 response_data["ota_message"] = "No OTA file is attached to this device."

#             # Add version label
#             response_data["device_version"] = frappe.db.get_value("OTA Version", device_doc.device_version, "ota_label") or device_doc.device_version

#         # Add acknowledgment message if needed
#         if ack == 1:
#             response_data["acknowledgment"] = "Acknowledgment received for the device."

#         return response_data

#     except Exception as e:
#         safe_log_error("process_new_config_handle_request error", str(e))
#         return {"message": "An error occurred while processing the request."}


@frappe.whitelist(allow_guest=True)
def process_new_config_handle_request():
    try:
        json_data = frappe.request.json

        # Extract fields and flags from input (UNCHANGED + NEW SSL)
        device_key = json_data.get('device_key')
        is_config = int(json_data.get('is_config') or 0)
        is_ota = int(json_data.get('is_ota') or 0)
        is_ssl = int(json_data.get('is_ssl') or 0)             # NEW
        ack = int(json_data.get('ACK') or 0)
        cack = int(json_data.get('CACK') or 0)
        oack = int(json_data.get('OACK') or 0)
        sack = int(json_data.get('SACK') or 0)                 # NEW

        # Sanitize device ID (UNCHANGED)
        device_id = device_key.replace("LSPL_", "", 1) if device_key and device_key.startswith("LSPL_") else device_key

        # Check device (UNCHANGED)
        existing_device_id_in_device_config = frappe.db.exists('Device Config', {'device_id': device_id})
        if not existing_device_id_in_device_config:
            return {"message": "Device not found"}

        device_doc = frappe.get_doc('Device Config', existing_device_id_in_device_config)

        # Update acknowledgment flags (UNCHANGED + SSL)
        if cack == 1:
            device_doc.is_new_config = 0
            device_doc.acknowledge = 1
        if oack == 1:
            device_doc.is_new_ota = 0
            device_doc.otaacknowledge = 1
        if sack == 1:  # NEW
            device_doc.is_new_ssl = 0
            device_doc.sslacknowledge = 1

        # Keep your combined-set block, and add a triple-all block for completeness (NEW)
        if cack == 1 and oack == 1:
            device_doc.is_new_config = 0
            device_doc.is_new_ota = 0
            device_doc.acknowledge = 1
            device_doc.otaacknowledge = 1
        if cack == 1 and oack == 1 and sack == 1:  # NEW
            device_doc.is_new_config = 0
            device_doc.is_new_ota = 0
            device_doc.is_new_ssl = 0
            device_doc.acknowledge = 1
            device_doc.otaacknowledge = 1
            device_doc.sslacknowledge = 1

        device_doc.save(ignore_permissions=True)

        # If nothing is to be sent, return blank (EXTENDED WITH SSL)
        if not device_doc.is_new_config and not device_doc.is_new_ota and not getattr(device_doc, "is_new_ssl", 0):
            return {}

        # Prepare response (UNCHANGED)
        response_data = {
            "device_key": device_key,
            "name": device_doc.device_id,
        }

        # CONFIG payload (UNCHANGED)
        if is_config == 1 and device_doc.is_new_config == 1:
            values = {p.key: p.value for p in device_doc.device_config_parameters}
            response_data["data"] = [{"values": values}]

        # OTA payload (UNCHANGED)
        if is_ota == 1 and device_doc.is_new_ota == 1:
            ota_file_reference = device_doc.attach_yybs
            if ota_file_reference:
                try:
                    base_url = frappe.utils.get_url().replace("iotweet.cloud", "iotweet.io")
                    ota_file_path = frappe.get_site_path("public", ota_file_reference.strip("/"))

                    file_urls = []

                    with tempfile.TemporaryDirectory() as temp_dir:
                        if zipfile.is_zipfile(ota_file_path):
                            with zipfile.ZipFile(ota_file_path, 'r') as zip_ref:
                                zip_ref.extractall(temp_dir)

                            for root, dirs, files in os.walk(temp_dir):
                                for file_name in files:
                                    file_path = os.path.join(root, file_name)
                                    if os.path.isfile(file_path):
                                        target_path = frappe.get_site_path("public", "files", file_name)
                                        try:
                                            shutil.move(file_path, target_path)
                                            file_urls.append(f"{base_url}/files/{file_name}")
                                            safe_log_error("OTA File Extracted", f"Extracted file: {file_name}")
                                        except Exception as move_error:
                                            safe_log_error("File move error", str(move_error))

                            if file_urls:
                                response_data["ota_file_url"] = file_urls
                            else:
                                response_data["ota_message"] = "No files found in OTA archive."
                        else:
                            file_url = f"{base_url}/files/{os.path.basename(ota_file_path)}"
                            response_data["ota_file_url"] = file_url
                except Exception as e:
                    safe_log_error("OTA extract error", str(e))
                    response_data["ota_message"] = "Failed to extract OTA files."
            else:
                response_data["ota_message"] = "No OTA file is attached to this device."

        # SSL payload (NEW, mirrors OTA logic but uses attach_ssl and ota_ssl_file_url)
        if is_ssl == 1 and getattr(device_doc, "is_new_ssl", 0) == 1:
            ssl_file_reference = getattr(device_doc, "attach_ssl", None)
            if ssl_file_reference:
                try:
                    base_url = frappe.utils.get_url().replace("iotweet.cloud", "iotweet.io")
                    ssl_file_path = frappe.get_site_path("public", ssl_file_reference.strip("/"))

                    ssl_file_urls = []

                    with tempfile.TemporaryDirectory() as temp_dir:
                        if zipfile.is_zipfile(ssl_file_path):
                            with zipfile.ZipFile(ssl_file_path, 'r') as zip_ref:
                                zip_ref.extractall(temp_dir)

                            for root, dirs, files in os.walk(temp_dir):
                                for file_name in files:
                                    file_path = os.path.join(root, file_name)
                                    if os.path.isfile(file_path):
                                        target_path = frappe.get_site_path("public", "files", file_name)
                                        try:
                                            shutil.move(file_path, target_path)
                                            ssl_file_urls.append(f"{base_url}/files/{file_name}")
                                            safe_log_error("SSL File Extracted", f"Extracted file: {file_name}")
                                        except Exception as move_error:
                                            safe_log_error("SSL file move error", str(move_error))

                            if ssl_file_urls:
                                response_data["ota_ssl_file_url"] = ssl_file_urls
                            else:
                                response_data["ota_ssl_message"] = "No files found in SSL archive."
                        else:
                            file_url = f"{base_url}/files/{os.path.basename(ssl_file_path)}"
                            response_data["ota_ssl_file_url"] = file_url
                except Exception as e:
                    safe_log_error("SSL extract error", str(e))
                    response_data["ota_ssl_message"] = "Failed to extract SSL files."
            else:
                response_data["ota_ssl_message"] = "No SSL file is attached to this device."

        # Version label: ensure it's present even for SSL-only (NEW fallback)
        if "device_version" not in response_data:
            response_data["device_version"] = (
                frappe.db.get_value("OTA Version", device_doc.device_version, "ota_label")
                or device_doc.device_version
            )

        # Optional general acknowledgment message (UNCHANGED)
        if ack == 1:
            response_data["acknowledgment"] = "Acknowledgment received for the device."

        return response_data

    except Exception as e:
        safe_log_error("process_new_config_handle_request error", str(e))
        return {"message": "An error occurred while processing the request."}
