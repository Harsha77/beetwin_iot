app_name = "beetwin_iot"
app_title = "beetwin_iot"
app_publisher = "Logicare Systems Private Limited"
app_description = "This is the aap for beetwin iot platform"
app_email = "harshavardhan.deshmukh@logicare.in"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "beetwin_iot",
# 		"logo": "/assets/beetwin_iot/logo.png",
# 		"title": "beetwin_iot",
# 		"route": "/beetwin_iot",
# 		"has_permission": "beetwin_iot.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/beetwin_iot/css/beetwin_iot.css"
# app_include_js = "/assets/beetwin_iot/js/beetwin_iot.js"

# include js, css files in header of web template
# web_include_css = "/assets/beetwin_iot/css/beetwin_iot.css"
# web_include_js = "/assets/beetwin_iot/js/beetwin_iot.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "beetwin_iot/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "beetwin_iot/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "beetwin_iot.utils.jinja_methods",
# 	"filters": "beetwin_iot.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "beetwin_iot.install.before_install"
# after_install = "beetwin_iot.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "beetwin_iot.uninstall.before_uninstall"
# after_uninstall = "beetwin_iot.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "beetwin_iot.utils.before_app_install"
# after_app_install = "beetwin_iot.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "beetwin_iot.utils.before_app_uninstall"
# after_app_uninstall = "beetwin_iot.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "beetwin_iot.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"beetwin_iot.tasks.all"
# 	],
# 	"daily": [
# 		"beetwin_iot.tasks.daily"
# 	],
# 	"hourly": [
# 		"beetwin_iot.tasks.hourly"
# 	],
# 	"weekly": [
# 		"beetwin_iot.tasks.weekly"
# 	],
# 	"monthly": [
# 		"beetwin_iot.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "beetwin_iot.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "beetwin_iot.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "beetwin_iot.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["beetwin_iot.utils.before_request"]
before_request = ["beetwin_iot.auth.validate_api_key_secret"]



doc_events = {
    "Device Telemetry": {
        "after_insert": "beetwin_iot.beetwin_iot.api.telemetry_hooks.check_telemetry_alarms"
    }
}




# after_request = ["beetwin_iot.utils.after_request"]

# Job Events
# ----------
# before_job = ["beetwin_iot.utils.before_job"]
# after_job = ["beetwin_iot.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"beetwin_iot.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }



app_include_js = ["/assets/beetwin_iot/js/sensor_dashboard.js"]
app_include_js = ["/assets/frappe/css/help.css"]


# Add this line to ensure your JS file is loaded for the report
app_include_js = ["/assets/beetwin_iot/js/sensor_data_report.js"]


website_route_rules = [{'from_route': '/vertive/<path:app_path>', 'to_route': 'vertive'}, {'from_route': '/beetwin_hs/<path:app_path>', 'to_route': 'beetwin_hs'}, {'from_route': '/iotweet-dashboard/<path:app_path>', 'to_route': 'iotweet-dashboard'},]
# Add this line
app_include_js = "/assets/beetwin_iot/js/beetwin_iot.js"

# Add this line for API
override_whitelisted_methods = {
    'get_latest_device_data': 'beetwin_iot.api.get_latest_device_data',
}