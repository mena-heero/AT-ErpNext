import frappe
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

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

        # Fetch non-contacted entities in the current document type directly
        non_contacted_entities = frappe.get_all(doc_type, filters={'contacted': 0})

        # Filter out entities without email addresses
        valid_entities = [entity for entity in non_contacted_entities if 'email' in entity and entity['email']]

        # Define the email template for this document type
        email_template = get_email_template(doc_type)

        for entity in valid_entities:
            # Send the specific email using the email template and sender
            sent_successfully = send_email(entity, email_template, sender_email)

            # Log the email send attempt (both success and failure)
            log_email_send(email_template.name, entity['name'], 'Sent' if sent_successfully else 'Failed', 'Email sent successfully' if sent_successfully else 'Failed to send email')

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
        try:
            # Send the email using the email template and sender
            frappe.sendmail(
                recipients=[entity['email']],
                sender=sender_email,  # Use the sender email specified for the document type
                template=email_template.name,  # Use the email template
                doc=entity,  # Pass the entity as the context
            )

            return True  # Email sent successfully
        except Exception as e:
            return False  # Email send failed
    else:
        # Print debug information to understand the entity structure
        print(f"Invalid entity: missing 'email' key. Entity: {entity}")
        return False  # Invalid entity

def log_email_send(template_name, entity_name, action, details):
    try:
        # Create a log entry in the custom doctype
        log_entry = frappe.new_doc("Email Log")
        log_entry.timestamp = datetime.now()
        log_entry.document_type = template_name  # Use the email template name as document type
        log_entry.entity_name = entity_name
        log_entry.action = action
        log_entry.details = details
        log_entry.insert(ignore_permissions=True)  # Insert the log entry without checking permissions
    except Exception as e:
        # Log any errors that occur during log entry creation
        frappe.log_error(f"Failed to create email log entry: {str(e)}", "Custom Cron Error")
