from frappe.model.document import Document
import frappe
import re

class Member(Document):
    def validate(self):
        self.validate_email()
        self.validate_phone()
    
    def validate_email(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            frappe.throw("Please enter a valid email address")
    
    def validate_phone(self):
        if self.phone and not re.match(r"^[\d\s\+\-\(\)]+$", self.phone):
            frappe.throw("Please enter a valid phone number")