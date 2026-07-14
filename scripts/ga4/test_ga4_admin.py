import os
from google.oauth2 import service_account
from google.analytics.admin_v1alpha import AnalyticsAdminServiceClient
from dotenv import load_dotenv

load_dotenv(r"d:\AI-Cyborg-2558\00_agents\.env")

private_key = os.environ.get("GOOGLE_PRIVATE_KEY", "")
if "\\n" in private_key:
    private_key = private_key.replace("\\n", "\n")

credentials_info = {
    "type": os.environ.get("GOOGLE_SERVICE_ACCOUNT_TYPE"),
    "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
    "private_key_id": os.environ.get("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": private_key,
    "client_email": os.environ.get("GOOGLE_CLIENT_EMAIL"),
    "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
    "auth_uri": os.environ.get("GOOGLE_AUTH_URI"),
    "token_uri": os.environ.get("GOOGLE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.environ.get("GOOGLE_CLIENT_X509_CERT_URL")
}

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)

client = AnalyticsAdminServiceClient(credentials=credentials)

try:
    accounts = client.list_account_summaries()
    found = False
    for account in accounts:
        found = True
        print(f"Account: {account.account} ({account.display_name})")
        for property_summary in account.property_summaries:
            print(f"  Property: {property_summary.property} ({property_summary.display_name})")
    
    if not found:
        print("Service account has no access to any Google Analytics accounts.")
except Exception as e:
    print(f"Error: {e}")
