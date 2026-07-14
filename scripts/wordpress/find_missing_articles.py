import os
import csv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv(r'd:\AI-Cyborg-2558\00_agents\.env')

post_urls = set()
try:
    with open('post_sitemap.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            post_urls.add(row['URL'].strip())
except Exception as e:
    print(f"Error reading post_sitemap.csv: {e}")

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
scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = service_account.Credentials.from_service_account_info(credentials_info, scopes=scopes)
service = build('sheets', 'v4', credentials=creds)

sheet_id = '1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ'

metadata = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
sheet_name = metadata.get('sheets', [])[0].get('properties', {}).get('title', 'Pages')

result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'{sheet_name}!A1:A').execute()
urls = result.get('values', [])

sheet_urls = set()
for row in urls:
    if row:
        sheet_urls.add(row[0].strip())

# Some URLs might have trailing slashes differ.
normalized_sheet_urls = {u.strip('/') for u in sheet_urls}

missing_urls = []
for p_url in post_urls:
    if p_url.strip('/') not in normalized_sheet_urls:
        missing_urls.append(p_url)

print(f"Total articles in sitemap: {len(post_urls)}")
print(f"Total URLs in sheet: {len(sheet_urls)}")
print(f"Missing articles (0 impressions in GSC): {len(missing_urls)}")
print("-" * 50)
for url in sorted(missing_urls):
    print(url)
