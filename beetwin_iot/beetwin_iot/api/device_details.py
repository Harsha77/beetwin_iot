# import frappe
# from frappe.utils.password import get_decrypted_password

# @frappe.whitelist(allow_guest=True)
# def get_device_details():
#     """
#     API to fetch IMEI Number, API Key, and decrypted API Secret from the Device DocType.
#     Does not provide a response if `is_set_keys` is 0.
#     After sending the response, the `is_set_keys` field will be unchecked.
#     :return: JSON object with IMEI Number, API Key, and API Secret
#     """
#     try:
#         # Parse the JSON payload
#         request_data = frappe.request.json
#         # Extract `values` and `IM` from the payload
#         values = request_data.get("values")
#         imei_number = values.get("IM") if values else None

#         if not imei_number:
#             frappe.throw(("IMEI Number is required."))

#         # Fetch the device record
#         device = frappe.get_doc("Device", {"imei_number": imei_number})

#         if not device:
#             return {"error": "Device not found for the given IMEI number."}

#         # Validation: Do not provide a response if `is_set_keys` is 0
#         if not device.is_set_keys:
#             return {"error": "Access denied. 'is_set_keys' is not set."}

#         # Decrypt the API Secret
#         decrypted_api_secret = get_decrypted_password("Device", device.name, fieldname="api_secret")

#         # Prepare the response
#         response = {
#             "imei_number": device.imei_number,
#             "api_key": device.api_key,
#             "api_secret": decrypted_api_secret
#         }

#         # After preparing the response, update `is_set_keys` to 0
#         device.db_set('is_set_keys', 0)
#         device.db_set('ack', 1)  # To ensure the change is saved in the database
#         frappe.db.commit()  # Ensure the change is saved in the database

#         return response

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Get Device Details Error")
#         return {"error": str(e)}


import frappe
from frappe.utils.password import get_decrypted_password


@frappe.whitelist(allow_guest=True)
def get_device_details():
    """
    API to fetch IMEI Number, API Key, and decrypted API Secret from the Device DocType.
    Does not provide a response if `is_set_keys` is 0.
    After sending the response, the `is_set_keys` field will be unchecked if `DACK` is 1.
    :return: JSON object with IMEI Number, API Key, and API Secret
    """
    try:
        # Parse the JSON payload
        request_data = frappe.request.json
        values = request_data.get("values", {})
        
        imei_number = values.get("IM")
        dack = values.get("DACK", None)  # Default to None if not present

        if not imei_number:
            frappe.throw("IMEI Number is required.")

        # Fetch the device record
        device = frappe.get_doc("Device", {"imei_number": imei_number})

        if not device:
            return {"error": "Device not found for the given IMEI number."}

        # Validation: Do not provide a response if `is_set_keys` is 0
        if not device.is_set_keys:
            return {"error": "Access denied. 'is_set_keys' is not set."}

        # Decrypt the API Secret
        decrypted_api_secret = get_decrypted_password("Device", device.name, fieldname="api_secret")

        # Prepare the response
        response = {
            "imei_number": device.imei_number,
            "api_key": device.api_key,
            "api_secret": decrypted_api_secret
        }

        # If `DACK` is explicitly provided and set to 1, update `is_set_keys` and `ack`
        if dack == 1:
            device.db_set('is_set_keys', 0)
            device.db_set('ack', 1)
            frappe.db.commit()  # Ensure changes are saved

        return  response  # Wrapped response inside "message"

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Device Details Error")
        return {"error": str(e)}
