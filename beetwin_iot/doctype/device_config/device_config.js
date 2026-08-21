// // ================================================================
// // Frappe Client Script for "Device Config" DocType
// // ------------------------------------------------
// // This script handles automatic flagging of configuration and OTA changes,
// // by tracking modifications in child tables and file attachments.
// // It also ensures the reset of acknowledgment flags and stores the last
// // known values to avoid redundant change detection.
// // ================================================================
// frappe.ui.form.on("Device Config", {
//     // ---------------------------------------------
//     // Event: before_save
//     // Purpose: Detect changes in device configuration parameters or
//     // firmware file attachment, and accordingly set flags for config
//     // or OTA update and reset acknowledgments.
//     // ---------------------------------------------
//     before_save: function (frm) {
//         let config_params_changed = false;
//         let firmware_file_attached = false;

//         // Check for changes in "Device Config Parameters" child table
//         if (frm.doc.device_config_parameters) {
//             frm.doc.device_config_parameters.forEach((row) => {
//                 if (!row.__islocal && row.value !== row.__last_value) {
//                     config_params_changed = true;  // Config parameter has changed
//                 }
//             });
//         }

//         // Check for changes in the firmware file attachment field
//         if (frm.doc.attach_yybs) {
//             if (!frm.doc.__last_attach_yybs || frm.doc.attach_yybs !== frm.doc.__last_attach_yybs) {
//                 firmware_file_attached = true;  // Firmware file has changed
//             }
//         }

//         // Set config change flags if only config changed (not firmware)
//         if (config_params_changed && !firmware_file_attached) { 
//             frm.set_value("is_new_config", 1);  // Mark config as new
//             frm.set_value("acknowledge", 0);    // Reset acknowledgment flag
//         } else if (!config_params_changed) {
//             frm.set_value("is_new_config", 0);  // No config change detected
//         }

//         // Set OTA change flags if firmware changed
//         if (firmware_file_attached) {
//             frm.set_value("is_new_ota", 1);       // Mark OTA update as new
//             frm.set_value("otaacknowledge", 0);   // Reset OTA acknowledgment
//         } else {
//             frm.set_value("is_new_ota", 0);       // No OTA change detected
//         }

//         // Store the current firmware file as the last known state
//         frm.doc.__last_attach_yybs = frm.doc.attach_yybs;

//         // Store last known value for each config parameter to track changes next time
//         frm.doc.device_config_parameters.forEach((row) => {
//             row.__last_value = row.value;
//         });
//     }
// });


// // ================================================================
// // Frappe Client Script for "Device Version Entry" Child Table
// // ------------------------------------------------------------
// // This script automatically populates the firmware_file field
// // in the child row when a Device Version is selected by fetching
// // its associated data from the "OTA Version" DocType.
// // ================================================================
// frappe.ui.form.on("Device Version Entry", {
//     // ---------------------------------------------
//     // Trigger: device_version (field change)
//     // Purpose: On selecting a Device Version, fetch its related
//     // firmware file and populate the firmware_file field.
//     // ---------------------------------------------
//     device_version: function(frm, cdt, cdn) {
//         var row = locals[cdt][cdn];
//         if (row.device_version) {
//             frappe.db.get_doc("OTA Version", row.device_version).then(doc => {
//                 frappe.model.set_value(cdt, cdn, "firmware_file", doc.firmware_file);
//             });
//         }
//     }
// });



// ================================================================
// Frappe Client Script for "Device Config" DocType
// ------------------------------------------------
// Strictly independent flags, no unintended resets:
// - device_version   => attach_yybs + is_new_ota (only)
// - device_ssl_version => attach_ssl + is_new_ssl (only)
// - config param value change => is_new_config (only)
// IMPORTANT: We do NOT set unrelated flags to 0 in before_save.
// ================================================================

function hasField(doctype, fieldname) {
    try {
        return Boolean(frappe.meta.get_docfield(doctype, fieldname, null));
    } catch (e) {
        return false;
    }
}

// Seed baselines on first load/refresh to avoid false positives
function seedBaselines(frm) {
    if (frm.__baselined) return;

    frm.doc.__last_attach_yybs = frm.doc.attach_yybs || null;
    if (hasField("Device Config", "attach_ssl")) {
        frm.doc.__last_attach_ssl = frm.doc.attach_ssl || null;
    }
    if (Array.isArray(frm.doc.device_config_parameters)) {
        frm.doc.device_config_parameters.forEach(row => {
            if (typeof row.__last_value === "undefined") row.__last_value = row.value;
        });
    }
    frm.__baselined = true;
}

frappe.ui.form.on("Device Config", {
    onload(frm) { seedBaselines(frm); },
    refresh(frm) { seedBaselines(frm); },

    // ---- OTA: select version => attach_yybs, mark OTA changed
    device_version(frm) {
        const v = frm.doc.device_version;
        if (!v) { frm.__ota_user_set = false; return; }

        frappe.db.get_doc("OTA Version", v).then(doc => {
            if (hasField("Device Config", "attach_yybs") && doc.firmware_file) {
                frm.set_value("attach_yybs", doc.firmware_file);
            }
            // Mark this round as OTA change; set flag = 1 (do not touch others)
            frm.__ota_user_set = true;
            frm.set_value("is_new_ota", 1);
            if (hasField("Device Config", "otaacknowledge")) frm.set_value("otaacknowledge", 0);
        }).catch(() => {});
    },

    // ---- SSL: select version => attach_ssl, mark SSL changed
    device_ssl_version(frm) {
        const v = frm.doc.device_ssl_version;
        if (!v) { frm.__ssl_user_set = false; return; }

        // If SSL uses a different DocType, replace "OTA Version"
        frappe.db.get_doc("OTA Version", v).then(doc => {
            if (hasField("Device Config", "attach_ssl")) {
                const sslPath = doc.ssl_file || doc.firmware_file || null;
                if (sslPath) frm.set_value("attach_ssl", sslPath);
            }
            frm.__ssl_user_set = true;
            if (hasField("Device Config", "is_new_ssl")) frm.set_value("is_new_ssl", 1);
            if (hasField("Device Config", "sslacknowledge")) frm.set_value("sslacknowledge", 0);
        }).catch(() => {});
    },

    // Manual file pick for SSL => only SSL flag
    attach_ssl(frm) {
        if (!hasField("Device Config", "is_new_ssl")) return;
        const changed = frm.doc.attach_ssl && frm.doc.attach_ssl !== frm.doc.__last_attach_ssl;
        if (changed) {
            frm.__ssl_user_set = true;
            frm.set_value("is_new_ssl", 1);
            if (hasField("Device Config", "sslacknowledge")) frm.set_value("sslacknowledge", 0);
        }
    },

    // Manual file pick for OTA => only OTA flag
    attach_yybs(frm) {
        const changed = frm.doc.attach_yybs && frm.doc.attach_yybs !== frm.doc.__last_attach_yybs;
        if (changed) {
            frm.__ota_user_set = true;
            frm.set_value("is_new_ota", 1);
            if (hasField("Device Config", "otaacknowledge")) frm.set_value("otaacknowledge", 0);
        }
    },

    // ---- Finalize only what changed THIS round; never reset others to 0
    before_save(frm) {
        // CONFIG diffs
        let config_params_changed = false;
        if (Array.isArray(frm.doc.device_config_parameters)) {
            frm.doc.device_config_parameters.forEach(row => {
                if (typeof row.__last_value !== "undefined" && row.value !== row.__last_value) {
                    config_params_changed = true;
                }
            });
        }
        const mark_config = !!frm.__config_user_set || config_params_changed;
        if (mark_config) {
            frm.set_value("is_new_config", 1);
            if (hasField("Device Config", "acknowledge")) frm.set_value("acknowledge", 0);
        }
        // NOTE: else do NOTHING (do not set to 0) so prior state is preserved

        // OTA diffs
        const ota_file_changed = !!(frm.doc.attach_yybs && frm.doc.attach_yybs !== frm.doc.__last_attach_yybs);
        const mark_ota = !!frm.__ota_user_set || ota_file_changed;
        if (mark_ota) {
            frm.set_value("is_new_ota", 1);
            if (hasField("Device Config", "otaacknowledge")) frm.set_value("otaacknowledge", 0);
        }
        // NOTE: else do NOTHING (no reset)

        // SSL diffs
        const ssl_file_changed = !!(frm.doc.attach_ssl && frm.doc.attach_ssl !== frm.doc.__last_attach_ssl);
        const mark_ssl = !!frm.__ssl_user_set || ssl_file_changed;
        if (mark_ssl && hasField("Device Config", "is_new_ssl")) {
            frm.set_value("is_new_ssl", 1);
            if (hasField("Device Config", "sslacknowledge")) frm.set_value("sslacknowledge", 0);
        }
        // NOTE: else do NOTHING (no reset)

        // Update baselines for next round
        frm.doc.__last_attach_yybs = frm.doc.attach_yybs || null;
        if (hasField("Device Config", "attach_ssl")) {
            frm.doc.__last_attach_ssl = frm.doc.attach_ssl || null;
        }
        if (Array.isArray(frm.doc.device_config_parameters)) {
            frm.doc.device_config_parameters.forEach(row => { row.__last_value = row.value; });
        }

        // Clear transient markers for this round
        frm.__ota_user_set = false;
        frm.__ssl_user_set = false;
        frm.__config_user_set = false;
    }
});

// CONFIG value edits => only CONFIG flag
frappe.ui.form.on("Device Config Parameters", {
    value(frm, cdt, cdn) {
        frm.__config_user_set = true;
        frm.set_value("is_new_config", 1);
        if (hasField("Device Config", "acknowledge")) frm.set_value("acknowledge", 0);
        // Do not touch OTA/SSL here
    }
});

// ================================================================
// Child Table: "Device Version Entry" (unchanged intent)
// - device_version     => set firmware_file only
// - device_ssl_version => set ssl_file only
// ================================================================
frappe.ui.form.on("Device Version Entry", {
    device_version(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        if (!row.device_version) return;
        frappe.db.get_doc("OTA Version", row.device_version).then(doc => {
            if (hasField(cdt, "firmware_file") && doc.firmware_file) {
                frappe.model.set_value(cdt, cdn, "firmware_file", doc.firmware_file);
            }
        }).catch(() => {});
    },
    device_ssl_version(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        if (!row.device_ssl_version) return;
        // Replace "OTA Version" with SSL DocType if different
        frappe.db.get_doc("OTA Version", row.device_ssl_version).then(doc => {
            if (hasField(cdt, "ssl_file")) {
                const sslPath = doc.ssl_file || doc.firmware_file || null;
                if (sslPath) frappe.model.set_value(cdt, cdn, "ssl_file", sslPath);
            }
        }).catch(() => {});
    }
});
