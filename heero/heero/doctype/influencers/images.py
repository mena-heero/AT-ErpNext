import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
from urllib.parse import urlparse

def download_images_from_drive_folder(folder_link, save_directory):
    # Extract the folder ID from the link
    parsed_url = urlparse(folder_link)
    path_parts = parsed_url.path.split('/')
    folder_id = path_parts[-1] if path_parts[-1] else path_parts[-2]

    if not folder_id:
        raise ValueError("Invalid folder link format")

    credentials = Credentials.from_service_account_file('/home/heero/at/apps/heero/heero/heero/doctype/influencers/account-keys.json')
    # Initialize the Drive API client
    drive_service = build('drive', 'v3', credentials=credentials)

    # Get the folder name
    folder = drive_service.files().get(fileId=folder_id, fields='name').execute()
    folder_name = folder.get('name')

    # Rest of the code...


    # Get the list of files within the folder
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and mimeType contains 'image/'",
        fields='files(id, name)',
        pageSize=1000
    ).execute()

    files = results.get('files', [])

    # Create the save directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

    # Download each image with custom names
    for index, file in enumerate(files, start=1):
        image_id = file['id']
        image_name = file['name']
        custom_name = f"{folder_name}{index}"  # Modify the name as desired

        request = drive_service.files().get_media(fileId=image_id)
        file_path = os.path.join(save_directory, custom_name)

        with open(file_path, 'wb') as file:
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Downloading {custom_name}... {int(status.progress() * 100)}%")


