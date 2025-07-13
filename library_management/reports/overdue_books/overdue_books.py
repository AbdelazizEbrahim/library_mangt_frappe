import frappe
from frappe import _
from frappe.utils import nowdate

def execute(filters=None):
    columns = [
        {
            "label": _("Loan ID"),
            "fieldname": "loan_id",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Book"),
            "fieldname": "book",
            "fieldtype": "Link",
            "options": "Book",
            "width": 150
        },
        {
            "label": _("Book Title"),
            "fieldname": "book_title",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Member"),
            "fieldname": "member",
            "fieldtype": "Link",
            "options": "Member",
            "width": 150
        },
        {
            "label": _("Member Name"),
            "fieldname": "member_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Loan Date"),
            "fieldname": "loan_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Return Date"),
            "fieldname": "return_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Days Overdue"),
            "fieldname": "days_overdue",
            "fieldtype": "Int",
            "width": 100
        }
    ]

    today = nowdate()
    data = frappe.db.sql("""
        SELECT 
            l.name, l.loan_id, l.book, b.title as book_title, 
            l.member, m.full_name as member_name, 
            l.loan_date, l.return_date,
            DATEDIFF(%s, l.return_date) as days_overdue
        FROM 
            `tabLoan` l
        JOIN 
            `tabBook` b ON l.book = b.name
        JOIN 
            `tabMember` m ON l.member = m.name
        WHERE 
            l.status = 'Active' AND l.return_date < %s
        ORDER BY 
            days_overdue DESC
    """, (today, today), as_dict=1)

    return columns, data