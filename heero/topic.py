import frappe

@frappe.whitelist(allow_guest=True)
def get_topic_page(route):
    topic = frappe.get_doc("Topic", route)
    return frappe.render_template("topic.html", {"topic": topic})


@frappe.whitelist(allow_guest=True)
def get_route():
    return [
        {"route": "/topics/<route>", "method": "heero.get_topic_page"}
    ]
