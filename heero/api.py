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


