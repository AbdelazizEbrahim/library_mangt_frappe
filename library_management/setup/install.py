import frappe

def after_install():
    create_roles()
    set_role_permissions()

def create_roles():
    roles = ["Librarian", "Member"]
    for role in roles:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role,
                "desk_access": 1
            }).insert()

def set_role_permissions():
    # Librarian can access everything in the app
    frappe.get_doc({
        "doctype": "Role Profile",
        "name": "Librarian",
        "roles": [
            {"role": "Librarian"}
        ]
    }).insert(ignore_if_duplicate=True)
    
    # Member has limited access
    frappe.get_doc({
        "doctype": "Role Profile",
        "name": "Member",
        "roles": [
            {"role": "Member"}
        ]
    }).insert(ignore_if_duplicate=True)