import frappe

def check_telemetry_alarms(doc, method):
    # Loop through each row in the child table "Device Telemetry Key-Value"
    for row in doc.device_telemetry_key_value:  # Assuming the child table is named 'device_telemetry_key_value'
        frappe.logger().info(f"[CHECKING] {row.key} = {row.value}")

        # Check for the alarm conditions (ALINPVHI = 1 or ALINPVLOW = 1)
        if row.key in ["ALINPVHI", "ALINPVLOW"] and row.value == "1":
            send_alarm_email(row.key, doc.timestamp)  # doc.timestamp comes from the parent DocType

def send_alarm_email(alarm_type, timestamp):
    subject = f"⚠️ {alarm_type} Alarm Triggered"
    message = f"""
        <p><strong>Alarm Triggered</strong> at {timestamp}</p>
        <p><strong>{alarm_type}</strong> = 1</p>
        <p>Please take necessary action.</p>
    """

    recipients = ["harshavardhan.deshmukh@logicare.in"]  # Replace with your actual email(s)

    try:
        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            message=message
        )
        frappe.logger().info(f"[EMAIL SENT] {alarm_type} triggered at {timestamp}")
    except Exception as e:
        frappe.logger().error(f"[EMAIL ERROR] Failed: {str(e)}")
