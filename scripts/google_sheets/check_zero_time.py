import os
import datetime
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

def main():
    try:
        sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        target_sheet_name = None
        for s in sheets:
            if s.get("properties", {}).get("sheetId") == target_gid:
                target_sheet_name = s.get("properties", {}).get("title")
                break
                
        # Read Column A (URL), Column H (Active User), Column I (Engagement Time)
        print("Reading rows to find pages with 0 engagement time...")
        result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!A1:J20").execute()
        rows = result.get('values', [])
        
        for idx, r in enumerate(rows):
            if idx == 0:
                continue
            url = r[0]
            users = r[7] # Column H
            time_val = r[8] # Column I
            
            if time_val == '0' and int(users) > 0:
                path = url.replace("https://rwcclinic.com", "")
                if not path.startswith("/"):
                    path = "/" + path
                print(f"Row {idx+1}: {path} has Users: {users}, Time: {time_val}")
                
                # Query GA4 directly for this path
                req = RunReportRequest(
                    property=f"properties/{property_id}",
                    dimensions=[Dimension(name="pagePath")],
                    metrics=[Metric(name="userEngagementDuration"), Metric(name="activeUsers")],
                    date_ranges=[DateRange(start_date="90daysAgo", end_date="today")],
                    dimension_filter=FilterExpression(
                        filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value=path))
                    )
                )
                res = ga4_client.run_report(req)
                for row in res.rows:
                    tot_time = row.metric_values[0].value
                    active_users = row.metric_values[1].value
                    print(f"  -> GA4 API reports: total duration = {tot_time}s, active users = {active_users}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
