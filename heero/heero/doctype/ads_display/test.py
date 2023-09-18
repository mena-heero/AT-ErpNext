# Copyright (c) 2023, Heero and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class AdsDisplay(Document):
   pass


@frappe.whitelist()
def send_email_to_uncontacted_party(docname):
    # Get the record based on the provided docname
    doc = frappe.get_doc("Ads Display", docname)

    # Check if the record has not been contacted
    if not doc.contacted:
        try:
            # Customize the email subject and sender
            email_subject = "Get More Customers/Advertise With Us"
            sender = "ads@alltargeting.com"

            # Determine the email template based on inserted_by
            inserted_by = doc.inserted_by
            template_name = ""

            # Define mappings from inserted_by to email templates
            template_mappings = {
                "Marina": "Display",
                "Shahinda": "Ads",
                # Add more mappings as needed
            }

            # Check if inserted_by has a mapping to a template
            if inserted_by in template_mappings:
                template_name = template_mappings[inserted_by]
            else:
                # If there's no specific mapping, use a default template
                template_name = "Ads"

            # Fetch the email template
            email_template = frappe.get_doc("Email Template", template_name)

            # Send the email
            try:
                frappe.sendmail(
                    recipients=[doc.email],
                    subject=email_subject,
                    template=email_template.name,
                    sender=sender,
                    args={"doc": doc}
                )
            except Exception as e:
                # Handle the error when the email template is not found or other sendmail issues
                frappe.log_error(f"Error sending email: {str(e)}")
                return f"Error sending email: {str(e)}"

            # Get the email content
            email_content = email_template.response

            # Create a communication record with the email content
            communication = frappe.get_doc({
                "doctype": "Communication",
                "subject": email_subject,
                "communication_type": "Communication",
                "communication_medium": "Email",
                "sent_or_received": "Sent",
                "content": email_template.name,
                "reference_doctype": doc.doctype,
                "reference_name": doc.name,
                "sender": sender,
                "recipients": doc.email,
            })
            communication.insert(ignore_permissions=True)

            # If the email is sent successfully, mark 'contacted' as True
            doc.contacted = 1
            doc.save()

            return "Email sent successfully."

        except Exception as e:
            # Handle any exceptions that may occur during email sending
            frappe.log_error(_("Error sending email: {0}").format(str(e)))
            return "Error sending email: {0}".format(str(e))
    else:
        return "Record has already been contacted."
