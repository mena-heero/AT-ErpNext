
# import frappe
from frappe.model.document import Document
import frappe
import requests
import logging
import re
from bs4 import BeautifulSoup
import urllib.parse

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
    parsed_url = urllib.parse.urlparse(channel_url)
    path_parts = parsed_url.path.split('/')

    if len(path_parts) >= 3 and path_parts[1] == 'channel':
        channel_id = path_parts[2]
        return channel_id
    elif len(path_parts) >= 2 and path_parts[1] == 'user':
        username = path_parts[2]
        url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&forUsername={username}&key={api_key}"
    else:
        match = re.match(r"https?://(?:www\.)?youtube\.com/(?:c/|@)([^/]+)", channel_url, re.UNICODE)
        if match:
            username = urllib.parse.quote(match.group(1), safe='')
            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&type=channel&q={username}&key={api_key}"
        else:
            logging.error("Invalid YouTube channel URL.")
            return None

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
def update_instagram_followers_count(docname):
    # Fetch the document using docname
    doc = frappe.get_doc("Influencers", docname)
    instagram_link = doc.channel_link

    followers_count = scrape_followers_count(instagram_link)

    if followers_count is not None:
        # Update the read-only field
        doc.insta_followers = followers_count
        doc.save(ignore_permissions=True)
        frappe.msgprint("Instagram followers count updated successfully.")
    else:
        frappe.msgprint("Failed to retrieve Instagram followers count.")


def convert_to_numeric(value):
    if value.endswith('M'):
        return int(float(value[:-1]) * 1000000)
    elif value.endswith('K'):
        return int(float(value[:-1]) * 1000)
    else:
        return int(value.replace(',', ''))


def scrape_followers_count(instagram_link):
    response = requests.get(instagram_link)
    soup = BeautifulSoup(response.text, 'html.parser')

    meta_tag = soup.find('meta', property='og:description')
    if meta_tag is not None:
        content = meta_tag['content']
        followers_count_text = content.split()[0].replace(',', '')
        followers_count = convert_to_numeric(followers_count_text)
        return followers_count
    else:
        return None



@frappe.whitelist()
def transfer_to_lead(docname):
    influencer = frappe.get_doc("Influencers", docname)
    # Check if a lead with the same first_name already exists
    existing_lead = frappe.get_all("Lead", filters={"first_name": influencer.channel_name})

    if existing_lead:
        frappe.msgprint("Lead with the same first name already exists. Transfer aborted.")
        return
    # Create a new Lead document
    lead = frappe.new_doc("Lead")
    lead.first_name = influencer.channel_name
    lead.website = influencer.channel_link
    lead.phone = influencer.phone_number
    lead.inserted_by = influencer.inserted_by

    lead.insert(ignore_permissions=True)

    frappe.msgprint("Influencer transferred to Lead successfully.")