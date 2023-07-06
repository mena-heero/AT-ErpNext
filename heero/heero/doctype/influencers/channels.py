import frappe
import json

@frappe.whitelist()
def update_channels(doc):
    doc = json.loads(doc)
    channel_links = doc.get('channel_link').split('\n')
    child_table = doc.get('channels') or []

    try:
        for link in channel_links:
            channel_link = link.strip()
            if channel_link:
                platform = get_platform_from_link(channel_link)
                existing_channel = next((row for row in child_table if row.get('channel_link') == channel_link), None)

                if not existing_channel:
                    child_row = {
                        'doctype': 'Influencer Channels',
                        'channel_link': channel_link,
                        'platform': platform
                    }
                    child_table.append(child_row)

        doc['channels'] = child_table
        updated_doc = frappe.get_doc(doc)
        updated_doc.set('channels', child_table)
        updated_doc.save()

        frappe.msgprint('Channels updated successfully.')
    except Exception as e:
        frappe.msgprint('Failed to update channels. Error: {}'.format(str(e)))

def get_platform_from_link(link):
    if 'youtube.com' in link or 'youtu.be' in link:
        return 'YouTube'
    elif 'facebook.com' in link:
        return 'Facebook'
    elif 'instagram.com' in link:
        return 'Instagram'
    elif 'tiktok.com' in link:
        return 'TikTok'
    elif 'snapchat.com' in link:
        return 'Snapchat'
    elif 'twitter.com' in link:
        return 'Twitter'
    else:
        return ''
