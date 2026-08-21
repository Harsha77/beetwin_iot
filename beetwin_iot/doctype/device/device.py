# Copyright (c) 2024, Logicare Systems Pvt Ltd and contributors
# For license information, please see license.txt

# Imports
# --------
# Frappe framework and utility functions for document handling and key generation
# `random_string` is used for generating secure keys
from frappe.model.document import Document
import frappe
from frappe.utils import random_string
from frappe.model.document import Document

# Constants
# ---------
# Define the lengths of the keys used for device authentication and identification
API_KEY_LENGTH = 15
API_SECRET_LENGTH = 15
DEVICE_KEY_SUFFIX_LENGTH = 20

# ------------------------------------------------------------------
# Helper Function: generate_api_key
# ------------------------------------------------------------------
# Generate a random API Key using predefined length
def generate_api_key():
    return random_string(API_KEY_LENGTH)

# ------------------------------------------------------------------
# Helper Function: generate_api_secret
# ------------------------------------------------------------------
# Generate a random API Secret using predefined length
def generate_api_secret():
    return random_string(API_SECRET_LENGTH)

# ------------------------------------------------------------------
# Helper Function: generate_device_key
# ------------------------------------------------------------------
# Generate a Device Key with a fixed prefix and a random suffix
def generate_device_key():
    return f"LSPL_{random_string(DEVICE_KEY_SUFFIX_LENGTH)}"

# ------------------------------------------------------------------
# Class: Device (Custom DocType Extension)
# ------------------------------------------------------------------
# Customization of the standard Document class for the "Device" DocType
# Includes logic for automatically setting API credentials and device key
class Device(Document):
    def before_save(self):
        """
        Hook that runs before saving the Device document.
        Ensures that API Key, API Secret, and Device Key are set.
        Displays the API Secret in a popup if generated.
        """
        # Generate and set API Key if not already set
        if not self.api_key:
            self.api_key = generate_api_key()

        # Generate and set API Secret if not already set
        if not self.api_secret:
            self.api_secret = generate_api_secret()
            # Show the API secret to the user in a popup
            self.show_api_secret_popup()

        # Generate and set Device Key if not already set
        if not self.device_key:
            self.device_key = generate_device_key()

    def show_api_secret_popup(self):
        """
        Displays the generated API credentials (Key & Secret) in a UI message popup.
        Ensures that the user sees the secret before the document is saved.
        """
        frappe.msgprint(
            msg=f"""
            <p><strong>Your API Key:</strong> {self.api_key}</p>
            <p><strong>Your API Secret:</strong> {self.api_secret}</p>
            """,
            title="API Credentials",
            indicator="green"
        )

# ------------------------------------------------------------------
# Function: get_restricted_devices
# ------------------------------------------------------------------
# Returns a list of device records that belong to device groups assigned
# to the given user.
# Used for filtering device data based on group permissions.
def get_restricted_devices(user):
    """
    Fetch devices for logged-in user based on assigned device group.
    
    Args:
        user (str): The current logged-in user.

    Returns:
        list: A list of device records that belong to user's device groups.
    """
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

# ------------------------------------------------------------------
# Function: on_device_list_query
# ------------------------------------------------------------------
# Frappe DocType query hook function used to restrict the list view
# of the "Device" DocType to devices that belong to the user's assigned
# groups, except for the Administrator.
def on_device_list_query(doc, method):
    """
    Restrict Device listing to assigned groups, but allow Administrator to see all devices.
    
    Args:
        doc (Document): The current document (not used here).
        method (str): The method name triggering this hook (not used here).

    Returns:
        dict | None: A filter dict if user is not admin, else None for no filter.
    """
    user = frappe.session.user

    # Allow Administrator to view all device records without restrictions
    if user == "Administrator":
        return

    # Get filtered list of devices for the user
    allowed_devices = get_restricted_devices(user)

    # Return Frappe-style filter dict to limit list view
    return {"filters": [["name", "in", [d["name"] for d in allowed_devices]]]}
