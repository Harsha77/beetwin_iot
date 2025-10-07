import frappe
from datetime import datetime
from pytz import timezone  # Import timezone for IST conversion
 
 
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
   
# ****************************************************************************************************************************
           
            #The code below does not filter out future datetime data when retrieving it from a JSON string for receive_telemetry
            ##Modified DateTime is :- 31-03-2025 11:30:00
 
# ****************************************************************************************************************************
 
def receive_telemetry(json_data):
    try:
        # Define IST timezone
        ist = timezone("Asia/Kolkata")
 
        # Validate and process telemetry data
        device_key = json_data.get("device_key")
        device = frappe.get_doc("Device", {"device_key": device_key})
        data = json_data.get("data")
 
        telemetry_data = {}
 
        # Process existing telemetry data if it exists
        parent_doc_name = frappe.db.get_value(
            "Device Telemetry",
            {"device_id": device.name},
            "name"
        )
 
        if parent_doc_name:
            telemetry_doc = frappe.get_doc("Device Telemetry", parent_doc_name)
            # Load existing data into telemetry_data
            for entry in telemetry_doc.device_telemetry_data:
                key = entry.key
                timestamp = int(entry.timestamp.timestamp())  # Convert to ms
               
                value = entry.value
                # Retain only the latest timestamp for each key
                if key not in telemetry_data or timestamp > telemetry_data[key]["ts"]:
                    telemetry_data[key] = {"ts": timestamp, "value": value}
        else:
            telemetry_doc = frappe.get_doc({
                "doctype": "Device Telemetry",
                "device_id": device.name,
                "device_telemetry_data": [],
            })
 
        # Process incoming telemetry data
        for record in data:
            ts = record.get("ts")
            timestamp = datetime.fromtimestamp(ts / 1000.0).astimezone(ist).replace(tzinfo=None)  # Remove timezone info
            values = record.get("values", {})
            formatted_values = format_field_names(values)
 
            # Remove IM field if it exists in the formatted values
            formatted_values.pop("im", None)
 
            for key, value in formatted_values.items():
                # Update the key only if the timestamp is newer
                if key not in telemetry_data or ts > telemetry_data[key]["ts"]:
                    telemetry_data[key] = {"ts": ts, "timestamp": timestamp, "value": value}
 
        # Flatten telemetry_data for saving
        updated_telemetry_data = []
        for key, entry in telemetry_data.items():
            updated_telemetry_data.append({
                "timestamp": datetime.fromtimestamp(entry["ts"] / 1000.0).astimezone(ist).replace(tzinfo=None),  # Remove timezone info
                "key": key,
                "value": entry["value"],
            })
 
        # Clear existing telemetry data and append the updated list
        telemetry_doc.device_telemetry_data = []
        for entry in updated_telemetry_data:
            telemetry_doc.append("device_telemetry_data", entry)
 
        # Store the current timestamp in "DatTime" field
        telemetry_doc.datetime = datetime.now(timezone("Asia/Kolkata")).replace(tzinfo=None)
 
        telemetry_doc.save()
        frappe.db.commit()
 
        return {"status": "success", "message": "Telemetry data recorded successfully"}
 
    except Exception as e:
        frappe.log_error(message=str(e), title="Telemetry Processing Error")
        return {"status": "error", "message": str(e)}
    
    
    
# def receive_telemetry(json_data):

# # ****************************************************************************************************************************
            
#             #The below code is filter out future datetime data when retrieving it from a JSON string for receive_telemetry
#             #Modified DateTime is :- 31-03-2025 11:30:00
                        
# # ****************************************************************************************************************************

#     try:
#         # Define IST timezone
#         ist = timezone("Asia/Kolkata")

#         # Validate and process telemetry data
#         device_key = json_data.get("device_key")
#         device = frappe.get_doc("Device", {"device_key": device_key})
#         data = json_data.get("data")

#         telemetry_data = {}

#         # Process existing telemetry data if it exists
#         parent_doc_name = frappe.db.get_value(
#             "Device Telemetry",
#             {"device_id": device.name},
#             "name"
#         )

#         if parent_doc_name:
#             telemetry_doc = frappe.get_doc("Device Telemetry", parent_doc_name)
#             # Load existing data into telemetry_data
#             for entry in telemetry_doc.device_telemetry_data:
#                 key = entry.key
#                 timestamp = int(entry.timestamp.timestamp())  # Convert to ms
                
#                 value = entry.value
#                 # Retain only the latest timestamp for each key
#                 if key not in telemetry_data or timestamp > telemetry_data[key]["ts"]:
#                     telemetry_data[key] = {"ts": timestamp, "value": value}
#         else:
#             telemetry_doc = frappe.get_doc({
#                 "doctype": "Device Telemetry",
#                 "device_id": device.name,
#                 "device_telemetry_data": [],
#             })

#         # Process incoming telemetry data
#         for record in data:
#             ts = record.get("ts")
#             timestamp = datetime.fromtimestamp(ts / 1000.0).astimezone(ist).replace(tzinfo=None)  # Remove timezone info
            
#             # Get current datetime in IST without timezone info
#             current_time = datetime.now(timezone("Asia/Kolkata")).replace(tzinfo=None)

#             # Skip processing if timestamp is in the future
#             if timestamp > current_time:
#                 continue

#             values = record.get("values", {})
#             formatted_values = format_field_names(values)

#             # Remove IM field if it exists in the formatted values
#             formatted_values.pop("im", None)

#             for key, value in formatted_values.items():
#                 # Update the key only if the timestamp is newer
#                 if key not in telemetry_data or ts > telemetry_data[key]["ts"]:
#                     telemetry_data[key] = {"ts": ts, "timestamp": timestamp, "value": value}

#         # Flatten telemetry_data for saving
#         updated_telemetry_data = []
#         for key, entry in telemetry_data.items():
#             updated_telemetry_data.append({
#                 "timestamp": datetime.fromtimestamp(entry["ts"] / 1000.0).astimezone(ist).replace(tzinfo=None),  # Remove timezone info
#                 "key": key,
#                 "value": entry["value"],
#             })

#         # Clear existing telemetry data and append the updated list
#         telemetry_doc.device_telemetry_data = []
#         for entry in updated_telemetry_data:
#             telemetry_doc.append("device_telemetry_data", entry)

#         # Store the current timestamp in "DatTime" field
#         telemetry_doc.datetime = datetime.now(timezone("Asia/Kolkata")).replace(tzinfo=None)

#         telemetry_doc.save()
#         frappe.db.commit()

#         return {"status": "success", "message": "Telemetry data recorded successfully"}

#     except Exception as e:
#         frappe.log_error(message=str(e), title="Telemetry Processing Error")
#         return {"status": "error", "message": str(e)}



# ****************************************************************************************************************************
            
            #The code below does not filter out future datetime data when retrieving it from a JSON string for receive_reading
            ##Modified DateTime is :- 31-03-2025 11:30:00

# ****************************************************************************************************************************


def receive_reading(json_data):
    try:
        # Define IST timezone
        ist = timezone("Asia/Kolkata")

        # Validate and process reading data
        device_key = json_data.get('device_key')
        device = frappe.get_doc("Device", {"device_key": device_key})
        data = json_data.get('data')

        for record in data:
            timestamp = datetime.fromtimestamp(record["ts"] / 1000.0).astimezone(ist).replace(tzinfo=None)  # Remove timezone info
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



# def receive_reading(json_data):

# # ****************************************************************************************************************************
            
#             #The below code is filter out future datetime data when retrieving it from a JSON string for receive_reading
#             ##Modified DateTime is :- 31-03-2025 11:30:00
                        
# # ****************************************************************************************************************************

#     try:
#         # Define IST timezone
#         ist = timezone("Asia/Kolkata")

#         # Validate and process reading data
#         device_key = json_data.get('device_key')
#         device = frappe.get_doc("Device", {"device_key": device_key})
#         data = json_data.get('data')

#         for record in data:
#             timestamp = datetime.fromtimestamp(record["ts"] / 1000.0).astimezone(ist).replace(tzinfo=None)  # Remove timezone info
            
#             # Get current datetime in IST without timezone info
#             current_time = datetime.now(timezone("Asia/Kolkata")).replace(tzinfo=None)

#             # Skip processing if timestamp is in the future
#             if timestamp > current_time:
#                 continue

#             values = record.get("values", {})

#             # Always create a new "Device Reading" document
#             device_reading_doc = frappe.get_doc({
#                 "doctype": "Device Reading",
#                 "device_id": device.name,
#                 "timestamp": timestamp,
#             })
#             device_reading_doc.insert(ignore_permissions=True)

#             for key, value in values.items():
#                 # Always append new key-value pairs
#                 device_reading_doc.append("reading", {
#                     "key": key,
#                     "value": value
#                 })

#             device_reading_doc.save()

#         frappe.db.commit()
#         return {"status": "success", "message": "Reading data recorded successfully"}

#     except Exception as e:
#         frappe.log_error(message=str(e), title="Reading Processing Error")
#         return {"status": "error", "message": str(e)}


def format_field_names(values):
    """Format field names to ensure they are valid for Frappe and match the JSON data keys."""
    formatted_values = {}
    for key, value in values.items():
        formatted_key = key.replace("-", "_")  # Replace hyphen with underscore and lowercase
        formatted_values[formatted_key] = value
    return formatted_values


