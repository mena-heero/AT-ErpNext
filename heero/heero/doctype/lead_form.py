import frappe
from frappe import _

@frappe.whitelist()
def create_lead(data):
    try:
        # Extract form data from 'data' argument and process as needed
        form_dict = frappe.parse_json(data)

        name = form_dict.get('name')
        email = form_dict.get('email')
        message = form_dict.get('message')

        # Perform lead creation logic here using Frappe's API or ORM
        # For example:
        lead = frappe.new_doc('Lead')
        lead.lead_name = name
        lead.email_id = email
        lead.set('notes', [])  # Initialize notes as an empty list
        lead.append('notes', {
            'doctype': 'Note',
            'content': message
        })
        lead.insert(ignore_permissions=True)

        return _("Lead created successfully!")
    except Exception as e:
        frappe.log_error(_('Lead Creation Error'), message=str(e))
        frappe.throw(_("Lead creation failed. Please try again."))
