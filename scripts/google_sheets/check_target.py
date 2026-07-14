import os
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

target_sheet_id = '1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ'

metadata = service.spreadsheets().get(spreadsheetId=target_sheet_id).execute()
print("Sheets in Target:")
for sheet in metadata.get('sheets', []):
    props = sheet.get('properties', {})
    title = props.get('title')
    sheet_id = props.get('sheetId')
    print(f"- {title} (ID: {sheet_id})")

