import frappe
from frappe import _
from frappe.utils import nowdate
from frappe.model.document import Document

@frappe.whitelist()
def get_books(filters=None):
    """Get list of books with optional filters"""
    if not filters:
        filters = {}
    
    books = frappe.get_all("Book",
        fields=["name", "title", "author", "publish_date", "isbn", "status"],
        filters=filters,
        order_by="title"
    )
    
    return books

@frappe.whitelist()
def create_book(book_data):
    """Create a new book"""
    if not frappe.session.user == "Administrator" and "Librarian" not in frappe.get_roles():
        frappe.throw(_("You don't have permission to create books"), frappe.PermissionError)
    
    book = frappe.get_doc({
        "doctype": "Book",
        "title": book_data.get("title"),
        "author": book_data.get("author"),
        "publish_date": book_data.get("publish_date"),
        "isbn": book_data.get("isbn"),
        "status": "Available"
    })
    
    book.insert()
    return book

@frappe.whitelist()
def update_book(book_name, book_data):
    """Update an existing book"""
    if not frappe.session.user == "Administrator" and "Librarian" not in frappe.get_roles():
        frappe.throw(_("You don't have permission to update books"), frappe.PermissionError)
    
    book = frappe.get_doc("Book", book_name)
    book.update(book_data)
    book.save()
    return book

@frappe.whitelist()
def delete_book(book_name):
    """Delete a book"""
    if not frappe.session.user == "Administrator" and "Librarian" not in frappe.get_roles():
        frappe.throw(_("You don't have permission to delete books"), frappe.PermissionError)
    
    book = frappe.get_doc("Book", book_name)
    book.delete()
    return {"message": "Book deleted successfully"}