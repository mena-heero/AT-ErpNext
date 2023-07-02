import frappe
import requests
from bs4 import BeautifulSoup

@frappe.whitelist()
def update_facebook_followers_count(docname):
    # Fetch the document using docname
    doc = frappe.get_doc("Influencers", docname)
    facebook_link = doc.channel_link

    followers_count = scrape_facebook_followers_count(facebook_link)

    if followers_count is not None:
        # Update the read-only field
        doc.facebook_followers = followers_count
        doc.save(ignore_permissions=True)
        frappe.msgprint("Facebook followers count updated successfully.")
    else:
        frappe.msgprint("Failed to retrieve Facebook followers count.")

def scrape_facebook_followers_count(facebook_link):
    response = requests.get(facebook_link)
    soup = BeautifulSoup(response.text, 'html.parser')

    followers_tag = soup.select_one('a.x1i10hfl[href*="/followers/"]')
    if followers_tag:
        followers_count_text = followers_tag.text.strip()
        followers_count = convert_to_numeric(followers_count_text)
        return followers_count

    return None

def convert_to_numeric(value):
    if value.endswith('M'):
        return int(float(value[:-1]) * 1000000)
    elif value.endswith('K'):
        return int(float(value[:-1]) * 1000)
    else:
        return int(value.replace(',', ''))
