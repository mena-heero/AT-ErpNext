
# import frappe
from frappe.model.document import Document
import frappe
import requests
import logging
import re


class Influencers(Document):
	pass


@frappe.whitelist()
def update_subscriber_count(docname):
    # Fetch the document using docname
    doc = frappe.get_doc("Influencers", docname)
    channel_url = doc.channel_link
    api_key = "AIzaSyApNaEBngNrM394RSGV2q-9oOxl7WV-EPo"  # Replace with your YouTube API key

    subscriber_count = get_subscriber_count(channel_url, api_key)

    if subscriber_count is not None:
        # Update the read-only field
        doc.subcs = subscriber_count  # Update 'subcs' field with subscriber_count
        doc.save(ignore_permissions=True)
        frappe.msgprint("Subscriber count updated successfully.")
    else:
        frappe.msgprint("Failed to retrieve subscriber count.")


def get_channel_id(channel_url, api_key):
    match = re.match(r"https://www.youtube.com/(?:c/|@)([^/]+)", channel_url)
    if match:
        username = match.group(1)
    else:
        logging.error("Invalid YouTube channel URL.")
        return None

    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&type=channel&q={username}&key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'items' in data and len(data['items']) > 0:
            channel_id = data['items'][0]['snippet']['channelId']
            return channel_id
        else:
            logging.error("No channel ID found in API response.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error retrieving channel ID: {e}")

    return None


def get_subscriber_count(channel_url, api_key):
    channel_id = get_channel_id(channel_url, api_key)
    if not channel_id:
        return None

    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'items' in data:
            subscriber_count = data['items'][0]['statistics']['subscriberCount']
            return subscriber_count
        else:
            logging.error("No 'items' key found in API response.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error retrieving subscriber count: {e}")
    except (KeyError, IndexError) as e:
        logging.error(f"Error parsing API response: {e}")

    return None




@frappe.whitelist()
def transfer_to_lead(docname):
    influencer = frappe.get_doc("Influencers", docname)

    # Create a new Lead document
    lead = frappe.new_doc("Lead")
    lead.first_name = influencer.channel_name
    lead.website = influencer.channel_link
    lead.phone = influencer.phone_number
    lead.inserted_by = influencer.inserted_by

    lead.insert(ignore_permissions=True)

    frappe.msgprint("Influencer transferred to Lead successfully.")