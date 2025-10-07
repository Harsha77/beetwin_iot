import frappe

@frappe.whitelist(allow_guest=True)
def get_device_config():
    """
    API to fetch Device Config with selected parameters (Device ID, SR, MAC),
    sorted by SR in ascending order.
    """
    device_data = frappe.db.sql("""
        SELECT 
            dc.device_id AS `Device ID`,
            MAX(CASE WHEN dcp.key = 'SR' THEN dcp.value ELSE NULL END) AS `SR`,
            MAX(CASE WHEN dcp.key = 'MAC' THEN dcp.value ELSE NULL END) AS `MAC`
        FROM 
            `tabDevice Config` dc
        LEFT JOIN `tabDevice Config Key-Value` dcp ON dc.name = dcp.parent
        WHERE 
            dcp.key IN ('SR', 'MAC')
        GROUP BY 
            dc.device_id
        ORDER BY 
            CAST(MAX(CASE WHEN dcp.key = 'SR' THEN dcp.value ELSE NULL END) AS UNSIGNED) ASC
    """, as_dict=True)

    return device_data
