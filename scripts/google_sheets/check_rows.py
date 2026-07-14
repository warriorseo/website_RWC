import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv(r"d:\AI-Cyborg-2558\00_agents\.env")
private_key = os.environ.get("GOOGLE_PRIVATE_KEY", "").replace("\\n", "\n")
credentials_info = {
    "type": os.environ.get("GOOGLE_SERVICE_ACCOUNT_TYPE"),
    "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
    "private_key_id": os.environ.get("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": private_key,
    "client_email": os.environ.get("GOOGLE_CLIENT_EMAIL"),
    "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
    "token_uri": os.environ.get("GOOGLE_TOKEN_URI"),
}

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

sheet_id = "1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ"
target_gid = 199841076

sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
sheets = sheet_metadata.get('sheets', '')
target_sheet_name = None
for s in sheets:
    if s.get("properties", {}).get("sheetId") == target_gid:
        target_sheet_name = s.get("properties", {}).get("title")
        break

result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!A:A").execute()
rows = result.get('values', [])
print(f"Total rows in column A: {len(rows)}")
