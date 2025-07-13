from frappe.model.document import Document
import frappe

class Reservation(Document):
    def before_save(self):
        # Generate reservation ID
        if not self.reservation_id:
            self.reservation_id = f"RES-{frappe.generate_hash(length=8)}"
        
        # Validate book is not available
        self.validate_book_status()
    
    def validate_book_status(self):
        book = frappe.get_doc("Book", self.book)
        if book.status == "Available":
            frappe.throw("Cannot reserve a book that is currently available")
    
    def on_submit(self):
        # Update book status when reservation is created
        book = frappe.get_doc("Book", self.book)
        if book.status == "On Loan":
            book.status = "Reserved"
            book.save()
    
    def before_cancel(self):
        # Update book status if needed when reservation is cancelled
        book = frappe.get_doc("Book", self.book)
        if book.status == "Reserved":
            # Check if there are other reservations
            other_reservations = frappe.get_all("Reservation", 
                filters={"book": self.book, "status": "Pending", "name": ["!=", self.name]})
            
            if not other_reservations:
                book.status = "Available"
                book.save()