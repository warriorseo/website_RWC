import os
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv(r'd:\AI-Cyborg-2558\00_agents\.env')

private_key = os.environ.get('GOOGLE_PRIVATE_KEY', '').replace('\\n', '\n')
credentials_info = {
    'type': os.environ.get('GOOGLE_SERVICE_ACCOUNT_TYPE'),
    'project_id': os.environ.get('GOOGLE_PROJECT_ID'),
    'private_key_id': os.environ.get('GOOGLE_PRIVATE_KEY_ID'),
    'private_key': private_key,
    'client_email': os.environ.get('GOOGLE_CLIENT_EMAIL'),
    'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
    'auth_uri': os.environ.get('GOOGLE_AUTH_URI'),
    'token_uri': os.environ.get('GOOGLE_TOKEN_URI'),
    'auth_provider_x509_cert_url': os.environ.get('GOOGLE_AUTH_PROVIDER_X509_CERT_URL'),
    'client_x509_cert_url': os.environ.get('GOOGLE_CLIENT_X509_CERT_URL')
}
scopes = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_info(credentials_info, scopes=scopes)
service = build('sheets', 'v4', credentials=creds)

sheet_id = '1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ'

metadata = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
sheet_name = metadata.get('sheets', [])[0].get('properties', {}).get('title', 'Pages')

result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'{sheet_name}!A1:A').execute()
urls = result.get('values', [])

# We know the last 119 rows are the missing ones, but let's check all rows that have "Draft (0 Clicks/Impressions)" status just to be safe.
result_status = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'{sheet_name}!L1:L').execute()
statuses = result_status.get('values', [])

updates = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

print("Checking URLs for redirects...")
for i in range(1, len(urls)):
    if not urls[i]: continue
    url = urls[i][0].strip()
    
    status_text = ""
    if i < len(statuses) and statuses[i]:
        status_text = statuses[i][0]
        
    if "Draft (0 Clicks/Impressions)" in status_text:
        try:
            resp = requests.get(url, headers=headers, allow_redirects=False, timeout=10)
            if resp.status_code in (301, 302, 307, 308):
                # Update this row
                # Google Sheets API uses 0-based index for batchUpdate requests
                updates.append({
                    'range': f'{sheet_name}!L{i+1}',
                    'values': [['Redirected (Sitemap Error)']]
                })
        except Exception as e:
            print(f"Error checking {url}: {e}")

print(f"Found {len(updates)} redirected URLs to update.")

if updates:
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': updates
    }
    service.spreadsheets().values().batchUpdate(spreadsheetId=sheet_id, body=body).execute()
    print("Google Sheet updated successfully.")
else:
    print("No updates needed.")
