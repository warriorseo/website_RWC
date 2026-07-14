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

        result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!A1:B").execute()
        rows = result.get('values', [])
        
        keywords = ["filler", "juvederm", "restylane", "belotero", "neuramis", "hyaluronic", "sculptra", "radiesse"]
        
        filler_pages = {"Service": [], "Article": [], "News": [], "Page": []}
        
        for i, row in enumerate(rows):
            if i == 0 or len(row) == 0:
                continue
            
            url = row[0].lower()
            page_type = row[1] if len(row) > 1 else "Page"
            
            # Check if any keyword is in the URL
            is_filler = any(kw in url for kw in keywords)
            
            if is_filler:
                if page_type not in filler_pages:
                    filler_pages[page_type] = []
                filler_pages[page_type].append(row[0])
                
        print("=== FILLER PAGES EXTRACTED ===")
        for p_type, urls in filler_pages.items():
            print(f"\\n[{p_type}] - {len(urls)} pages:")
            for u in urls:
                print(f"  - {u}")
                
        total = sum(len(urls) for urls in filler_pages.values())
        print(f"\\nTotal Filler Pages Found: {total}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
