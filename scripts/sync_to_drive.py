#!/usr/bin/env python3
import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Authenticate
gauth = GoogleAuth()
gauth.service_account_file = '/tmp/credentials.json'
gauth.ServiceAuth()
drive = GoogleDrive(gauth)

folder_id = os.environ['GOOGLE_DRIVE_FOLDER_ID']
files_to_upload = ['PROJECT_STATE.md', 'DECISIONS.md', 'CLAUDE.md']

for filename in files_to_upload:
    if not os.path.exists(filename):
        print(f"Skipping {filename} - not found")
        continue
    
    # Check if file already exists in folder
    file_list = drive.ListFile({
        'q': f"'{folder_id}' in parents and title='{filename}' and trashed=false"
    }).GetList()
    
    if file_list:
        # Update existing file
        file_drive = file_list[0]
        file_drive.SetContentFile(filename)
        file_drive.Upload()
        print(f"Updated {filename}")
    else:
        # Create new file
        file_drive = drive.CreateFile({
            'title': filename,
            'parents': [{'id': folder_id}]
        })
        file_drive.SetContentFile(filename)
        file_drive.Upload()
        print(f"Uploaded {filename}")