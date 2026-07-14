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

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

sheet_id = "1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ"
target_gid = 199841076

try:
    # Get spreadsheet info to find the sheet name for the target gid
    sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    
    target_sheet_name = None
    for s in sheets:
        if s.get("properties", {}).get("sheetId") == target_gid:
            target_sheet_name = s.get("properties", {}).get("title")
            break
            
    if not target_sheet_name:
        target_sheet_name = sheets[0].get("properties", {}).get("title")
    
    print(f"Reading from sheet: {target_sheet_name}")
    
    # Get first 25 rows, columns A to Z
    result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!A1:Z25").execute()
    values = result.get('values', [])
    
    if not values:
        print("No data found.")
    else:
        # Print header
        header = values[0]
        print(f"Columns: {header}")
        # Print rows 1 to 20
        for i, row in enumerate(values[1:21]):
            print(f"Row {i+1}: {row}")

except Exception as e:
    print(f"Error accessing sheet: {e}")
