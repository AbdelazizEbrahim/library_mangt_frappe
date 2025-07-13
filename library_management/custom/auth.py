import frappe

def has_loan_permission(doc, user):
    if "Librarian" in frappe.get_roles(user):
        return True
    
    if doc.member == frappe.db.get_value("Member", {"email": frappe.session.user}, "name"):
        return True
    
    return False

def has_reservation_permission(doc, user):
    if "Librarian" in frappe.get_roles(user):
        return True
    
    if doc.member == frappe.db.get_value("Member", {"email": frappe.session.user}, "name"):
        return True
    
    return False