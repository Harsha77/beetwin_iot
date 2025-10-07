frappe.ui.form.on("Device Config", {
    before_save: function (frm) {
        let config_params_changed = false;
        let firmware_file_attached = false;

        // Track changes in "Device Config Parameters" section
        if (frm.doc.device_config_parameters) {
            frm.doc.device_config_parameters.forEach((row) => {
                if (!row.__islocal && row.value !== row.__last_value) {
                    config_params_changed = true;
                }
            });
        }

        // Track changes in "Device Firmware Version" section
        if (frm.doc.attach_yybs) {
            if (!frm.doc.__last_attach_yybs || frm.doc.attach_yybs !== frm.doc.__last_attach_yybs) {
                firmware_file_attached = true;
            }
        }

        // **Apply changes only for respective sections**
        if (config_params_changed && !firmware_file_attached) { 
            // Ensure is_new_config is set ONLY if firmware is NOT changed
            frm.set_value("is_new_config", 1);
            frm.set_value("acknowledge", 0); // Reset acknowledgment for config changes
        } else if (!config_params_changed) {
            frm.set_value("is_new_config", 0);
        }

        if (firmware_file_attached) {
            frm.set_value("is_new_ota", 1);
            frm.set_value("otaacknowledge", 0); // Reset acknowledgment for OTA changes
        } else {
            frm.set_value("is_new_ota", 0);
        }

        // **Store last known values**
        frm.doc.__last_attach_yybs = frm.doc.attach_yybs;

        // Store last known values for "Device Config Parameters"
        frm.doc.device_config_parameters.forEach((row) => {
            row.__last_value = row.value;
        });
    }
});



// ✨ New logic: Auto-populate firmware_file in child table when a Device Version is selected
frappe.ui.form.on("Device Version Entry", {
    device_version: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.device_version) {
            frappe.db.get_doc("OTA Version", row.device_version).then(doc => {
                frappe.model.set_value(cdt, cdn, "firmware_file", doc.firmware_file);
            });
        }
    }
});
