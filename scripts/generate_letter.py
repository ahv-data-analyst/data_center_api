# import time
# from googleapiclient.discovery import build
# from google.oauth2 import service_account
# import requests
# from database.database_manager import DatabaseManager

# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# import os
# import pickle

# # Setup
# SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive']
# SERVICE_ACCOUNT_FILE = 'credentials.json'
# TEMPLATE_ID = '1BP-0jWHgVNxzpoIexo1fAVLrCv3IrjQfQwn5sf36lPc'
# FOLDER_ID = '1H8rzsQZA1ZxtnxwmtrWvP76CHyFb-qBC'

# def get_credentials():
#     creds = None
#     # token.pickle stores the user's access and refresh tokens
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)
#     return creds

# # Then replace your current 'creds' line with:
# creds = get_credentials()
# drive_service = build('drive', 'v3', credentials=creds)
# slides_service = build('slides', 'v1', credentials=creds)

# # This is how your data from the database should look
# data_from_db = []

# def get_data():
#     response = requests.get('http://127.0.0.1:8000/assessments/assessments')
#     query = "SELECT province, country_of_attendance, branch FROM trsh_membership_numbers WHERE name=? and surname=?"
    
#     for i in response.json():
#         if i['pass_fail'] == 'PASS' and i['unique_code'] != 'WAITING':
#             with DatabaseManager('data/ahv_data.db') as db:
#                 data = db.connection.execute(query, (i['name'], i['surname'])).fetchone()
                
#                 if not data:
#                     continue
                
#                 data_from_db.append({
#                     'membership_number': i['membership_number'],
#                     'unique_id': i['unique_code'],
#                     'centre': data[2] + "/" + data[0] + "/" + data[1],
#                     'name': f'{i['name']} {i['surname']}',
#                     'assessment_date': i['assessment_date'],
#                 })
    
# get_data()

# import json
# import os
# import time
# from googleapiclient.discovery import build
# # ... (rest of your imports)

# LOG_FILE = 'created_letters.json'

# def load_processed_ids():
#     """Loads the list of already created IDs from a JSON file."""
#     if os.path.exists(LOG_FILE):
#         with open(LOG_FILE, 'r') as f:
#             try:
#                 return set(json.load(f))
#             except json.JSONDecodeError:
#                 return set()
#     return set()

# def save_processed_id(unique_id):
#     """Adds a new ID to the JSON log file."""
#     processed_ids = list(load_processed_ids())
#     processed_ids.append(unique_id)
#     with open(LOG_FILE, 'w') as f:
#         json.dump(processed_ids, f, indent=4)
        
# import io
# from googleapiclient.http import MediaIoBaseDownload

# def download_as_pdf(file_id, filename):
#     # Request the PDF export from Google Drive
#     request = drive_service.files().export_media(fileId=file_id, mimeType='application/pdf')
#     fh = io.FileIO(f"output_pdfs/{filename}.pdf", 'wb')
#     downloader = MediaIoBaseDownload(fh, request)
#     done = False
#     while done is False:
#         status, done = downloader.next_chunk()
#     print(f"📄 Downloaded PDF: {filename}")

# def generate_tskh_letters(data_list):
#     # 1. Load existing progress
#     already_processed = load_processed_ids()
#     print(f"Loaded {len(already_processed)} existing records. Starting run...")

#     for entry in data_list:
#         u_id = str(entry['unique_id'])

#         # 2. Skip if we've already done this one
#         if u_id in already_processed:
#             print(f"⏩ Skipping {entry['name']} (ID: {u_id}) - already exists.")
#             continue

#         try:
#             # 3. Create descriptive filename
#             copy_title = f"Progression Letter - {entry['name']} ({entry['assessment_date']})"
            
#             body = {'name': copy_title, 'parents': [FOLDER_ID]}
#             new_file = drive_service.files().copy(fileId=TEMPLATE_ID, body=body).execute()
#             presentation_id = new_file.get('id')

#             # 4. Define replacements
#             requests = [
#                 {'replaceAllText': {'replaceText': str(entry['membership_number']), 'containsText': {'text': '{{membership_number}}'}}},
#                 {'replaceAllText': {'replaceText': u_id, 'containsText': {'text': '{{unique_id}}'}}},
#                 {'replaceAllText': {'replaceText': str(entry['name']), 'containsText': {'text': '{{name}}'}}},
#                 {'replaceAllText': {'replaceText': str(entry['assessment_date']), 'containsText': {'text': '{{assessment_date}}'}}},
#                 {'replaceAllText': {'replaceText': entry['centre'], 'containsText': {'text': '{{centre}}'}}},
#             ]

#             slides_service.presentations().batchUpdate(
#                 presentationId=presentation_id,
#                 body={'requests': requests}
#             ).execute()
            
#             # download_as_pdf(presentation_id, copy_title)

#             # 5. Success! Log it so we don't repeat it
#             save_processed_id(u_id)
#             print(f"✅ Created: {copy_title}")
            
#             time.sleep(1.2) 

#         except Exception as e:
#             print(f"❌ Error on {entry['name']}: {e}")
#             print(entry)
#             # Optional: Stop script on serious errors
#             if "quota" in str(e).lower():
#                 print("Quota exceeded. Stopping script.")
#                 break
            
# generate_tskh_letters(data_from_db)


# import io
# import os
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload
# # ... include your get_credentials() function here ...

# def download_existing_letters():
#     creds = get_credentials()
#     drive_service = build('drive', 'v3', credentials=creds)
    
#     # Create local folder if it doesn't exist
#     if not os.path.exists('to_print'):
#         os.makedirs('to_print')

#     # 1. List all files in your Google Drive destination folder
#     results = drive_service.files().list(
#         q=f"'{FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.presentation'",
#         fields="files(id, name)"
#     ).execute()
#     items = results.get('files', [])

#     if not items:
#         print('No slides found in the folder.')
#         return

#     print(f"Found {len(items)} letters. Starting download...")

#     for item in items:
#         file_id = item['id']
#         file_name = item['name'].replace("/", "-") # Clean filename
        
#         # 2. Export to PDF
#         request = drive_service.files().export_media(
#             fileId=file_id, 
#             mimeType='application/pdf'
#         )
        
#         fh = io.FileIO(f"to_print/{file_name}.pdf", 'wb')
#         downloader = MediaIoBaseDownload(fh, request)
        
#         done = False
#         while done is False:
#             status, done = downloader.next_chunk()
        
#         print(f"✅ Downloaded: {file_name}.pdf")

# # Run it
# download_existing_letters()

import os
import io
import time
import pickle
import json
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pypdf import PdfWriter
from database.database_manager import DatabaseManager

# Setup
SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive']
TEMPLATE_ID = '1BP-0jWHgVNxzpoIexo1fAVLrCv3IrjQfQwn5sf36lPc'
FOLDER_ID = '1H8rzsQZA1ZxtnxwmtrWvP76CHyFb-qBC'
LOG_FILE = 'created_letters.json'
OUTPUT_BASE_DIR = 'daily_letters'

def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

creds = get_credentials()
drive_service = build('drive', 'v3', credentials=creds)
slides_service = build('slides', 'v1', credentials=creds)

def load_processed_ids():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            try: return set(json.load(f))
            except: return set()
    return set()

def save_processed_id(unique_id):
    processed_ids = list(load_processed_ids())
    processed_ids.append(unique_id)
    with open(LOG_FILE, 'w') as f:
        json.dump(processed_ids, f, indent=4)

def get_data_grouped_by_date():
    """Groups database results by date: { '14-04-2026': [user1, user2], ... }"""
    response = requests.get('http://127.0.0.1:8000/assessments/assessments')
    query = "SELECT province, country_of_attendance, branch FROM trsh_membership_numbers WHERE name=? and surname=?"
    
    grouped_data = {}
    
    for i in response.json():
        if i['pass_fail'] == 'PASS' and i['unique_code'] != 'WAITING':
            with DatabaseManager('data/ahv_data.db') as db:
                data = db.connection.execute(query, (i['name'], i['surname'])).fetchone()
                if not data: continue
                
                # Format date to be filename friendly (replace / with -)
                date_key = i['assessment_date'].replace('/', '-')
                
                entry = {
                    'membership_number': i['membership_number'],
                    'unique_id': i['unique_code'],
                    'centre': f"{data[2]}/{data[0]}/{data[1]}",
                    'name': f"{i['name']} {i['surname']}",
                    'assessment_date': i['assessment_date'],
                }
                
                if date_key not in grouped_data:
                    grouped_data[date_key] = []
                grouped_data[date_key].append(entry)
    return grouped_data

def download_pdf_content(file_id):
    request = drive_service.files().export_media(fileId=file_id, mimeType='application/pdf')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.seek(0)
    return fh

def process_batches():
    grouped_data = get_data_grouped_by_date()
    already_processed = load_processed_ids()

    if not os.path.exists(OUTPUT_BASE_DIR):
        os.makedirs(OUTPUT_BASE_DIR)

    for date_str, users in grouped_data.items():
        print(f"\n📅 Processing Date: {date_str} ({len(users)} users)")
        merger = PdfWriter()
        files_added_to_pdf = 0

        for entry in users:
            u_id = str(entry['unique_id'])
            if u_id in already_processed:
                print(f"⏩ Skipping {entry['name']} - already processed.")
                continue

            try:
                # 1. Create Slide
                copy_title = f"Temp_{u_id}"
                body = {'name': copy_title, 'parents': [FOLDER_ID]}
                new_file = drive_service.files().copy(fileId=TEMPLATE_ID, body=body).execute()
                presentation_id = new_file.get('id')

                # 2. Fill Placeholders
                replacements = [
                    {'replaceAllText': {'replaceText': entry['membership_number'], 'containsText': {'text': '{{membership_number}}'}}},
                    {'replaceAllText': {'replaceText': u_id, 'containsText': {'text': '{{unique_id}}'}}},
                    {'replaceAllText': {'replaceText': entry['name'], 'containsText': {'text': '{{name}}'}}},
                    {'replaceAllText': {'replaceText': entry['assessment_date'], 'containsText': {'text': '{{assessment_date}}'}}},
                    {'replaceAllText': {'replaceText': entry['centre'], 'containsText': {'text': '{{centre}}'}}},
                ]
                slides_service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': replacements}).execute()

                # 3. Download to Memory & Append to PDF Merger
                pdf_stream = download_pdf_content(presentation_id)
                merger.append(pdf_stream)
                files_added_to_pdf += 1

                # 4. Clean up: Delete temp slide from Drive
                drive_service.files().delete(fileId=presentation_id).execute()
                
                save_processed_id(u_id)
                print(f"✅ Added {entry['name']} to {date_str} batch")
                time.sleep(1.2) # Avoid rate limits

            except Exception as e:
                print(f"❌ Error on {entry['name']}: {e}")

        # 5. Save the Master PDF for this date
        if files_added_to_pdf > 0:
            output_filename = f"progression letters - {date_str}.pdf"
            with open(os.path.join(OUTPUT_BASE_DIR, output_filename), "wb") as f:
                merger.write(f)
            print(f"💾 SAVED MASTER PDF: {output_filename}")
        merger.close()

if __name__ == "__main__":
    process_batches()