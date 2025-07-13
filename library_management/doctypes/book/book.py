from frappe.model.document import Document

class Book(Document):
    def before_save(self):
        # Validate ISBN format (simple check)
        if not self.isbn or len(self.isbn) < 10:
            frappe.throw("ISBN must be at least 10 characters long")