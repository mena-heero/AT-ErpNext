import frappe

def get_context(context):
    route = frappe.get_request_header("route")  # Assuming route is passed in header
    topic = frappe.get_doc("Topic", route)
    context["topic"] = topic
    
website_routes = [
    {"routename": "/topics/<route>", "page": "details"},
]