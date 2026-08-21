import frappe
from frappe.utils.password import get_decrypted_password

# ------------------------------
# Function: get_device_details
# ------------------------------
# Description:
#    API endpoint to retrieve device credentials (IMEI, API Key, and decrypted API Secret)
#    from the 'Device' DocType using the provided IMEI number.
#
# Key Features:
# - Accepts a JSON request with the IMEI number under `values.IM`
# - Checks if `is_set_keys` is enabled before returning credentials
# - Optionally resets `is_set_keys` to 0 and sets `ack` to 1 if `DACK` is 1
# - Logs any exceptions that occur during the operation
#
# Input JSON Payload Example:
# {
#    "ts":1734348733000,
#    "values":{
#        "IM":"708672027065418",
#         "DACK":0
#    }
#}
#
# Output Example (on success):


# {
#     "message": {
#         "imei_number": "708672027065418",
#         "api_key": "1JkgfDUWeIf4Cjv",
#         "api_secret": "AL6skbXFOqWWqTi"
#     }
# }

#
# Output Example (on error):
# {
#   "error": "Device not found for the given IMEI number."
# }
#
# Note:
# - `allow_guest=True` allows this API to be accessed without authentication
# - No core logic is modified per user request; only comments added
@frappe.whitelist(allow_guest=True)
def get_device_details():
    """
    API to fetch IMEI Number, API Key, and decrypted API Secret from the Device DocType.
    Does not provide a response if `is_set_keys` is 0.
    After sending the response, the `is_set_keys` field will be unchecked if `DACK` is 1.
    :return: JSON object with IMEI Number, API Key, and API Secret
    """
    try:
        # Parse the incoming JSON request body
        request_data = frappe.request.json

        # Extract the 'values' dictionary from the request
        values = request_data.get("values", {})

        # Retrieve IMEI number and DACK flag from the request
        imei_number = values.get("IM")
        dack = values.get("DACK", None)  # Optional field, defaults to None

        # Ensure IMEI number is provided
        if not imei_number:
            frappe.throw("IMEI Number is required.")

        # Fetch the Device document based on IMEI number
        device = frappe.get_doc("Device", {"imei_number": imei_number})

        # Check if device was found
        if not device:
            return {"error": "Device not found for the given IMEI number."}

        # Do not return API credentials if 'is_set_keys' is not enabled
        if not device.is_set_keys:
            return {"error": "Access denied. 'is_set_keys' is not set."}

        # Decrypt the API secret using frappe's password utility
        decrypted_api_secret = get_decrypted_password("Device", device.name, fieldname="api_secret")

        # Construct response payload
        response = {
            "imei_number": device.imei_number,
            "api_key": device.api_key,
            "api_secret": decrypted_api_secret
        }

        # If DACK is set to 1, reset 'is_set_keys' and acknowledge
        if dack == 1:
            device.db_set('is_set_keys', 0)  # Reset is_set_keys to false
            device.db_set('ack', 1)          # Mark acknowledgment
            frappe.db.commit()               # Persist changes to DB

        # Return the final response with credentials
        return response

    except Exception as e:
        # Log the error with traceback in Frappe Error Logs
        frappe.log_error(frappe.get_traceback(), "Get Device Details Error")
        # Return a generic error response
        return {"error": str(e)}
