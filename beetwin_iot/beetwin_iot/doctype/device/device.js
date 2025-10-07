

// frappe.ui.form.on("Device", {
// 	before_save: function(frm) {
//         frm.set_value('is_set_keys',1);
//         frm.set_value('ack',0);
//     }
// });


frappe.ui.form.on("Device", {
    before_save: function(frm) {
        if (frm.is_new()) { // Check if the document is being created
            frm.set_value('is_set_keys', 1);
            frm.set_value('ack', 0);
        }
    }
});



