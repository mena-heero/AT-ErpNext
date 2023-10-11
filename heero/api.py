import frappe
from frappe import _

import frappe

@frappe.whitelist(allow_guest=True)
def check_customer_existence(customer_name):
    customer_exists = frappe.get_all("Customer", filters={"customer_name": customer_name})
    
    if customer_exists:
        return {"customer_exists": True}
    else:
        return {"customer_exists": False}




@frappe.whitelist(allow_guest=True)
def create_customer():
    try:
        # Extract customer data from the request (you might need to adjust this)
        data = frappe.request.json
        customer_name = data.get('customer_name')
        customer_type = data.get('customer_type')
        # Add other fields as needed
        
        # Create a new customer document
        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": customer_name,
            "customer_type": customer_type,
            # Add other fields here
        })
        customer.insert()

        return {"message": "Customer created successfully"}
    except Exception as e:
        return {"error": _("Error creating customer: {0}").format(str(e))}



@frappe.whitelist(allow_guest=True)
def create_lead_with_message():
    try:
        # Extract lead data from the request (you might need to adjust this)
        data = frappe.request.json
        lead_name = data.get('name')
        lead_description = data.get('message')
        # Add other fields as needed
        email_id=data.get('email')
        notes_html=data.get('message')
        
        # Create a new lead document
        lead = frappe.get_doc({
            "doctype": "Lead",
            "lead_name": lead_name,
            "lead_description": lead_description,
            "email_id":email_id,
            "notes_html":notes_html
            # Add other fields here
        })
        lead.insert()

        return {"message": "Lead created successfully"}
    except Exception as e:
        return {"error": _("Error creating lead: {0}").format(str(e))}


@frappe.whitelist()
def get_topic_detail(topic_route):
    topic = frappe.get_doc("Topic", {"route": topic_route})
    return {"topic": topic}


@frappe.whitelist(allow_guest=True)
def lead_at():
    try:
        # Extract lead data from the request (you might need to adjust this)
        data = frappe.request.json
        lead_name = data.get('name')
        lead_description = data.get('message')
        # Add other fields as needed
        email=data.get('email')
        phone=data.get('phone')
        
        
        # Create a new lead document
        lead = frappe.get_doc({
            "doctype": "Alltargeting Leads",
            "name1": lead_name,
            "message": lead_description,
            "email":email,
            "phone":phone,
            
            # Add other fields here
        })
        lead.insert(ignore_permissions=True)
        return {"message": "Thank You for contacting us"}
    except Exception as e:
        return {"error": _("Error creating lead: {0}").format(str(e))}


@frappe.whitelist(allow_guest=True)
def flagedu_lead():
    try:
        # Extract lead data from the request (you might need to adjust this)
        data = frappe.request.json
        lead_name = data.get('name')
        lead_description = data.get('message')
        # Add other fields as needed
        email=data.get('email')
        phone=data.get('phone')
        
        
        # Create a new lead document
        lead = frappe.get_doc({
            "doctype": "Flagedu-Lead",
            "name1": lead_name,
            "message": lead_description,
            "email":email,
            "phone":phone,
            
            # Add other fields here
        })
        lead.insert(ignore_permissions=True)
        return {"message": "Thank You for contacting us"}
    except Exception as e:
        return {"error": _("Error creating lead: {0}").format(str(e))}
