import frappe
from frappe.utils import nowdate, get_url
from frappe.core.doctype.communication.email import make

def daily():
    check_overdue_loans()

def check_overdue_loans():
    """Check for overdue loans and send notifications"""
    today = nowdate()
    overdue_loans = frappe.get_all("Loan",
        filters={
            "status": "Active",
            "return_date": ["<", today]
        },
        fields=["name", "book", "member", "return_date"]
    )
    
    for loan in overdue_loans:
        # Update status to Overdue
        frappe.db.set_value("Loan", loan.name, "status", "Overdue")
        
        # Get member details
        member = frappe.get_doc("Member", loan.member)
        book = frappe.get_doc("Book", loan.book)
        
        # Send email notification
        subject = f"Overdue Book: {book.title}"
        message = f"""
            <p>Dear {member.full_name},</p>
            <p>The book <strong>{book.title}</strong> by {book.author} is overdue.</p>
            <p>It was due on {loan.return_date}. Please return it as soon as possible.</p>
            <p>Thank you,</p>
            <p>The Library Team</p>
        """
        
        make(
            subject=subject,
            content=message,
            recipients=member.email,
            send_email=True,
            sender=frappe.db.get_value("Email Account", {"default_outgoing": 1}, "email_id")
        )