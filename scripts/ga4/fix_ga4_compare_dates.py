import os
import urllib.parse
import datetime
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

        print("Fetching URLs from Google Sheets...")
        result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!A:A").execute()
        rows = result.get('values', [])
        
        col_o = [["GA4 Link Compare\n(6 เดือน)"]]
        
        today = datetime.datetime.now()
        
        # Calculate compare dates (1 year ago)
        # compareDate01: Today 1 year ago (e.g. 20250714)
        # compareDate00: 180 days before compareDate01 (e.g. 20250115)
        compareDate01_dt = today - datetime.timedelta(days=365)
        compareDate01 = compareDate01_dt.strftime("%Y%m%d")
        compareDate00 = (compareDate01_dt - datetime.timedelta(days=180)).strftime("%Y%m%d")
        
        print(f"Compare Range: {compareDate00} to {compareDate01}")
        
        print("Processing Column O with yearToDate and custom comparison dates...")
        for i, row in enumerate(rows):
            if i == 0:
                continue
                
            url = row[0] if len(row) > 0 else ""
            if not url or "rwcclinic.com" not in url:
                col_o.append([""])
                continue
                
            path = url.replace("https://rwcclinic.com", "")
            if not path.startswith("/"):
                path = "/" + path
                
            path_encoded = urllib.parse.quote(urllib.parse.quote(path, safe=''), safe='')
            
            # Match the exact template provided by the user:
            # _u.dateOption%3DyearToDate
            # _u.comparisonOption%3DlastPeriod
            # _u.compareDateOption%3Dcustom
            # _u.compareDate00%3D{compareDate00}
            # Using custom comparison dates in URL with built_comparisons_enabled=true and comparisonOption=custom
            ga4_url_o = f'https://analytics.google.com/analytics/web/?hl=en#/a149800124p292925407/reports/explorer?params=_u..nav%3Dmaui%26_u..built_comparisons_enabled%3Dtrue%26_u..comparisons%3D%5B%7B%22savedComparisonId%22:%227523527606%22,%22name%22:%22Organic%20traffic%22,%22isEnabled%22:true,%22filters%22:%5B%7B%22fieldName%22:%22sessionDefaultChannelGrouping%22,%22evaluationType%22:8,%22expressionList%22:%5B%22Organic%20Search%22,%22Organic%20Video%22,%22Organic%20Social%22,%22Organic%20Shopping%22%5D,%22isCaseSensitive%22:true%7D%5D,%22systemDefinedSavedComparisonType%22:2,%22isSystemDefined%22:true%7D%5D%26_u.dateOption%3DyearToDate%26_u.comparisonOption%3Dcustom%26_u.compareDateOption%3Dcustom%26_u.compareDate00%3D{compareDate00}%26_u.compareDate01%3D{compareDate01}%26_r.explorerCard..filterTerm%3D{path_encoded}%26_r.explorerCard..startRow%3D0&ruid=0d646679-6477-4cd0-a2cc-a3c33313c77f&collectionId=10576530072&r=15246722299'
            
            col_o.append([f'=HYPERLINK("{ga4_url_o}", "Compare in GA4")'])

        print(f"Updating Column O (688 rows)...")
        
        body = {
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"'{target_sheet_name}'!O1:O{len(col_o)}", "values": col_o},
            ]
        }
        
        sheet.values().batchUpdate(
            spreadsheetId=sheet_id,
            body=body
        ).execute()
        
        print("Update completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
