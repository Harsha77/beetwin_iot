import frappe
from datetime import datetime
from pytz import timezone  # Import timezone for IST conversion



@frappe.whitelist(allow_guest=True)
def device_config():
    try:
        # Extract JSON payload
        json_data = frappe.request.json

        # Validate device key
        device_key = json_data.get('device_key')
        if not device_key:
            return {"status": "error", "message": "Device key is required"}

        # Call receive_device_config() function
        device_config_result = receive_device_config(json_data)

        # Consolidate results
        return {
            "status": "success",
            "telemetry_result": device_config_result,
        }

    except Exception as e:
        frappe.log_error(message=str(e), title="Read Data Error")
        return {"status": "error", "message": str(e)}


def receive_device_config(json_data):
    try:
        # Define IST timezone
        ist = timezone("Asia/Kolkata")

        # Validate and process telemetry data
        device_key = json_data.get("device_key")
        device = frappe.get_doc("Device", {"device_key": device_key})
        data = json_data.get("data")

        telemetry_data = {}
        desc_data = {}

        # Process existing telemetry data if it exists
        parent_doc_name = frappe.db.get_value(
            "Device Config",
            {"device_id": device.name},
            "name"
        )

        if parent_doc_name:
            telemetry_doc = frappe.get_doc("Device Config", parent_doc_name)
        else:
            telemetry_doc = frappe.get_doc({
                "doctype": "Device Config",
                "device_id": device.name,
                "device_config_parameters": [],
                "device_desc_parameters": [],
            })

        # Process incoming telemetry data
        for record in data:
            ts = record.get("ts")
            timestamp = datetime.fromtimestamp(ts / 1000.0).astimezone(ist).replace(tzinfo=None)  # Remove timezone info

            # Process `read_only_values`
            read_only_values = record.get("read_only_values", {})
            for key, value in read_only_values.items():
                if key not in desc_data or ts > desc_data[key]["ts"]:
                    desc_data[key] = {"ts": ts, "timestamp": timestamp, "value": value}

            # Process `values`
            values = record.get("values", {})
            formatted_values = format_field_names(values)

            for key, value in formatted_values.items():
                if key not in telemetry_data or ts > telemetry_data[key]["ts"]:
                    telemetry_data[key] = {"ts": ts, "timestamp": timestamp, "value": value}

        # Flatten telemetry_data for saving into `device_config_parameters`
        updated_telemetry_data = []
        for key, entry in telemetry_data.items():
            updated_telemetry_data.append({
                "timestamp": datetime.fromtimestamp(entry["ts"] / 1000.0).astimezone(ist).replace(tzinfo=None),
                "key": key,
                "value": entry["value"],
            })

        # Flatten desc_data for saving into `device_desc_parameters`
        updated_desc_data = []
        for key, entry in desc_data.items():
            updated_desc_data.append({
                "timestamp": datetime.fromtimestamp(entry["ts"] / 1000.0).astimezone(ist).replace(tzinfo=None),
                "key": key,
                "value": entry["value"],
            })

        # Clear and append updated telemetry data
        telemetry_doc.device_config_parameters = []
        for entry in updated_telemetry_data:
            telemetry_doc.append("device_config_parameters", entry)

        # Clear and append updated description data
        telemetry_doc.device_desc_parameters = []
        for entry in updated_desc_data:
            telemetry_doc.append("device_desc_parameters", entry)

        telemetry_doc.save(ignore_permissions=True)
        frappe.db.commit()

        return {"status": "success", "message": "Device Configuration data recorded successfully"}

    except Exception as e:
        frappe.log_error(message=str(e), title="Device Configuration Data Processing Error")
        return {"status": "error", "message": str(e)}


def format_field_names(values):
    """
    Format field names in the telemetry data if needed.
    You can modify this function based on specific formatting requirements.
    """
    formatted_values = {}
    for key, value in values.items():
        formatted_values[key] = value  
    return formatted_values


#########################  THIS Below IS THE NORMAL SINGLE FILE CODE #########################


# @frappe.whitelist(allow_guest=True)
# def process_new_config_handle_request():
#     try:
#         # Extract JSON payload from the request
#         json_data = frappe.request.json

#         # Extract device_key, is_config, is_ota, ACK, CACK, and OACK from JSON data
#         device_key = json_data.get('device_key')
#         is_config = json_data.get('is_config')
#         is_ota = json_data.get('is_ota')
#         ack = json_data.get('ACK')
#         cack = json_data.get('CACK')
#         oack = json_data.get('OACK')

#         # Convert to integers to avoid issues with string vs integer comparisons
#         is_config = int(is_config) if is_config is not None else 0
#         is_ota = int(is_ota) if is_ota is not None else 0
#         ack = int(ack) if ack is not None else 0
#         cack = int(cack) if cack is not None else 0
#         oack = int(oack) if oack is not None else 0

#         # Log received values for debugging purposes
#         frappe.log_error(f"Received values: device_key={device_key}, is_config={is_config}, is_ota={is_ota}, ack={ack}, cack={cack}, oack={oack}")

#         # Remove "LSPL_" prefix dynamically, if present
#         if device_key and device_key.startswith("LSPL_"):
#             device_id = device_key.replace("LSPL_", "", 1)  # Remove only the first occurrence of "LSPL_"
#         else:
#             device_id = device_key

#         # Check if the device exists in the 'Device Config' doctype
#         existing_device_id_in_device_config = frappe.db.exists(
#             'Device Config', {'device_id': device_id}
#         )

#         if existing_device_id_in_device_config:
#             # Fetch the device config document
#             device_doc = frappe.get_doc('Device Config', existing_device_id_in_device_config)

#             # Handle the CACK and OACK logic
#             if cack == 1:
#                 device_doc.is_new_config = 0  # Reset is_new_config to 0
#                 device_doc.acknowledge = 1   # Set acknowledge to 1

#             if oack == 1:
#                 device_doc.is_new_ota = 0  # Reset is_new_ota to 0
#                 device_doc.otaacknowledge = 1  # Set otaacknowledge to 1

#             if cack == 1 and oack == 1:
#                 device_doc.is_new_config = 0  # Reset is_new_config to 0
#                 device_doc.is_new_ota = 0    # Reset is_new_ota to 0
#                 device_doc.acknowledge = 1   # Set acknowledge to 1
#                 device_doc.otaacknowledge = 1  # Set otaacknowledge to 1

#             # Save the updated device document to reflect changes in the database
#             device_doc.save(ignore_permissions=True)

#             # Log the updated values for debugging
#             frappe.log_error(f"Updated device config for {device_id}: is_new_config={device_doc.is_new_config}, is_new_ota={device_doc.is_new_ota}, acknowledge={device_doc.acknowledge}, otaacknowledge={device_doc.otaacknowledge}")

#             # If neither is_new_config nor is_new_ota are selected, return a blank response
#             if not device_doc.is_new_config and not device_doc.is_new_ota:
#                 return {}

#             # Initialize the response data structure
#             response_data = {
#                 "device_key": device_key,  # Keep the original device_key
#                 "name": device_doc.device_id , # Use device_id as name
               
#             }

#             # Handle the 'is_new_config' scenario if selected in JSON
#             if is_config == 1 and device_doc.is_new_config == 1:
#                 values = {}
#                 for config_parameter in device_doc.device_config_parameters:
#                     values[config_parameter.key] = config_parameter.value

#                 response_data["data"] = [{
#                     "values": values,
#                 }]

#             # Handle the 'is_new_ota' scenario if selected in JSON
#             if is_ota == 1 and device_doc.is_new_ota == 1:
#                 ota_file_reference = device_doc.attach_yybs

#                 if ota_file_reference:
#                     base_url = frappe.utils.get_url()  # Get the base URL
#                     ota_file_url = base_url.replace("iotweet.cloud", "iotweet.io") + ota_file_reference
#                     response_data["ota_file_url"] = ota_file_url
                    
#                     # Add device_version using OTA label if available
#                     response_data["device_version"] = frappe.db.get_value("OTA Version", device_doc.device_version, "ota_label") or device_doc.device_version
                    
#                 else:
#                     response_data["ota_message"] = "No OTA file is attached to this device."

#             # If ACK is 1, include an acknowledgment message in the response
#             if ack == 1:
#                 response_data["acknowledgment"] = "Acknowledgment received for the device."

#             return response_data

#         # If device doesn't exist
#         return {
#             "message": "Device not found"
#         }

#     except Exception as e:
#         frappe.log_error(f"Error in process_new_config_handle_request: {str(e)}")
#         return {
#             "message": "An error occurred while processing the request."
#         }

#########################  THIS ABOVE IS THE NORMAL SINGLE FILE CODE #########################




#########################  THIS Below IS THE Multiple  FILE CODE using child docjtype method #########################



# @frappe.whitelist(allow_guest=True)
# def process_new_config_handle_request():
#     try:
#         json_data = frappe.request.json

#         device_key = json_data.get('device_key')
#         is_config = json_data.get('is_config')
#         is_ota = json_data.get('is_ota')
#         ack = json_data.get('ACK')
#         cack = json_data.get('CACK')
#         oack = json_data.get('OACK')

#         is_config = int(is_config) if is_config is not None else 0
#         is_ota = int(is_ota) if is_ota is not None else 0
#         ack = int(ack) if ack is not None else 0
#         cack = int(cack) if cack is not None else 0
#         oack = int(oack) if oack is not None else 0

#         frappe.log_error(f"Received values: device_key={device_key}, is_config={is_config}, is_ota={is_ota}, ack={ack}, cack={cack}, oack={oack}")

#         if device_key and device_key.startswith("LSPL_"):
#             device_id = device_key.replace("LSPL_", "", 1)
#         else:
#             device_id = device_key

#         existing_device_id_in_device_config = frappe.db.exists('Device Config', {'device_id': device_id})

#         if existing_device_id_in_device_config:
#             device_doc = frappe.get_doc('Device Config', existing_device_id_in_device_config)

#             if cack == 1:
#                 device_doc.is_new_config = 0
#                 device_doc.acknowledge = 1

#             if oack == 1:
#                 device_doc.is_new_ota = 0
#                 device_doc.otaacknowledge = 1

#             if cack == 1 and oack == 1:
#                 device_doc.is_new_config = 0
#                 device_doc.is_new_ota = 0
#                 device_doc.acknowledge = 1
#                 device_doc.otaacknowledge = 1

#             device_doc.save(ignore_permissions=True)

#             frappe.log_error(f"Updated device config for {device_id}: is_new_config={device_doc.is_new_config}, is_new_ota={device_doc.is_new_ota}, acknowledge={device_doc.acknowledge}, otaacknowledge={device_doc.otaacknowledge}")

#             if not device_doc.is_new_config and not device_doc.is_new_ota:
#                 return {}

#             response_data = {
#                 "device_key": device_key,
#                 "name": device_doc.device_id,
#             }

#             if is_config == 1 and device_doc.is_new_config == 1:
#                 values = {}
#                 for config_parameter in device_doc.device_config_parameters:
#                     values[config_parameter.key] = config_parameter.value

#                 response_data["data"] = [{
#                     "values": values,
#                 }]

#             if is_ota == 1 and device_doc.is_new_ota == 1:
#                 base_url = frappe.utils.get_url().replace("iotweet.cloud", "iotweet.io")
#                 ota_files = []

#                 for version_entry in device_doc.device_versions:
#                     if version_entry.firmware_file:
#                         full_url = base_url + version_entry.firmware_file
#                         ota_label = frappe.db.get_value("OTA Version", version_entry.device_version, "ota_label") or version_entry.device_version
#                         ota_files.append({
#                             "device_version": ota_label,
#                             "firmware_file_url": full_url
#                         })

#                 if len(ota_files) == 1:
#                     single = ota_files[0]
#                     ota_label_value = single.get("device_version")  # fix added here
#                     response_data["ota_file_url"] = single["firmware_file_url"]
#                     response_data["device_version"] = ota_label_value  # fix used here
#                 elif len(ota_files) > 1:
#                     response_data["ota_file_url"] = ota_files
#                 else:
#                     response_data["ota_message"] = "No OTA files are attached to this device."

#             if ack == 1:
#                 response_data["acknowledgment"] = "Acknowledgment received for the device."

#             return response_data

#         return {
#             "message": "Device not found"
#         }

#     except Exception as e:
#         frappe.log_error(f"Error in process_new_config_handle_request: {str(e)}")
#         return {
#             "message": "An error occurred while processing the request."
#         }


#########################  THIS Above IS THE Multiple  FILE CODE using child docjtype method #########################


#########################  THIS Below IS THE Multiple  FILE CODE using ZIP file method #########################


# import os
# import zipfile
# import tempfile
# import frappe

# @frappe.whitelist(allow_guest=True)
# def process_new_config_handle_request():
#     try:
#         # Extract JSON payload from the request
#         json_data = frappe.request.json

#         # Extract fields
#         device_key = json_data.get('device_key')
#         is_config = int(json_data.get('is_config') or 0)
#         is_ota = int(json_data.get('is_ota') or 0)
#         ack = int(json_data.get('ACK') or 0)
#         cack = int(json_data.get('CACK') or 0)
#         oack = int(json_data.get('OACK') or 0)

#         # Remove "LSPL_" prefix dynamically, if present
#         device_id = device_key.replace("LSPL_", "", 1) if device_key and device_key.startswith("LSPL_") else device_key

#         # Check if device exists
#         existing_device_id_in_device_config = frappe.db.exists('Device Config', {'device_id': device_id})
#         if not existing_device_id_in_device_config:
#             return {"message": "Device not found"}

#         # Fetch device doc
#         device_doc = frappe.get_doc('Device Config', existing_device_id_in_device_config)

#         # Handle ACK logic
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

#         # If nothing new, return blank
#         if not device_doc.is_new_config and not device_doc.is_new_ota:
#             return {}

#         # Build response
#         response_data = {
#             "device_key": device_key,
#             "name": device_doc.device_id,
#         }

#         # CONFIG data if needed
#         if is_config == 1 and device_doc.is_new_config == 1:
#             values = {p.key: p.value for p in device_doc.device_config_parameters}
#             response_data["data"] = [{"values": values}]

#         # OTA file handling
#         if is_ota == 1 and device_doc.is_new_ota == 1:
#             ota_file_reference = device_doc.attach_yybs
#             if ota_file_reference:
#                 try:
#                     base_url = frappe.utils.get_url().replace("iotweet.cloud", "iotweet.io")
#                     ota_file_path = frappe.get_site_path("public", ota_file_reference.strip("/"))

#                     file_urls = []

#                     # Extract into temporary directory
#                     with tempfile.TemporaryDirectory() as temp_dir:
#                         # ZIP extraction
#                         if zipfile.is_zipfile(ota_file_path):
#                             with zipfile.ZipFile(ota_file_path, 'r') as zip_ref:
#                                 zip_ref.extractall(temp_dir)
#                         else:
#                             frappe.log_error("OTA file is not a valid ZIP")
#                             response_data["ota_message"] = "OTA file is not a valid ZIP archive."
#                             return {"message": response_data}

#                         # Recursively find all files and move to public/files
#                         for root, dirs, files in os.walk(temp_dir):
#                             for file_name in files:
#                                 file_path = os.path.join(root, file_name)
#                                 if os.path.isfile(file_path):
#                                     target_path = frappe.get_site_path("public", "files", file_name)
#                                     os.rename(file_path, target_path)
#                                     file_urls.append(f"{base_url}/files/{file_name}")
#                                     frappe.log_error(f"Extracted file: {file_name}")

#                     if file_urls:
#                         response_data["ota_file_url"] = file_urls
#                     else:
#                         response_data["ota_message"] = "No files found in OTA archive."

#                 except Exception as e:
#                     frappe.log_error(f"OTA extract error: {str(e)}")
#                     response_data["ota_message"] = "Failed to extract OTA files."
#             else:
#                 response_data["ota_message"] = "No OTA file is attached to this device."

#             # Add version info
#             response_data["device_version"] = frappe.db.get_value("OTA Version", device_doc.device_version, "ota_label") or device_doc.device_version

#         # ACK message
#         if ack == 1:
#             response_data["acknowledgment"] = "Acknowledgment received for the device."

#         return {"message": response_data}

#     except Exception as e:
#         frappe.log_error(f"Error in process_new_config_handle_request: {str(e)}")
#         return {"message": "An error occurred while processing the request."}



# import os
# import shutil
# import zipfile
# import tempfile
# import frappe

# def safe_log_error(title, message):
#     try:
#         frappe.log_error(title=title, message=message)
#     except Exception as e:
#         frappe.log_error(title="Error in safe_log_error", message=str(e))

# @frappe.whitelist(allow_guest=True)
# def process_new_config_handle_request():
#     try:
#         # Extract JSON payload from the request
#         json_data = frappe.request.json

#         # Extract fields
#         device_key = json_data.get('device_key')
#         is_config = int(json_data.get('is_config') or 0)
#         is_ota = int(json_data.get('is_ota') or 0)
#         ack = int(json_data.get('ACK') or 0)
#         cack = int(json_data.get('CACK') or 0)
#         oack = int(json_data.get('OACK') or 0)

#         # Remove "LSPL_" prefix dynamically, if present
#         device_id = device_key.replace("LSPL_", "", 1) if device_key and device_key.startswith("LSPL_") else device_key

#         # Check if device exists
#         existing_device_id_in_device_config = frappe.db.exists('Device Config', {'device_id': device_id})
#         if not existing_device_id_in_device_config:
#             return {"message": "Device not found"}

#         # Fetch device doc
#         device_doc = frappe.get_doc('Device Config', existing_device_id_in_device_config)

#         # Handle ACK logic
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

#         # If nothing new, return blank
#         if not device_doc.is_new_config and not device_doc.is_new_ota:
#             return {}

#         # Build response
#         response_data = {
#             "device_key": device_key,
#             "name": device_doc.device_id,
#         }

#         # CONFIG data if needed
#         if is_config == 1 and device_doc.is_new_config == 1:
#             values = {p.key: p.value for p in device_doc.device_config_parameters}
#             response_data["data"] = [{"values": values}]

#         # OTA file handling
#         if is_ota == 1 and device_doc.is_new_ota == 1:
#             ota_file_reference = device_doc.attach_yybs
#             if ota_file_reference:
#                 try:
#                     base_url = frappe.utils.get_url().replace("iotweet.cloud", "iotweet.io")
#                     ota_file_path = frappe.get_site_path("public", ota_file_reference.strip("/"))

#                     file_urls = []

#                     # Extract into temporary directory
#                     with tempfile.TemporaryDirectory() as temp_dir:
#                         # ZIP extraction
#                         if zipfile.is_zipfile(ota_file_path):
#                             with zipfile.ZipFile(ota_file_path, 'r') as zip_ref:
#                                 zip_ref.extractall(temp_dir)
#                         else:
#                             safe_log_error("OTA extract error", "OTA file is not a valid ZIP archive.")
#                             response_data["ota_message"] = "OTA file is not a valid ZIP archive."
#                             return {"message": response_data}

#                         # Recursively find all files and move to public/files
#                         for root, dirs, files in os.walk(temp_dir):
#                             for file_name in files:
#                                 file_path = os.path.join(root, file_name)
#                                 if os.path.isfile(file_path):
#                                     target_path = frappe.get_site_path("public", "files", file_name)
#                                     try:
#                                         shutil.move(file_path, target_path)
#                                         file_urls.append(f"{base_url}/files/{file_name}")
#                                         safe_log_error("OTA File Extracted", f"Extracted file: {file_name}")
#                                     except Exception as move_error:
#                                         safe_log_error("File move error", str(move_error))

#                     if file_urls:
#                         response_data["ota_file_url"] = file_urls
#                     else:
#                         response_data["ota_message"] = "No files found in OTA archive."

#                 except Exception as e:
#                     safe_log_error("OTA extract error", str(e))
#                     response_data["ota_message"] = "Failed to extract OTA files."
#             else:
#                 response_data["ota_message"] = "No OTA file is attached to this device."

#             # Add version info
#             response_data["device_version"] = frappe.db.get_value("OTA Version", device_doc.device_version, "ota_label") or device_doc.device_version

#         # ACK message
#         if ack == 1:
#             response_data["acknowledgment"] = "Acknowledgment received for the device."

#         return {"message": response_data}

#     except Exception as e:
#         safe_log_error("process_new_config_handle_request error", str(e))
#         return {"message": "An error occurred while processing the request."}



import os
import shutil
import zipfile
import tempfile
import frappe

def safe_log_error(title, message):
    try:
        frappe.log_error(title=title, message=message)
    except Exception as e:
        frappe.log_error(title="Error in safe_log_error", message=str(e))

@frappe.whitelist(allow_guest=True)
def process_new_config_handle_request():
    try:
        # Extract JSON payload from the request
        json_data = frappe.request.json

        # Extract fields
        device_key = json_data.get('device_key')
        is_config = int(json_data.get('is_config') or 0)
        is_ota = int(json_data.get('is_ota') or 0)
        ack = int(json_data.get('ACK') or 0)
        cack = int(json_data.get('CACK') or 0)
        oack = int(json_data.get('OACK') or 0)

        # Remove "LSPL_" prefix dynamically, if present
        device_id = device_key.replace("LSPL_", "", 1) if device_key and device_key.startswith("LSPL_") else device_key

        # Check if device exists
        existing_device_id_in_device_config = frappe.db.exists('Device Config', {'device_id': device_id})
        if not existing_device_id_in_device_config:
            return {"message": "Device not found"}

        # Fetch device doc
        device_doc = frappe.get_doc('Device Config', existing_device_id_in_device_config)

        # Handle ACK logic
        if cack == 1:
            device_doc.is_new_config = 0
            device_doc.acknowledge = 1
        if oack == 1:
            device_doc.is_new_ota = 0
            device_doc.otaacknowledge = 1
        if cack == 1 and oack == 1:
            device_doc.is_new_config = 0
            device_doc.is_new_ota = 0
            device_doc.acknowledge = 1
            device_doc.otaacknowledge = 1

        device_doc.save(ignore_permissions=True)

        # If nothing new, return blank
        if not device_doc.is_new_config and not device_doc.is_new_ota:
            return {}

        # Build response
        response_data = {
            "device_key": device_key,
            "name": device_doc.device_id,
        }

        # CONFIG data if needed
        if is_config == 1 and device_doc.is_new_config == 1:
            values = {p.key: p.value for p in device_doc.device_config_parameters}
            response_data["data"] = [{"values": values}]

        # OTA file handling
        if is_ota == 1 and device_doc.is_new_ota == 1:
            ota_file_reference = device_doc.attach_yybs
            if ota_file_reference:
                try:
                    base_url = frappe.utils.get_url().replace("iotweet.cloud", "iotweet.io")
                    ota_file_path = frappe.get_site_path("public", ota_file_reference.strip("/"))

                    file_urls = []

                    # Extract into temporary directory
                    with tempfile.TemporaryDirectory() as temp_dir:
                        if zipfile.is_zipfile(ota_file_path):
                            with zipfile.ZipFile(ota_file_path, 'r') as zip_ref:
                                zip_ref.extractall(temp_dir)

                            # Recursively find all files and move to public/files
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
                            # If not a zip, treat as a single OTA file
                            file_url = f"{base_url}/files/{os.path.basename(ota_file_path)}"
                            response_data["ota_file_url"] = file_url

                except Exception as e:
                    safe_log_error("OTA extract error", str(e))
                    response_data["ota_message"] = "Failed to extract OTA files."
            else:
                response_data["ota_message"] = "No OTA file is attached to this device."

            # Add version info
            response_data["device_version"] = frappe.db.get_value("OTA Version", device_doc.device_version, "ota_label") or device_doc.device_version

        # ACK message
        if ack == 1:
            response_data["acknowledgment"] = "Acknowledgment received for the device."

        #return {"message": response_data}
        return response_data

    except Exception as e:
        safe_log_error("process_new_config_handle_request error", str(e))
        return {"message": "An error occurred while processing the request."}



#########################  THIS Above IS THE Multiple  FILE CODE using ZIP file method #########################