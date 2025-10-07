import frappe
import time
from frappe.utils import now_datetime


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
        frappe.log_error(frappe.get_traceback(), "Get Epoch DateTime Error")
        frappe.response["error"] = str(e)
