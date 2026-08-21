import frappe
import time
from frappe.utils import now_datetime


# ===========================================================
# Function: get_epoch_datetime
# -----------------------------------------------------------
# Description:
#     API endpoint to fetch the current date and time in two formats:
#     1. Epoch time in milliseconds.
#     2. Human-readable formatted datetime string.
# 
#     This is triggered only when the input JSON contains:
#     {
#         "values": {
#             "EPOCH": "Get_Epoch"
#         }
#     }
# 
# Notes:
#     - The function sets the response directly via frappe.response to
#       prevent automatic API wrapping.
#     - If the input format is incorrect or an exception occurs,
#       an appropriate error is returned.
# ===========================================================
@frappe.whitelist(allow_guest=True)
def get_epoch_datetime():
    """
    API to return the current datetime in epoch (milliseconds) and formatted string
    when the request contains {"values": {"EPOCH": "Get_Epoch"}}
    """
    try:
        # Parse the request JSON
        request_data = frappe.request.json
        values = request_data.get("values", {})

        # Check if the request contains the expected key and value
        if values.get("EPOCH") != "Get_Epoch":
            frappe.response["error"] = "Invalid request format."
            return

        # Get the current epoch time in milliseconds
        current_epoch_ms = int(time.time() * 1000)  # Epoch in milliseconds
        current_datetime = now_datetime().strftime("%Y-%m-%d %H:%M:%S")  # Formatted datetime

        # Set response directly in frappe.response to avoid automatic wrapping
        frappe.response["timestamp_epoch"] = current_epoch_ms
        frappe.response["timestamp_formatted"] = current_datetime

    except Exception as e:
        # Log the full traceback in case of an error and return error response
        frappe.log_error(frappe.get_traceback(), "Get Epoch DateTime Error")
        frappe.response["error"] = str(e)
