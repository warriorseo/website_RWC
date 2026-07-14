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
        # Columns to delete: L, M, N (indices 11, 12, 13)
        # startIndex: 11 (L)
        # endIndex: 14 (N is index 13, so endIndex is 14)
        print("Deleting Columns L, M, N (index 11 to 14)...")
        batch_update_request = {
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": target_gid,
                            "dimension": "COLUMNS",
                            "startIndex": 11,
                            "endIndex": 14
                        }
                    }
                }
            ]
        }
        sheet.batchUpdate(spreadsheetId=sheet_id, body=batch_update_request).execute()
        print("Columns L, M, N deleted successfully.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
