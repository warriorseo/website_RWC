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

# The list provided by the user
true_news_urls = [
    "https://rwcclinic.com/drkanom-regional-expert-of-gouri/",
    "https://rwcclinic.com/drkanom-the-path-to-expertise/",
    "https://rwcclinic.com/edencolors-award-2023/",
    "https://rwcclinic.com/drkanom-aesla-awards-2023/",
    "https://rwcclinic.com/drkanom-praew-iconic-beauty2023/",
    "https://rwcclinic.com/drkanom-region-expert-gouri/",
    "https://rwcclinic.com/drkanom-gain2023/",
    "https://rwcclinic.com/drkanom-ami-immersion2023/",
    "https://rwcclinic.com/drkanom-wcam2023/",
    "https://rwcclinic.com/drkanom-tesslift-gouri/",
    "https://rwcclinic.com/drkanom-5th-smart/",
    "https://rwcclinic.com/rwc-clinic-sculptra/",
    "https://rwcclinic.com/drkanom-skin-quality/",
    "https://rwcclinic.com/drkanom-smpf/",
    "https://rwcclinic.com/drkanom-gouri-international-symposium-in-asia/",
    "https://rwcclinic.com/drkanom-imcasasia2023/",
    "https://rwcclinic.com/drkanom-finalist-amwc/",
    "https://rwcclinic.com/drkanom-advanced-full-face-anatomy/",
    "https://rwcclinic.com/drkanom-gouri/",
    "https://rwcclinic.com/drkanom-dst-annual-meeting-2023/",
    "https://rwcclinic.com/drkanom-woody/",
    "https://rwcclinic.com/youthful-by-drkanom/",
    "https://rwcclinic.com/best-filler-clinic-sudsupda/",
    "https://rwcclinic.com/allergan-aesthetic-award/",
    "https://rwcclinic.com/thread-lifting-advance-class/",
    "https://rwcclinic.com/edencolors-awards/",
    "https://rwcclinic.com/rwc-elle-awards/",
    "https://rwcclinic.com/drkanom-amas2022/",
    "https://rwcclinic.com/rwc-iconic-beauty-awards-2022/",
    "https://rwcclinic.com/drkanom-imcas-asia-2022/",
    "https://rwcclinic.com/dr-kanom-asia-partners-meeting-2022/",
    "https://rwcclinic.com/rwc-event-sudsapda/"
]

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
        news_found = 0
        changed_to_article = 0
        
        for i, row in enumerate(rows):
            if i == 0:
                continue
                
            url = row[0] if len(row) > 0 else ""
            current_type = row[1] if len(row) > 1 else ""
            
            # Normalizing URL to handle trailing slashes optionally
            url_normalized = url.rstrip('/')
            true_news_normalized = [u.rstrip('/') for u in true_news_urls]
            
            is_true_news = url_normalized in true_news_normalized
            
            new_type = None
            if is_true_news:
                if current_type != "News":
                    new_type = "News"
                news_found += 1
            else:
                if current_type == "News":
                    new_type = "Article"
                    changed_to_article += 1
            
            if new_type:
                # Update this specific cell
                updates.append({
                    "range": f"'{target_sheet_name}'!B{i+1}",
                    "values": [[new_type]]
                })
                
        print(f"Total True News URLs matched in sheet: {news_found}/{len(true_news_urls)}")
        print(f"Total false News changed back to Article: {changed_to_article}")
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
