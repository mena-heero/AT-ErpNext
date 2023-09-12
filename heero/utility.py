import frappe
from frappe.email import sendmail
from datetime import datetime

def execute_hourly():
    # List of document types to process, along with their corresponding sender email addresses
    document_types = [
        {'type': 'Ads Display', 'sender': 'ads@alltargeting.com'},
        {'type': 'Advertiser', 'sender': 'contact@alltargeting.com'},
        {'type': 'MCN Data', 'sender': 'info@alltargeting.com'},
    ]

    # Loop through the specified document types
    for doc_info in document_types:
        doc_type = doc_info['type']
        sender_email = doc_info['sender']

        # Fetch non-contacted entities in the current document type
        non_contacted_entities = frappe.get_all(doc_type, filters={'contacted': 0})

        # Define the email template for this document type
        email_template = get_email_template(doc_type)

        for entity in non_contacted_entities:
            # Send the specific email using the email template and sender
            sent_successfully = send_email(entity, email_template, sender_email)

            if sent_successfully:
                # Mark the entity as contacted
                doc = frappe.get_doc(entity['doctype'], entity['name'])
                doc.contacted = 1
                doc.save()

                # Log the successful email send
                log_email_send(doc_type, entity['name'], 'Sent', 'Email sent successfully')

def get_email_template(doc_type):
    # Define a mapping of document types to email template names
    template_mapping = {
        'Ads Display': 'Display ADS',
        'Advertiser': 'Ads Branding',
        'MCN Data': 'MCN YouTube Partner',
    }

    # Get the template name based on the document type
    template_name = template_mapping.get(doc_type)

    if not template_name:
        # Handle the case where no template is found for the document type
        frappe.log_error(f"No email template found for {doc_type}", "Custom Cron Error")
        return None

    # Fetch the email template from ERPNext
    email_template = frappe.get_doc('Email Template', template_name)

    return email_template

def send_email(entity, email_template, sender_email):
    # Ensure that the entity has an email address
    if 'email' in entity and entity['email']:
        # Send the email using the email template and sender
        try:
            sendmail(
                recipients=[entity['email']],
                sender=sender_email,  # Use the sender email specified for the document type
                template=email_template.name,  # Use the email template
                doc=entity,  # Pass the entity as the context
            )

            # Log the successful email send
            log_email_send(entity['doctype'], entity['name'], 'Sent', 'Email sent successfully')

            return True  # Email sent successfully
        except Exception as e:
            # Log the email send failure
            log_email_send(entity['doctype'], entity['name'], 'Failed', f"Failed to send email: {str(e)}")
            return False  # Email send failed
    else:
        frappe.log_error(f"No valid email address found for {entity['doctype']} ({entity['name']})", "Custom Cron Error")
        return False  # No valid email address

def log_email_send(doc_type, entity_name, action, details):
    # Create a log entry in the custom doctype
    log_entry = frappe.get_doc({
        "doctype": "Email Log",
        "timestamp": datetime.now(),
        "document_type": doc_type,
        "entity_name": entity_name,
        "action": action,
        "details": details,
    })
    log_entry.insert()
