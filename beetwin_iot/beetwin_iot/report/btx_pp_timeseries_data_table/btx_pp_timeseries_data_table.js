
// frappe.query_reports["BTX-PP Timeseries Data Table"] = {
//     "onload": function() {
//         frappe.call({
//             method: "beetwin_iot.beetwin_iot.report.btx_pp_timeseries_data_table.get_devices.get_device_data",
//             callback: function(r) {
//                 if (r.message) {
//                     let device_filter = frappe.query_report.get_filter("device_data");

//                     // Create a mapping of "name1" → "IMEI Number"
//                     let device_options_map = {};
//                     let display_options = [];

//                     r.message.forEach(device => {
//                         let parts = device.split(" ");
//                         let imei_number = parts.pop(); // Extract IMEI Number
//                         let device_name = parts.join(" "); // Extract Device Name (name1)

//                         // Ensure "ALL" is not duplicated
//                         if (device_name.toUpperCase() === "ALL" || imei_number.toUpperCase() === "ALL") {
//                             return;
//                         }

//                         device_options_map[device_name] = imei_number;
//                         display_options.push({
//                             label: device_name, // Show only name1 in dropdown
//                             value: imei_number  // Internally store IMEI Number for selection
//                         });
//                     });

//                     // Save mapping to filter object for reference
//                     device_filter.df.device_options_map = device_options_map;

//                     // Bind name1 values to the dropdown (no "ALL")
//                     device_filter.df.options = display_options;
//                     device_filter.refresh();
//                 } else {
//                     frappe.msgprint(__('No device data found.'));
//                 }
//             }
//         });
//     },

//     "filters": [
//         {
//             "fieldname": "device_data",
//             "label": __("Device Name"),
//             "fieldtype": "Select",
//             "options": [], // Dynamically set
//             "reqd": 1,
//             "on_change": function() {
//                 let device_filter = frappe.query_report.get_filter("device_data");
//                 let selected_value = device_filter.get_value(); // Get selected value (IMEI)

//                 // Refresh report with selected IMEI Number
//                 frappe.query_report.set_filter_value("device_data", selected_value);
//                 frappe.query_report.refresh();
//             }
//         }
//     ]
// };



frappe.query_reports["BTX-PP Timeseries Data Table"] = {
    "onload": function() {
        frappe.call({
            method: "beetwin_iot.beetwin_iot.report.btx_pp_timeseries_data_table.get_devices.get_device_data",
            callback: function(r) {
                if (r.message) {
                    let device_filter = frappe.query_report.get_filter("device_data");

                    let device_options_map = {};
                    let display_options = [];

                    r.message.forEach(device => {
                        let parts = device.split(" ");
                        let imei_number = parts.pop();
                        let device_name = parts.join(" ");

                        if (device_name.toUpperCase() === "ALL" || imei_number.toUpperCase() === "ALL") {
                            return;
                        }

                        device_options_map[device_name] = imei_number;
                        display_options.push({
                            label: device_name,
                            value: imei_number  
                        });
                    });

                    device_filter.df.device_options_map = device_options_map;
                    device_filter.df.options = display_options;
                    device_filter.refresh();
                } else {
                    frappe.msgprint(__('No device data found.'));
                }
            }
        });
    },

    "filters": [
    {
        "fieldname": "device_data",
        "label": __("Device Name"),
        "fieldtype": "Select",
        "options": [],
        "reqd": 1,
        "on_change": function() {
            let device_filter = frappe.query_report.get_filter("device_data");
            let selected_value = device_filter.get_value();
            frappe.query_report.set_filter_value("device_data", selected_value);
            frappe.query_report.refresh();
        }
    },
    {
        "fieldname": "from_date",
        "label": __("From Date"),
        "fieldtype": "Date"
    },
    {
        "fieldname": "to_date",
        "label": __("To Date"),
        "fieldtype": "Date"
    }
]

};
