# Copyright (c) 2024, Logicare Systems Pvt Ltd and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe.utils import random_string
from frappe.model.document import Document

# Define the length for API keys, secrets, and device keys
API_KEY_LENGTH = 15
API_SECRET_LENGTH = 15
DEVICE_KEY_SUFFIX_LENGTH = 20

# Functions to generate keys and secrets
def generate_api_key():
    return random_string(API_KEY_LENGTH)

def generate_api_secret():
    return random_string(API_SECRET_LENGTH)

def generate_device_key():
    return f"LSPL_{random_string(DEVICE_KEY_SUFFIX_LENGTH)}"

class Device(Document):
    def before_save(self):
        # Generate and set API Key and API Secret if they are not already set
        if not self.api_key:
            self.api_key = generate_api_key()

        if not self.api_secret:
            self.api_secret = generate_api_secret()
            # Show the API secret in a popup
            self.show_api_secret_popup()

        # Generate and set Device Key if not already set
        if not self.device_key:
            self.device_key = generate_device_key()

    def show_api_secret_popup(self):
        """Show API secret in a popup."""
        frappe.msgprint(
            msg=f"""
            <p><strong>Your API Key:</strong> {self.api_key}</p>
            <p><strong>Your API Secret:</strong> {self.api_secret}</p>
            """,
            title="API Credentials",
            indicator="green"
        )


def get_restricted_devices(user):
    """Fetch devices for logged-in user based on assigned device group."""
    groups = frappe.get_all(
        "User Device Group",
        filters={"user": user},
        fields=["device_group"]
    )

    group_ids = [g["device_group"] for g in groups]

    if not group_ids:
        return []

    return frappe.get_all(
        "Device",
        filters={"device_group": ["in", group_ids]},
        fields=["name", "device_group"]
    )

def on_device_list_query(doc, method):
    """Restrict Device listing to assigned groups, but allow Administrator to see all devices."""
    user = frappe.session.user

    # Allow Administrator to see all devices
    if user == "Administrator":
        return  # No filters applied, so all devices are shown

    # Fetch devices restricted to user's assigned groups
    allowed_devices = get_restricted_devices(user)

    return {"filters": [["name", "in", [d["name"] for d in allowed_devices]]]}
