import frappe
from frappe import _
from frappe.utils import nowdate

@frappe.whitelist()
def get_reservations(filters=None):
    """Get list of reservations with optional filters"""
    if not filters:
        filters = {}
    
    reservations = frappe.get_all("Reservation",
        fields=["name", "reservation_id", "book", "member", "reservation_date", "status"],
        filters=filters,
        order_by="reservation_date"
    )
    
    # Add book and member details
    for reservation in reservations:
        reservation.book_details = frappe.get_doc("Book", reservation.book).as_dict()
        reservation.member_details = frappe.get_doc("Member", reservation.member).as_dict()
    
    return reservations

@frappe.whitelist()
def create_reservation(reservation_data):
    """Create a new reservation"""
    # Members can create reservations for themselves
    if "Member" in frappe.get_roles():
        # Verify the member is reserving for themselves
        member = frappe.db.get_value("Member", {"email": frappe.session.user}, "name")
        if member != reservation_data.get("member"):
            frappe.throw(_("You can only create reservations for yourself"), frappe.PermissionError)
    
    reservation = frappe.get_doc({
        "doctype": "Reservation",
        "book": reservation_data.get("book"),
        "member": reservation_data.get("member"),
        "reservation_date": reservation_data.get("reservation_date") or nowdate(),
        "status": "Pending"
    })
    
    reservation.insert()
    reservation.submit()
    return reservation

@frappe.whitelist()
def cancel_reservation(reservation_name):
    """Cancel a reservation"""
    reservation = frappe.get_doc("Reservation", reservation_name)
    
    # Members can only cancel their own reservations
    if "Member" in frappe.get_roles():
        member = frappe.db.get_value("Member", {"email": frappe.session.user}, "name")
        if member != reservation.member:
            frappe.throw(_("You can only cancel your own reservations"), frappe.PermissionError)
    
    reservation.status = "Cancelled"
    reservation.save()
    
    # Update book status if needed
    book = frappe.get_doc("Book", reservation.book)
    if book.status == "Reserved":
        # Check if there are other pending reservations
        other_reservations = frappe.get_all("Reservation", 
            filters={"book": reservation.book, "status": "Pending", "name": ["!=", reservation.name]})
        
        if not other_reservations:
            book.status = "Available"
            book.save()
    
    return reservation