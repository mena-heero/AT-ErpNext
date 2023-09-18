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
            email_subject = "Get More Customers/Advertise With Us"
            template_name = "Ads"
            email_template = frappe.get_doc("Email Template", template_name)
            sender = "ads@alltargeting.com"

            # Render the email content
            context = {"doc": doc}
            email_content = frappe.render_template(email_template.response, context)
            print(email_content)
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
                "content": email_content,
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
