import frappe
from frappe.utils.file_manager import save_file
import os
from .images import download_images_from_drive_folder

@frappe.whitelist()
def download_images_for_influencer(influencer_docname):
    # Get the folder link from the Influencer doc
    folder_link = frappe.get_value("Influencers", influencer_docname, "statistics")
    
    # Specify the save directory path
    save_directory = "/home/heero/at/sites/images"

    try:
        if folder_link:
            # Download images from the Google Drive folder
            download_images_from_drive_folder(folder_link, save_directory)

            # Attach downloaded images to the Influencer doc
            attach_downloaded_images_to_influencer(influencer_docname, save_directory)

            return "Attachment of downloaded images completed successfully!"
        else:
            return "No folder link found in the Influencer document."

    except Exception as e:
        frappe.throw(str(e))

def attach_downloaded_images_to_influencer(influencer_docname, save_directory):
    # Get the list of downloaded image files
    image_files = [f for f in os.listdir(save_directory) if os.path.isfile(os.path.join(save_directory, f))]

    # Attach each image file to the Influencer doc
    for image_file in image_files:
        # Check if the image file name starts with the influencer's folder name
        if image_file.startswith(influencer_docname):
            file_path = os.path.join(save_directory, image_file)
            try:
                with open(file_path, 'rb') as file:
                    save_file(image_file, file.read(), "Influencers", influencer_docname)
            except frappe.ValidationError as e:
                frappe.throw(str(e))