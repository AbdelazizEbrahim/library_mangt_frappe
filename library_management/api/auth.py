import frappe
from frappe import _
from frappe.auth import LoginManager
from frappe.utils.password import get_decrypted_password

@frappe.whitelist(allow_guest=True)
def login(email, password):
    """Authenticate user and return user details"""
    try:
        login_manager = LoginManager()
        login_manager.authenticate(email, password)
        login_manager.post_login()
        
        user = frappe.get_doc("User", email)
        roles = frappe.get_roles(email)
        
        # Get member details if user is a member
        member = None
        if "Member" in roles:
            member = frappe.db.get_value("Member", {"email": email}, "name")
        
        return {
            "email": email,
            "full_name": user.full_name,
            "roles": roles,
            "member": member,
            "sid": frappe.session.sid
        }
    except frappe.AuthenticationError:
        frappe.throw(_("Invalid email or password"), frappe.AuthenticationError)

@frappe.whitelist()
def logout():
    """Logout current user"""
    frappe.local.login_manager.logout()
    return {"message": "Logged out successfully"}

@frappe.whitelist(allow_guest=True)
def register(full_name, email, password, membership_id=None, phone=None):
    """Register a new member"""
    if frappe.db.exists("User", email):
        frappe.throw(_("Email already registered"))
    
    # Create user
    user = frappe.get_doc({
        "doctype": "User",
        "email": email,
        "first_name": full_name,
        "new_password": password,
        "send_welcome_email": 0,
        "roles": [{"role": "Member"}]
    })
    user.insert()
    
    # Create member record
    member = frappe.get_doc({
        "doctype": "Member",
        "full_name": full_name,
        "email": email,
        "membership_id": membership_id or f"MEM-{frappe.generate_hash(length=8)}",
        "phone": phone
    })
    member.insert()
    
    return {
        "email": email,
        "full_name": full_name,
        "roles": ["Member"],
        "member": member.name
    }

@frappe.whitelist()
def get_current_user():
    """Get details of currently logged in user"""
    if not frappe.session.user or frappe.session.user == "Guest":
        frappe.throw(_("Not logged in"), frappe.AuthenticationError)
    
    user = frappe.get_doc("User", frappe.session.user)
    roles = frappe.get_roles()
    
    # Get member details if user is a member
    member = None
    if "Member" in roles:
        member = frappe.db.get_value("Member", {"email": frappe.session.user}, "name")
    
    return {
        "email": frappe.session.user,
        "full_name": user.full_name,
        "roles": roles,
        "member": member
    }