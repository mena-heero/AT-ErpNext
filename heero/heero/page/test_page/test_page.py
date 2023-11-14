import frappe




def get_context(context):
    context.docs=frappe.get_list("ToDo",
                      fields=["name", "description"],
                    filters = {"Allocated to":"mena.riyad17@gmail.com"})