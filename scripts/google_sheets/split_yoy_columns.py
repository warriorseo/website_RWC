import os
import time
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

def fetch_yoy_data():
    req_curr = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="userEngagementDuration"), Metric(name="engagementRate"), Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="180daysAgo", end_date="today")],
        dimension_filter=FilterExpression(
            filter=Filter(field_name="sessionDefaultChannelGroup", in_list_filter=Filter.InListFilter(values=["Organic Search", "Organic Video", "Organic Social", "Organic Shopping"]))
        ),
        limit=100000
    )
    req_past = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="userEngagementDuration"), Metric(name="engagementRate"), Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="545daysAgo", end_date="365daysAgo")],
        dimension_filter=FilterExpression(
            filter=Filter(field_name="sessionDefaultChannelGroup", in_list_filter=Filter.InListFilter(values=["Organic Search", "Organic Video", "Organic Social", "Organic Shopping"]))
        ),
        limit=100000
    )
    
    res_curr = ga4_client.run_report(req_curr)
    res_past = ga4_client.run_report(req_past)
    
    curr_data = {}
    for row in res_curr.rows:
        path = row.dimension_values[0].value
        tot_time = float(row.metric_values[0].value)
        eng_rate = float(row.metric_values[1].value)
        users = float(row.metric_values[2].value)
        avg_time = tot_time / users if users > 0 else 0
        curr_data[path] = (avg_time, eng_rate, users)
        
    past_data = {}
    for row in res_past.rows:
        path = row.dimension_values[0].value
        tot_time = float(row.metric_values[0].value)
        eng_rate = float(row.metric_values[1].value)
        users = float(row.metric_values[2].value)
        avg_time = tot_time / users if users > 0 else 0
        past_data[path] = (avg_time, eng_rate, users)
        
    return curr_data, past_data

def process_yoy_split(path, curr_data, past_data):
    curr = curr_data.get(path, (0.0, 0.0, 0.0))
    past = past_data.get(path, (0.0, 0.0, 0.0))
    
    curr_time, curr_eng, curr_users = curr
    past_time, past_eng, past_users = past
    
    if curr_users == 0 or past_users == 0:
        return "N/A", "N/A", "N/A"
    
    user_diff = curr_users - past_users
    user_sign = '+' if user_diff > 0 else ''
    user_summary = f"{int(curr_users)} | {int(past_users)}\n({user_sign}{int(user_diff)})"
    
    time_diff = curr_time - past_time
    time_sign = '+' if time_diff > 0 else ''
    time_summary = f"{curr_time:.1f}s | {past_time:.1f}s\n({time_sign}{time_diff:.1f}s)"
    
    curr_eng_pct = curr_eng * 100
    past_eng_pct = past_eng * 100
    eng_diff = curr_eng_pct - past_eng_pct
    eng_sign = '+' if eng_diff > 0 else ''
    eng_summary = f"{curr_eng_pct:.1f}% | {past_eng_pct:.1f}%\n({eng_sign}{eng_diff:.1f}%)"
    
    return user_summary, time_summary, eng_summary

def main():
    try:
        sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        target_sheet_name = None
        for s in sheets:
            if s.get("properties", {}).get("sheetId") == target_gid:
                target_sheet_name = s.get("properties", {}).get("title")
                break
                
        # Column O is already inserted, so we skip the insertDimension step
        print("Fetching data from GA4...")
        curr_yoy, past_yoy = fetch_yoy_data()

        print("Fetching URLs from Google Sheets...")
        result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!A:A").execute()
        rows = result.get('values', [])
        
        col_m = [["GA4 Active Users YoY\n(6 เดือน)"]]
        col_n = [["GA4 Eng Time YoY\n(6 เดือน)"]]
        col_o = [["GA4 Eng Rate YoY\n(6 เดือน)"]]
        
        print("Processing data...")
        for i, row in enumerate(rows):
            if i == 0:
                continue
                
            url = row[0] if len(row) > 0 else ""
            if not url or "rwcclinic.com" not in url:
                col_m.append([""])
                col_n.append([""])
                col_o.append([""])
                continue
                
            path = url.replace("https://rwcclinic.com", "")
            if not path.startswith("/"):
                path = "/" + path
                
            user_sum, time_sum, eng_sum = process_yoy_split(path, curr_yoy, past_yoy)
            col_m.append([user_sum])
            col_n.append([time_sum])
            col_o.append([eng_sum])

        print(f"Updating Columns M, N, O for {len(col_m)-1} rows...")
        
        body = {
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"'{target_sheet_name}'!M1:M{len(col_m)}", "values": col_m},
                {"range": f"'{target_sheet_name}'!N1:N{len(col_n)}", "values": col_n},
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
