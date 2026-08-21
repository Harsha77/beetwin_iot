// ================================================================
// Report Script: BTX-PP Timeseries Data Table
// ---------------------------------------------------------------
// This script defines the report logic for "BTX-PP Timeseries Data Table".
// It dynamically populates the Device Name dropdown filter by fetching
// device data via a backend call, and configures report filters.
// ================================================================

frappe.query_reports["BTX-PP Timeseries Data Table"] = {

    // ------------------------------------------------------------
    // onload: Triggered when the report is first loaded.
    // It makes a backend call to fetch device data and populate
    // the device filter dynamically.
    // ------------------------------------------------------------
    
    "onload": function() {
        frappe.call({
            // Backend method that returns device list
            method: "beetwin_iot.beetwin_iot.report.btx_pp_timeseries_data_table.get_devices.get_device_data",
            callback: function(r) {
                if (r.message) {
                    // Get reference to the 'device_data' filter object
                    let device_filter = frappe.query_report.get_filter("device_data");

                    // Map to store device name to IMEI mapping
                    let device_options_map = {};

                    // Array to store options for the select filter
                    let display_options = [];

                    // Iterate through each device string returned from backend
                    r.message.forEach(device => {
                        // Split string into words; last word is assumed IMEI
                        let parts = device.split(" ");
                        let imei_number = parts.pop(); // Extract IMEI
                        let device_name = parts.join(" "); // Extract name

                        // Skip 'ALL' placeholder entries
                        if (device_name.toUpperCase() === "ALL" || imei_number.toUpperCase() === "ALL") {
                            return;
                        }

                        // Add to mapping and filter options list
                        device_options_map[device_name] = imei_number;
                        display_options.push({
                            label: device_name,
                            value: imei_number  
                        });
                    });

                    // Assign generated map and options to the filter
                    device_filter.df.device_options_map = device_options_map;
                    device_filter.df.options = display_options;
                    device_filter.refresh(); // Re-render the filter
                } else {
                    // Show message if no device data is returned
                    frappe.msgprint(__('No device data found.'));
                }
            }
        });
    },

    // ------------------------------------------------------------
    // Filters for the report UI
    // ------------------------------------------------------------
    "filters": [
        {
            // Device selection filter (populated on load)
            "fieldname": "device_data",
            "label": __("Device Name"),
            "fieldtype": "Select",
            "options": [], // Dynamically assigned
            "reqd": 1, // Required field

            // Triggered when filter value is changed
            "on_change": function() {
                let device_filter = frappe.query_report.get_filter("device_data");
                let selected_value = device_filter.get_value();
                
                // Set the selected value again to ensure it's retained
                frappe.query_report.set_filter_value("device_data", selected_value);
                
                // Refresh the report based on the selected filter
                frappe.query_report.refresh();
            }
        },
        {
            // From Date filter
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date"
        },
        {
            // To Date filter
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date"
        }
    ]
};
