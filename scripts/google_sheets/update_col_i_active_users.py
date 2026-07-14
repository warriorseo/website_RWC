import os
import urllib.parse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Metric, Dimension, RunReportRequest, FilterExpression, Filter
)
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

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/analytics.readonly']
credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
sheet_service = build('sheets', 'v4', credentials=credentials)
sheet = sheet_service.spreadsheets()
ga4_client = BetaAnalyticsDataClient(credentials=credentials)

sheet_id = "1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ"
target_gid = 199841076
property_id = "292925407"

def fetch_90d_active_users():
    req = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="90daysAgo", end_date="today")],
        dimension_filter=FilterExpression(
            filter=Filter(field_name="sessionDefaultChannelGroup", in_list_filter=Filter.InListFilter(values=["Organic Search", "Organic Video", "Organic Social", "Organic Shopping"]))
        ),
        limit=100000
    )
    res = ga4_client.run_report(req)
    data = {}
    for row in res.rows:
        path = row.dimension_values[0].value
        users = int(row.metric_values[0].value)
        data[path] = users
    return data

def main():
    try:
        sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        target_sheet_name = None
        for s in sheets:
            if s.get("properties", {}).get("sheetId") == target_gid:
                target_sheet_name = s.get("properties", {}).get("title")
                break

        print("Fetching Active Users (90 Days) from GA4...")
        data_90d = fetch_90d_active_users()

        print("Fetching URLs from Google Sheets...")
        result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!A:A").execute()
        rows = result.get('values', [])
        
        col_i = [["Active User\n(3 เดือนล่าสุด)"]]
        
        print("Processing data...")
        for i, row in enumerate(rows):
            if i == 0:
                continue
                
            url = row[0] if len(row) > 0 else ""
            if not url or "rwcclinic.com" not in url:
                col_i.append([""])
                continue
                
            path = url.replace("https://rwcclinic.com", "")
            if not path.startswith("/"):
                path = "/" + path
                
            users = data_90d.get(path, 0)
            col_i.append([users])

        print(f"Updating Column I for {len(col_i)-1} rows...")
        
        sheet.values().update(
            spreadsheetId=sheet_id,
            range=f"'{target_sheet_name}'!I1:I{len(col_i)}",
            valueInputOption="USER_ENTERED",
            body={"values": col_i}
        ).execute()
        
        print("Update completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
