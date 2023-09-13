import frappe
from frappe import _
from frappe.utils import nowdate

# Define the API endpoint
@frappe.whitelist(allow_guest=True)
def submit_contact_form(name, email, subject, message):
    # Create a new Contact document in CRM
    contact = frappe.get_doc({
        "doctype": "Contact",
        "first_name": name,
        "email_id": email,
        "contact_type": "Lead",
        "lead_name": subject,
        "lead_description": message,
        "lead_status": "Open",
        "creation": nowdate(),
        "source": "Website Contact Form"
    })
    contact.insert(ignore_permissions=True)

    # Return success response
    return {"message": "Form submitted successfully"}