
import frappe
import base64
from frappe.exceptions import AuthenticationError

class CustomAuthenticationError(AuthenticationError):
    pass






def validate_api_key_secret(*args, **kwargs):
    """Validate API Key and Secret for a device in the Beetwin_Devices doctype."""
    
    # Get the current request path
    current_route = frappe.request.path
    
    # Define the specific API routes that should use custom authentication
    custom_auth_routes = [
        "/api/method/beetwin_iot.beetwin_iot.api.device_config.device_config",
        "/api/method/beetwin_iot.beetwin_iot.api.read_data.read_data",
        "/api/method/beetwin_iot.beetwin_iot.api.device_config.process_new_config_handle_request",
        "/api/method/beetwin_iot.beetwin_iot.api.get_user_devices.get_user_devices"
        "/api/method/beetwin_iot.beetwin_iot.api.get_device_config.get_device_config"
        "/api/method/beetwin_iot.beetwin_iot.api.get_latest_device_data_for_Production.get_filtered_device_data_for_production"
        "/api/method/beetwin_iot.beetwin_iot.api.changedpassword.admin_change_password"
        
        
 

    ]
    
    # Check if the current route requires custom authentication
    if current_route in custom_auth_routes:
        # Get the 'Authorization' header
        auth_header = frappe.request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Basic '):
            raise CustomAuthenticationError("Authorization header is missing or malformed.")

        # Extract the base64 encoded part of the header
        encoded_credentials = auth_header[len('Basic '):]
        
        try:
            # Decode the base64 string
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        except Exception:
            raise CustomAuthenticationError("Invalid Base64 encoding in Authorization header.")

        # Split credentials by ':'
        credentials = decoded_credentials.split(':', 1)

        if len(credentials) != 2:
            raise CustomAuthenticationError("Invalid Basic Auth credentials format.")

        api_key = credentials[0].strip()
        api_secret = credentials[1].strip()

        # Extracting IMEI from the JSON request body
        request_data = frappe.request.json
        imei = request_data.get('device_key')

        if not imei:
            raise CustomAuthenticationError("Device Key is missing from the request body.")

        # Retrieve the device document
        device_doc = frappe.db.exists('Device', {'api_key': api_key, 'device_key': imei})

        if not device_doc:
            raise CustomAuthenticationError("Invalid Device Key Number or Invalid API Key or Secret")

        # Decrypt the stored API secret
        decrypted_secret = frappe.get_doc('Device', device_doc).get_password('api_secret')
        
        if not decrypted_secret:
            raise frappe.AuthenticationError("No API Secret found for the provided API Key and IMEI Number")

        if api_secret != decrypted_secret:
            raise frappe.AuthenticationError("Invalid API Key or Secret")
        else:
            # Simulate removing the Authorization header by setting it to None in frappe.local.request context
            frappe.local.request.environ.pop('HTTP_AUTHORIZATION')

            # Simple print statements for logging to the console
            print(f"Request Path: {current_route}")
            print(f"Request Headers after modification: {dict(frappe.request.headers)}")
            print(f"Request Body: {request_data}")

            # Mark the user as a guest
            frappe.set_user('Guest')
            return True
    else:
        # For all other routes, continue with normal authentication
        return None


