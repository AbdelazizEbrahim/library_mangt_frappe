from frappe import _

app_name = "library_management"
app_title = "Library Management"
app_publisher = "Your Name"
app_description = "A simple library management system"
app_icon = "octicon octicon-book"
app_color = "grey"
app_email = "your@email.com"
app_license = "MIT"

# Include JS/CSS files in header of desk.html
# app_include_css = "/assets/library_management/css/library_management.css"
# app_include_js = "/assets/library_management/js/library_management.js"

# Run after install
after_install = "library_management.setup.install.after_install"

# Custom permission hooks
has_permission = {
    "Loan": "library_management.custom.auth.has_loan_permission",
    "Reservation": "library_management.custom.auth.has_reservation_permission"
}

# Fixtures to export roles and custom permissions
fixtures = [
    {
        "dt": "Role",
        "filters": [["role_name", "in", ["Librarian", "Member"]]]
    },
    {
        "dt": "Custom DocPerm",
        "filters": [["role", "in", ["Librarian", "Member"]]]
    }
]

# Scheduler events
scheduler_events = {
    "daily": [
        "library_management.scheduler_events.daily"
    ]
}
