# import frappe

# @frappe.whitelist()
# def get_device_data():
#     device_data = frappe.db.sql("""
#         SELECT DISTINCT name1, imei_number
#         FROM `tabDevice`
#         WHERE name1 IS NOT NULL AND name1 != ''
#         AND imei_number IS NOT NULL AND imei_number != ''
#         ORDER BY name1 ASC  -- Sorting by Device Name in Ascending Order
#     """, as_dict=1)

#     # Format the data as "Device Name IMEI Number"
#     formatted_data = ["ALL"] + [f"{d['name1']} {d['imei_number']}" for d in device_data]

#     # Debugging to verify output
#     frappe.logger().debug("Formatted Device Data: {}".format(formatted_data))

#     return formatted_data




import frappe
import re

@frappe.whitelist(allow_guest=True)
def get_device_data():
    device_data = frappe.db.sql("""
        SELECT DISTINCT name1, imei_number
        FROM `tabDevice`
        WHERE name1 IS NOT NULL AND name1 != ''
        AND imei_number IS NOT NULL AND imei_number != ''
        ORDER BY name1 ASC  -- Sorting by Device Name in Ascending Order
    """, as_dict=1)

    # Filter devices where name1 starts with a number
    filtered_data = [d for d in device_data if re.match(r'^\d', d['name1'])]
    
    # Format the data as "Device Name IMEI Number"
    formatted_data = ["ALL"] + [f"{d['name1']} {d['imei_number']}" for d in filtered_data]

    # Debugging to verify output
    frappe.logger().debug("Filtered Device Data: {}".format(formatted_data))

    return formatted_data
