# Copyright (c) 2023, Heero and contributors
# For license information, please see license.txt

# import frappe

from frappe.model.document import Document
import frappe
import requests
import logging
import re

class Advertiser(Document):
	pass



@frappe.whitelist()
def transfer_to_lead(docname):
    advertiser = frappe.get_doc("Advertiser", docname)
    # Check if a lead with the same first_name already exists
    existing_lead = frappe.get_all("Lead", filters={"first_name": advertiser.website})

    if existing_lead:
        frappe.msgprint("Lead with the same first name already exists. Transfer aborted.")
        return
    # Create a new Lead document
    lead = frappe.new_doc("Lead")
    lead.first_name = advertiser.website
    lead.website = advertiser.website
    lead.phone = advertiser.phone
    lead.email = advertiser.email
    lead.inserted_by = advertiser.inserted_by

    lead.insert(ignore_permissions=True)

    frappe.msgprint("advertiser transferred to Lead successfully.")