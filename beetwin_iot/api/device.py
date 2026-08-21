# ============================================================
# Module: Device Metadata API
# Description:
#     This script provides a public API endpoint to retrieve
#     metadata such as Device Categories and Device Groups.
#     It can be consumed by client applications that need to 
#     populate dropdowns or filters based on these values.
#
# Function Summary:
# ------------------------------------------------------------
# 1. get_device_categories_and_groups():
#    - Type: Public API (whitelisted for guest)
#    - Purpose: Fetch and return all available device categories
#               and device groups from their respective DocTypes.
#    - Returns: Dictionary containing two lists:
#         • device_categories → [{"name": ..., "device_category": ...}, ...]
#         • device_groups     → [{"name": ..., "group_name": ...}, ...]
# ============================================================

import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_device_categories_and_groups():
    """
    API Endpoint: get_device_categories_and_groups
    ------------------------------------------------
    Publicly accessible function (guest access allowed) that 
    fetches:
      - All entries from the "Device Category" DocType with fields:
          * name
          * device_category
      - All entries from the "Device Group" DocType with fields:
          * name
          * group_name

    Returns:
        dict: {
            "device_categories": [...],
            "device_groups": [...]
        }
    """
    
    # Fetch Device Categories from the "Device Category" DocType
    device_categories = frappe.get_all("Device Category", 
        fields=["name", "device_category"])
    
    # Fetch Device Groups from the "Device Group" DocType
    device_groups = frappe.get_all("Device Group", 
        fields=["name", "group_name"])
    
    # Return the structured response with both lists
    return {
        "device_categories": device_categories,
        "device_groups": device_groups
    }
