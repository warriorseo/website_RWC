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
scopes = ['https://www.googleapis.com/auth/webmasters.readonly']
creds = service_account.Credentials.from_service_account_info(credentials_info, scopes=scopes)

try:
    service = build('searchconsole', 'v1', credentials=creds)
    site_list = service.sites().list().execute()
    sites = site_list.get('siteEntry', [])
    
    if not sites:
        print("Service account authenticated successfully, but it has no access to any Search Console properties.")
        print(f"Please add {credentials_info['client_email']} to the Search Console property.")
    else:
        print("Service account has access to the following sites in Search Console:")
        for site in sites:
            print(f"- {site.get('siteUrl')} (Permission level: {site.get('permissionLevel')})")
except Exception as e:
    print(f"Error accessing Search Console: {e}")
