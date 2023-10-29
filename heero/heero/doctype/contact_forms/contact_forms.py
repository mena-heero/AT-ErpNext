# Copyright (c) 2023, Heero and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document

class ContactForms(Document):
	pass



@frappe.whitelist()
def send_email_to_uncontacted_party(docname=None):
    try:
        if not docname:
            return "No docname provided."

        # Get the selected record based on the provided docname
        doc = frappe.get_doc("Contact Forms", docname)

        # Get the inserted_by value
        inserted_for = doc.inserted_for

        # Define a mapping of inserted_by values to email templates
        email_templates = {
            "Youssef": "Youssef_ColdSales",
            "Heero": "Heero_ColdSales",
            # Add more mappings as needed
        }

        # Check if the inserted_by value exists in the mapping
        if inserted_for in email_templates:
            template_name = email_templates[inserted_for]
            email_template = frappe.get_doc("Email Template", template_name)
            sender = "info@flagedu.com"

            # Customize the email subject, template, and any other parameters as needed
            email_subject = "فلاجيدو : فرصتك للتقدم"

            # Render the email content
            context = {"doc": doc}
            if email_template.use_html:
                email_content = frappe.render_template(email_template.response_html, context)
            else:
                email_content = frappe.render_template(email_template.response, context)

            # Send the email
            frappe.sendmail(
                recipients=[doc.email],
                subject=email_subject,
                message=email_content,
                sender=sender,
                args={"doc": doc}
            )

            # Create a communication record
            communication = frappe.get_doc({
                "doctype": "Communication",
                "subject": email_subject,
                "communication_type": "Communication",
                "communication_medium": "Email",
                "sent_or_received": "Sent",
                "content": email_content,
                "reference_doctype": doc.doctype,
                "reference_name": doc.name,
                "sender": sender,
                "recipients": doc.email,
            })
            communication.insert(ignore_permissions=True)

            # Mark the record as contacted
            doc.contacted = 1
            doc.save()

            return "Email sent successfully."
        else:
            return "No email template found for inserted_by: {0}".format(inserted_by)

    except Exception as e:
        # Handle any exceptions that may occur during email sending
        frappe.log_error(_("Error sending email: {0}").format(str(e)))
        return "Error sending email: {0}".format(str(e))
