// ===================================================================
// Frappe Client-Side Script for "Device" DocType
// ---------------------------------------------------
// This script runs before saving a new Device record.
// It sets default values for `is_set_keys` and `ack` fields
// when a new document is being created.
//
// Hooks:
//   - before_save: Triggered just before the form is saved
// ===================================================================

frappe.ui.form.on("Device", {
    
    // Hook: before_save
    // Purpose: Automatically initialize fields when a new device is being created
    // Logic:
    //   - If the document is new (i.e., being created),
    //     set `is_set_keys` to 1 (indicating that keys are initialized),
    //     and `ack` to 0 (resetting acknowledgment flag)
    before_save: function(frm) {
        if (frm.is_new()) { // Check if the document is being created
            frm.set_value('is_set_keys', 1);  // Mark keys as set
            frm.set_value('ack', 0);          // Reset ACK status
        }
    }
});
