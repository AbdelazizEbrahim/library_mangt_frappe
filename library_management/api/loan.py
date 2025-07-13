import frappe
from frappe import _
from frappe.utils import nowdate, add_days

@frappe.whitelist()
def get_loans(filters=None):
    """Get list of loans with optional filters"""
    if not filters:
        filters = {}
    
    loans = frappe.get_all("Loan",
        fields=["name", "loan_id", "book", "member", "loan_date", "return_date", "status"],
        filters=filters,
        order_by="return_date"
    )
    
    # Add book and member details
    for loan in loans:
        loan.book_details = frappe.get_doc("Book", loan.book).as_dict()
        loan.member_details = frappe.get_doc("Member", loan.member).as_dict()
    
    return loans

@frappe.whitelist()
def create_loan(loan_data):
    """Create a new loan"""
    if not frappe.session.user == "Administrator" and "Librarian" not in frappe.get_roles():
        frappe.throw(_("You don't have permission to create loans"), frappe.PermissionError)
    
    loan = frappe.get_doc({
        "doctype": "Loan",
        "book": loan_data.get("book"),
        "member": loan_data.get("member"),
        "loan_date": loan_data.get("loan_date") or nowdate(),
        "return_date": loan_data.get("return_date") or add_days(nowdate(), 14),
        "status": "Active"
    })
    
    loan.insert()
    loan.submit()
    return loan

@frappe.whitelist()
def return_loan(loan_name):
    """Mark a loan as returned"""
    if not frappe.session.user == "Administrator" and "Librarian" not in frappe.get_roles():
        frappe.throw(_("You don't have permission to update loans"), frappe.PermissionError)
    
    loan = frappe.get_doc("Loan", loan_name)
    loan.status = "Returned"
    loan.save()
    
    # Update book status
    book = frappe.get_doc("Book", loan.book)
    
    # Check if there are pending reservations
    pending_reservations = frappe.get_all("Reservation", 
        filters={"book": loan.book, "status": "Pending"})
    
    if pending_reservations:
        book.status = "Reserved"
    else:
        book.status = "Available"
    
    book.save()
    
    return loan