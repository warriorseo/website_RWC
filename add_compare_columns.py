import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
import time

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

sheet_id = "1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ"
target_gid = 199841076

def main():
    try:
        # Get sheet info
        sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        target_sheet_name = None
        for s in sheets:
            if s.get("properties", {}).get("sheetId") == target_gid:
                target_sheet_name = s.get("properties", {}).get("title")
                break
                
        if not target_sheet_name:
            target_sheet_name = sheets[0].get("properties", {}).get("title")
        
        # 1. Fetch existing formulas to transform them
        result = sheet.values().get(
            spreadsheetId=sheet_id, 
            range=f"'{target_sheet_name}'!A:J", 
            valueRenderOption='FORMULA'
        ).execute()
        
        rows = result.get('values', [])
        if not rows:
            print("No data found.")
            return

        print("Fetched existing formulas.")
        
        # We need GSC Link Compare (from col 6) and GA4 Link Compare (from col 9)
        gsc_compare_column = [["GSC Link Compare"]]
        ga4_compare_column = [["GA4 Link Compare"]]
        
        for i, row in enumerate(rows):
            if i == 0:
                continue # Skip header
            
            gsc_formula = ""
            ga4_formula = ""
            
            if len(row) > 6:
                gsc_val = row[6]
                if isinstance(gsc_val, str) and gsc_val.startswith("=HYPERLINK"):
                    # Transform GSC formula
                    gsc_formula = gsc_val.replace('num_of_months=6', 'num_of_months=3').replace('num_of_months=16', 'num_of_months=3').replace('"View in GSC"', '"Compare in GSC"')
            
            if len(row) > 9:
                ga4_val = row[9]
                if isinstance(ga4_val, str) and ga4_val.startswith("=HYPERLINK"):
                    # Transform GA4 formula
                    ga4_formula = ga4_val.replace('_u.comparisonOption%3Ddisabled', '_u.comparisonOption%3DyearOverYear').replace('"View in GA4"', '"Compare in GA4"')
            
            gsc_compare_column.append([gsc_formula])
            ga4_compare_column.append([ga4_formula])
        
        # 2. Insert columns
        print("Inserting columns...")
        batch_update_request = {
            "requests": [
                {
                    "insertDimension": {
                        "range": {
                            "sheetId": target_gid,
                            "dimension": "COLUMNS",
                            "startIndex": 7,  # After G (index 6), so index 7
                            "endIndex": 8
                        },
                        "inheritFromBefore": True
                    }
                },
                {
                    "insertDimension": {
                        "range": {
                            "sheetId": target_gid,
                            "dimension": "COLUMNS",
                            "startIndex": 11, # After J (which was index 9, but now index 10 due to prev insert). So index 11
                            "endIndex": 12
                        },
                        "inheritFromBefore": True
                    }
                }
            ]
        }
        
        sheet.batchUpdate(spreadsheetId=sheet_id, body=batch_update_request).execute()
        print("Columns inserted successfully.")
        
        # 3. Write data to new columns
        # Wait a moment for sheets to process
        time.sleep(2)
        
        print("Updating cells with new formulas...")
        # Update GSC Compare (Col H)
        sheet.values().update(
            spreadsheetId=sheet_id,
            range=f"'{target_sheet_name}'!H1:H{len(gsc_compare_column)}",
            valueInputOption="USER_ENTERED",
            body={"values": gsc_compare_column}
        ).execute()
        
        # Update GA4 Compare (Col L)
        sheet.values().update(
            spreadsheetId=sheet_id,
            range=f"'{target_sheet_name}'!L1:L{len(ga4_compare_column)}",
            valueInputOption="USER_ENTERED",
            body={"values": ga4_compare_column}
        ).execute()
        
        print("Update completed successfully!")
        
    except Exception as e:
        print(f"Error updating sheet: {e}")

if __name__ == "__main__":
    main()
