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

def main():
    try:
        sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        target_sheet_name = None
        for s in sheets:
            if s.get("properties", {}).get("sheetId") == target_gid:
                target_sheet_name = s.get("properties", {}).get("title")
                break
                
        # Read column K (GA4 Link)
        result = sheet.values().get(
            spreadsheetId=sheet_id, 
            range=f"'{target_sheet_name}'!K:K", 
            valueRenderOption='FORMULA'
        ).execute()
        
        rows = result.get('values', [])
        
        updated_column = [["GA4 Link Compare\n(12 เดือน)"]]
        
        for i, row in enumerate(rows):
            if i == 0:
                continue
                
            formula = row[0] if row else ""
            if formula.startswith("=HYPERLINK"):
                new_formula = formula.replace('last90Days', 'last12Months').replace('_u.comparisonOption%3Ddisabled', '_u.comparisonOption%3DyearOverYear').replace('"View in GA4"', '"Compare in GA4"')
                updated_column.append([new_formula])
            else:
                updated_column.append([""])
                
        print(f"Updating {len(updated_column)} rows in column N...")
        sheet.values().update(
            spreadsheetId=sheet_id,
            range=f"'{target_sheet_name}'!N1:N{len(updated_column)}",
            valueInputOption="USER_ENTERED",
            body={"values": updated_column}
        ).execute()
        
        print("Column N updated successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
