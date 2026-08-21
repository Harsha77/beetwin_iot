import frappe

# =============================================================
# Function: get_device_config
# -------------------------------------------------------------
# Public API endpoint to fetch device configuration details.
# Specifically retrieves 'Device ID', 'SR', and 'MAC' fields 
# from the 'Device Config' and related 'Device Config Key-Value'
# child table.
#
# - Filters key-value pairs for 'SR' and 'MAC' only.
# - Aggregates data by device.
# - Orders the results by SR (converted to integer) in ascending order.
#
# Access: Guest Allowed
# Return: List of dictionaries with keys: 'Device ID', 'SR', 'MAC'
# =============================================================
@frappe.whitelist(allow_guest=True)
def get_device_config():
    """
    API to fetch Device Config with selected parameters (Device ID, SR, MAC),
    sorted by SR in ascending order.
    """
    # SQL query to fetch and transform data
    device_data = frappe.db.sql("""
        SELECT 
            dc.device_id AS `Device ID`,
            MAX(CASE WHEN dcp.key = 'SR' THEN dcp.value ELSE NULL END) AS `SR`,
            MAX(CASE WHEN dcp.key = 'MAC' THEN dcp.value ELSE NULL END) AS `MAC`
        FROM 
            `tabDevice Config` dc
        LEFT JOIN `tabDevice Config Key-Value` dcp ON dc.name = dcp.parent
        WHERE 
            dcp.key IN ('SR', 'MAC')  -- Filter only required keys
        GROUP BY 
            dc.device_id              -- Group by device_id to aggregate SR and MAC
        ORDER BY 
            CAST(MAX(CASE WHEN dcp.key = 'SR' THEN dcp.value ELSE NULL END) AS UNSIGNED) ASC
            -- Order results numerically by SR
    """, as_dict=True)

    return device_data  # Return result as a list of dictionaries
