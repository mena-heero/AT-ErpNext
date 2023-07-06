import frappe
from frappe.utils.file_manager import save_file
import os
from .images import download_images_from_drive_folder

def attach_images_to_existing_influencers():
    save_directory = "/home/heero/at/sites/images"

    influencer_docs = frappe.get_all("Influencers", filters={"statistics": ("!=", "")}, pluck="name")

    for influencer_docname in influencer_docs:
        download_images_from_drive_folder(frappe.get_value("Influencers", influencer_docname, "statistics"), save_directory)
        attach_downloaded_images_to_influencer(influencer_docname, save_directory)

def attach_downloaded_images_to_influencer(influencer_docname, save_directory):
    image_files = [f for f in os.listdir(save_directory) if os.path.isfile(os.path.join(save_directory, f))]

    for image_file in image_files:
        file_path = os.path.join(save_directory, image_file)
        try:
            with open(file_path, 'rb') as file:
                save_file(image_file, file.read(), "Influencers", influencer_docname)
        except frappe.ValidationError as e:
            frappe.throw(str(e))
