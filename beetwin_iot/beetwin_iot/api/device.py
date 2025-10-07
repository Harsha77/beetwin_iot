import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_device_categories_and_groups():
    # Fetch Device Categories
    device_categories = frappe.get_all("Device Category", 
        fields=["name", "device_category"])
    
    # Fetch Device Groups
    device_groups = frappe.get_all("Device Group", 
        fields=["name", "group_name"])
    
    return {
        "device_categories": device_categories,
        "device_groups": device_groups
    }
