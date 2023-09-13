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
            # Customize the email subject, template, and any other parameters as needed
            email_subject = "إمكانية الإعلان على موقعك"
            template_name = "Ads Display"
            email_template = frappe.get_doc("Email Template", template_name)
            sender = "contact@alltargeting.com"

            # Send the email
            frappe.sendmail(
                recipients=[doc.email],
                subject=email_subject,
                template=email_template.name,
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
                "content": email_template.name,  # You can customize this as needed
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
