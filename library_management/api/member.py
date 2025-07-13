import frappe
from frappe import _

@frappe.whitelist()
def get_members(filters=None):
    """Get list of members with optional filters"""
    if not filters:
        filters = {}
    
    members = frappe.get_all("Member",
        fields=["name", "full_name", "membership_id", "email", "phone"],
        filters=filters,
        order_by="full_name"
    )
    
    return members

@frappe.whitelist()
def create_member(member_data):
    """Create a new member"""
    if not frappe.session.user == "Administrator" and "Librarian" not in frappe.get_roles():
        frappe.throw(_("You don't have permission to create members"), frappe.PermissionError)
    
    member = frappe.get_doc({
        "doctype": "Member",
        "full_name": member_data.get("full_name"),
        "membership_id": member_data.get("membership_id"),
        "email": member_data.get("email"),
        "phone": member_data.get("phone")
    })
    
    member.insert()
    return member

@frappe.whitelist()
def update_member(member_name, member_data):
    """Update an existing member"""
    if not frappe.session.user == "Administrator" and "Librarian" not in frappe.get_roles():
        frappe.throw(_("You don't have permission to update members"), frappe.PermissionError)
    
    member = frappe.get_doc("Member", member_name)
    member.update(member_data)
    member.save()
    return member

@frappe.whitelist()
def delete_member(member_name):
    """Delete a member"""
    if not frappe.session.user == "Administrator" and "Librarian" not in frappe.get_roles():
        frappe.throw(_("You don't have permission to delete members"), frappe.PermissionError)
    
    member = frappe.get_doc("Member", member_name)
    member.delete()
    return {"message": "Member deleted successfully"}