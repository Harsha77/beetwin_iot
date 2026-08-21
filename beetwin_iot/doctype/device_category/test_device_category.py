# Copyright (c) 2024, Logicare Systems Private Limited and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class UnitTestDeviceCategory(UnitTestCase):
	"""
	Unit tests for DeviceCategory.
	Use this class for testing individual functions and methods.
	"""

	pass


class IntegrationTestDeviceCategory(IntegrationTestCase):
	"""
	Integration tests for DeviceCategory.
	Use this class for testing interactions between multiple components.
	"""

	pass
