import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
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

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

sheets_to_inspect = {
    "Target (1Iz...)": "1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ",
    "GSC (1M3...)": "1M3AzK2GSgyxA295wsOJcGx_OwBrcRjhvxub5tMegPlw",
    "New GA4 (1jB...)": "1jB7zEv9mx_RgVJwSRg5fe8mGBxOZdDo5My8ygDeBDm4"
}

for name, sheet_id in sheets_to_inspect.items():
    try:
        # Get spreadsheet info
        sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        first_sheet_name = sheets[0].get("properties", {}).get("title", "Sheet1")
        
        # Get first few rows
        result = sheet.values().get(spreadsheetId=sheet_id, range=f"{first_sheet_name}!A1:J3").execute()
        values = result.get('values', [])
        
        print(f"--- {name} ---")
        print(f"Sheet Name: {first_sheet_name}")
        if not values:
            print("No data found.")
        else:
            for i, row in enumerate(values):
                print(f"Row {i+1}: {row}")
        print("\n")
    except Exception as e:
        print(f"Error accessing {name}: {e}")
