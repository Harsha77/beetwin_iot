import frappe
from frappe import _
from frappe.utils.password import check_password, update_password

@frappe.whitelist()
def admin_change_password(user, old_password, new_password):
    if frappe.session.user != user and frappe.session.user != "Administrator":
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    # Validate old password
    if not check_password(user, old_password):
        frappe.throw(_("Incorrect old password"), frappe.AuthenticationError)

    # Update password
    frappe.utils.password.update_password(user, new_password)

    return {"message": "Password Updated"}
