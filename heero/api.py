import frappe
from frappe import _



#test routes for topic
@frappe.whitelist()
def get_topic_detail(topic_route):
    topic = frappe.get_doc("Topic", {"route": topic_route})
    return {"topic": topic}


#leads for alltargeting contact us
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

#Flagedu Leads API
@frappe.whitelist(allow_guest=True)
def flagedu_lead():
    try:
        # Extract lead data from the request (you might need to adjust this)
        data = frappe.request.json
        name = data.get('name1')
        message = data.get('message')
        # Add other fields as needed
        email=data.get('email')
        phone=data.get('phone')
        country=data.get('country')
        company=data.get('company')
        interest=data.get('interest')
        source=data.get('source')
        client_id=data.get('client_id')
        afp=data.get('afp')
        
        # Create a new lead document
        lead = frappe.get_doc({
            "doctype": "Flagedu-Lead",
            "name1": name,
            "message": message,
            "email":email,
            "phone":phone,
            "country":country,
            "company":company,
            "status":"New",
            "interest":interest,
            "source":source,
            "client_id":client_id,
            "afp":afp
            # Add other fields here
        })
        lead.insert(ignore_permissions=True)
        return {"message": "Flagedu Lead Created"}
    except Exception as e:
        return {"error": _("Error creating lead: {0}").format(str(e))}
