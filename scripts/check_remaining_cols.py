import os
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

from compare_gsc_fillers_only import creds_info

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_info(creds_info, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

SPREADSHEET_ID = '1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ'
SHEET_NAME = 'URL Revision and Engagement'

result = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range=f"'{SHEET_NAME}'!A1:Z15"
).execute()

values = result.get('values', [])
print("Current columns check in Sheet:")
for idx, row in enumerate(values[:13]):
    url = row[0] if len(row) > 0 else ""
    avg_users = row[1] if len(row) > 1 else ""
    col_q = row[16] if len(row) > 16 else ""
    col_r = row[17] if len(row) > 17 else ""
    col_s = row[18] if len(row) > 18 else ""
    col_t = row[19] if len(row) > 19 else ""
    print(f"Row {idx+1} | URL: {url:<45} | Col B: {avg_users:<6} | Col Q: {col_q:<10} | Col R: {col_r:<10} | Col S: {col_s:<15} | Col T: {col_t:<15}")
