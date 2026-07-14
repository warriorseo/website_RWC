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

raw_services = """
https://rwcclinic.com/acne-treatment
https://rwcclinic.com/breaking-down-fillers
https://rwcclinic.com/cheek-filler
https://rwcclinic.com/chin-filler
https://rwcclinic.com/diode-laser
https://rwcclinic.com/dual-yellow-laser
https://rwcclinic.com/ellanse
https://rwcclinic.com/emsculpt
https://rwcclinic.com/fat-grafting-face
https://rwcclinic.com/fat-injection-breast
https://rwcclinic.com/fatbreak-down
https://rwcclinic.com/filler-cheek-groove
https://rwcclinic.com/filler-injection-expert
https://rwcclinic.com/filler-under-eyes
https://rwcclinic.com/forehead-filler-injection
https://rwcclinic.com/fractora-rf
https://rwcclinic.com/gouri
https://rwcclinic.com/gouri-pcl
https://rwcclinic.com/hifu-lift
https://rwcclinic.com/hip-filler-injection
https://rwcclinic.com/karisma-rh-collagen
https://rwcclinic.com/lady-repair-by-forma-v
https://rwcclinic.com/liposuction
https://rwcclinic.com/lips-filler
https://rwcclinic.com/made-collagen-rwc
https://rwcclinic.com/meso-fat-rwc
https://rwcclinic.com/meso-therapy
https://rwcclinic.com/mint-thread-lift
https://rwcclinic.com/morpheus-8
https://rwcclinic.com/nad-iv-therapy
https://rwcclinic.com/nose-filler-injection
https://rwcclinic.com/physiognomy
https://rwcclinic.com/pico-laser
https://rwcclinic.com/plinest-skin-treatment
https://rwcclinic.com/repair-vagina
https://rwcclinic.com/rwc-tips-face-shape
https://rwcclinic.com/sculptra
https://rwcclinic.com/temple-filler
https://rwcclinic.com/tess-lift-soft-thread
https://rwcclinic.com/therafill
https://rwcclinic.com/thermage
https://rwcclinic.com/ulthera-lift
https://rwcclinic.com/ulthera-prime
https://rwcclinic.com/ultraformer
https://rwcclinic.com/vagina-filler
https://rwcclinic.com/vitamin-injection
https://rwcclinic.com/vitaran
https://rwcclinic.com/what-is-harmonyca
"""

service_urls = [u.strip().rstrip('/') for u in raw_services.strip().split('\n') if u.strip()]

def main():
    try:
        sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        target_sheet_name = None
        for s in sheets:
            if s.get("properties", {}).get("sheetId") == target_gid:
                target_sheet_name = s.get("properties", {}).get("title")
                break

        print("Fetching Column A and B...")
        result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!A1:B").execute()
        rows = result.get('values', [])
        
        updates = []
        services_found = 0
        
        for i, row in enumerate(rows):
            if i == 0:
                continue
                
            url = row[0] if len(row) > 0 else ""
            current_type = row[1] if len(row) > 1 else ""
            
            url_normalized = url.rstrip('/')
            
            if url_normalized in service_urls:
                if current_type != "Service":
                    updates.append({
                        "range": f"'{target_sheet_name}'!B{i+1}",
                        "values": [["Service"]]
                    })
                services_found += 1
                
        print(f"Total Service URLs matched in sheet: {services_found}/{len(service_urls)}")
        print(f"Total updates to push: {len(updates)}")
        
        if updates:
            body = {
                "valueInputOption": "USER_ENTERED",
                "data": updates
            }
            res = sheet.values().batchUpdate(spreadsheetId=sheet_id, body=body).execute()
            print("Successfully updated the sheet!")
        else:
            print("No updates needed. Everything is already correct.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
