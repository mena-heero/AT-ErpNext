import random
import frappe
from frappe.model.document import Document
from frappe import _



class MCNData(Document):
	pass


@frappe.whitelist()
def send_email_to_uncontacted_MCN():
    """
    Sends an email to an uncontacted MCN Data record, selected randomly from the list of uncontacted records.
    The email template used is based on the inserted_by value of the selected record.
    If no email template is found for the inserted_by value, a default email template is used.
    After sending the email, a communication record is created and the selected record is marked as contacted.
    """
    try:
        # Query uncontacted records in the "Ads Display" document type
        uncontacted_records = frappe.get_list("MCN Data", filters={"contacted": 0})

        # Check if there are any uncontacted records
        if uncontacted_records:
            # Randomly select one uncontacted record
            selected_record = random.choice(uncontacted_records)

            # Get the selected record's docname
            docname = selected_record["name"]

            # Get the selected record based on the docname
            doc = frappe.get_doc("MCN Data", docname)

            # Get the inserted_by value
            inserted_by = doc.inserted_by

            # Define a mapping of inserted_by values to email templates
            email_templates = {
                "Marina": "mark_MCN",
                "Shahinda": "mark_MCN",
                "Nairaa": "mark_MCN",
                "Mark": "mark_MCN",
                "others": "mark_MCN",
                # Add default email template here
            
            }

            # Check if the inserted_by value exists in the mapping
            if inserted_by in email_templates:
                template_name = email_templates[inserted_by]
                email_template = frappe.get_doc("Email Template", template_name)
                sender = "info@alltargeting.com"
           

                
                # Customize the email subject, template, and any other parameters as needed
                email_subject = "Increase your subscribers and revenue - Partner with YouTube"

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
        else:
            return "No uncontacted records found."

    except Exception as e:
        # Handle any exceptions that may occur during email sending
        frappe.log_error(_("Error sending email: {0}").format(str(e)))
        return "Error sending email: {0}".format(str(e))
