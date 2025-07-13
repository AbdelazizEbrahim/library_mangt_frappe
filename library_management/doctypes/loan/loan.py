from frappe.model.document import Document
import frappe
from frappe.utils import nowdate, add_days, getdate

class Loan(Document):
    def before_save(self):
        # Generate loan ID
        if not self.loan_id:
            self.loan_id = f"LOAN-{frappe.generate_hash(length=8)}"
        
        # Set default return date (14 days from loan date)
        if not self.return_date:
            self.return_date = add_days(self.loan_date, 14)
        
        # Validate dates
        if getdate(self.return_date) < getdate(self.loan_date):
            frappe.throw("Return date cannot be before loan date")
        
        # Check book availability
        self.validate_book_availability()
    
    def validate_book_availability(self):
        book = frappe.get_doc("Book", self.book)
        if book.status != "Available":
            frappe.throw(f"Book {self.book} is not available for loan (Current status: {book.status})")
    
    def on_submit(self):
        # Update book status when loan is created
        book = frappe.get_doc("Book", self.book)
        book.status = "On Loan"
        book.save()
    
    def before_cancel(self):
        # Update book status when loan is cancelled
        book = frappe.get_doc("Book", self.book)
        book.status = "Available"
        book.save()