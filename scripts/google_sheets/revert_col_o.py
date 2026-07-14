import os
import urllib.parse
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

def main():
    try:
        sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        target_sheet_name = None
        for s in sheets:
            if s.get("properties", {}).get("sheetId") == target_gid:
                target_sheet_name = s.get("properties", {}).get("title")
                break

        print("Fetching column O...")
        result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!O:O", valueRenderOption='FORMULA').execute()
        rows = result.get('values', [])
        
        col_o = [["GA4 Link Compare\n(90 วัน)"]]
        
        for i, row in enumerate(rows):
            if i == 0:
                continue
                
            formula = row[0] if len(row) > 0 else ""
            if formula.startswith("=HYPERLINK"):
                new_formula = formula.replace('last12Months', 'last90Days')
                col_o.append([new_formula])
            else:
                col_o.append([""])
                
        print(f"Updating {len(col_o)-1} rows...")
        sheet.values().update(
            spreadsheetId=sheet_id,
            range=f"'{target_sheet_name}'!O1:O{len(col_o)}",
            valueInputOption="USER_ENTERED",
            body={"values": col_o}
        ).execute()
        
        print("Update completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
