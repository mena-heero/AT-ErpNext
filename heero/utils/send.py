import frappe
from frappe import _
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

def send():

  # List of document types 
  doc_types = [
    {'type': 'Ads Display', 'sender': 'ads@example.com'},
    {'type': 'Advertiser', 'sender': 'ads@example.com'},
    {'type': 'MCN Data', 'sender': 'mcn@example.com'}
  ]

  for doc_type in doc_types:
    
    # Validate doc type
    if not frappe.db.exists('DocType', doc_type['type']):
      print(_('Invalid doctype: {0}').format(doc_type['type']))
      continue

    # Get email template
    template = get_email_template(doc_type['type'])
    if not template:
      continue

    # Get valid entities
    entities = get_valid_entities(doc_type['type'])

    for entity in entities:
    
      # Send email  
      sent = send_email(entity, template, doc_type['sender'])
 
      # Log send result
      log_send_result(entity, template.name, sent)

def get_email_template(doc_type):

  if not frappe.db.exists('DocType', doc_type):
    print(_('Invalid doctype: {0}').format(doc_type))
    return

  template_name = get_template_name(doc_type)
  if not template_name:
    print(_('No template found for {0}').format(doc_type))
    return

  try:
    template = frappe.get_doc('Email Template', template_name)
    return template
  
  except Exception as e:
    print(_('Error getting template {0}: {1}').format(template_name, e))

def get_template_name(doc_type):

  # Map doc types to template names
  template_map = {
    'Ads Display': 'Display ADS',
    'Advertiser': 'Ads Branding',
    'MCN Data': 'MCN YouTube Partner' 
  }

  return template_map.get(doc_type)

def get_valid_entities(doc_type):
  
  try:
    entities = frappe.get_all(doc_type,  
      fields=['name', 'email'],
      filters={'contacted': 0}
    )

  except Exception as e:
    print(_('Error getting {0} entities: {1}').format(doc_type, e))
    return []

  valid = []
  for entity in entities:
    if 'email' in entity and entity['email']:
      email = entity['email']
      if validate_email(email):
        valid.append(entity)

  return valid

def validate_email(email):

  # Check for None
  if email is None:
    return False

  # Simple validation
  if '@' in email:
    return True

  return False

def send_email(entity, template, sender):

  try:
    frappe.sendmail(
      recipients=[entity['email']],
      sender=sender,
      template=template.name,  
      
    )
    return True

  except Exception as e:
    print(_('Error sending to {0}: {1}').format(entity['email'], e))
    return False

def log_send_result(entity, template, sent):

  # Log send result
  status = _('Sent') if sent else _('Failed')
  message = _('Email sent successfully') if sent else _('Failed to send email')

  try:
    log = frappe.new_doc('Email Log')
    log.entity_name = entity['name']
    log.document_type = template
    log.action = status 
    log.details = message
    log.insert()

  except Exception as e:
    print(_('Error logging email result: {0}').format(e))