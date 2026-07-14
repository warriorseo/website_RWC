import os
import time
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

def fetch_ytd_data():
    today = datetime.datetime.now()
    current_year = today.year
    previous_year = current_year - 1
    
    # YTD: Jan 1st to Today
    ytd_start_dt = datetime.datetime(current_year, 1, 1)
    ytd_end_dt = today
    ytd_days = (ytd_end_dt - ytd_start_dt).days + 1
    
    # Previous YTD: lastPeriod (preceding period of ytd_days before Jan 1st)
    prev_ytd_end_dt = ytd_start_dt - datetime.timedelta(days=1)
    prev_ytd_start_dt = prev_ytd_end_dt - datetime.timedelta(days=ytd_days - 1)
    
    ytd_start = ytd_start_dt.strftime("%Y-%m-%d")
    ytd_end = ytd_end_dt.strftime("%Y-%m-%d")
    prev_ytd_start = prev_ytd_start_dt.strftime("%Y-%m-%d")
    prev_ytd_end = prev_ytd_end_dt.strftime("%Y-%m-%d")
    
    req_curr = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="userEngagementDuration"), Metric(name="engagementRate"), Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date=ytd_start, end_date=ytd_end)],
        dimension_filter=FilterExpression(
            filter=Filter(field_name="sessionDefaultChannelGroup", in_list_filter=Filter.InListFilter(values=["Organic Search", "Organic Video", "Organic Social", "Organic Shopping"]))
        ),
        limit=100000
    )
    req_past = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="userEngagementDuration"), Metric(name="engagementRate"), Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date=prev_ytd_start, end_date=prev_ytd_end)],
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

def format_combined_cell(path, curr_data, past_data):
    curr = curr_data.get(path, (0.0, 0.0, 0.0))
    past = past_data.get(path, (0.0, 0.0, 0.0))
    
    curr_time, curr_eng, curr_users = curr
    past_time, past_eng, past_users = past
    
    if curr_users == 0 or past_users == 0 or past_time == 0 or past_eng == 0:
        return "N/A"
        
    # Line 1: Current YTD
    line1 = f"A:{int(curr_users)} | T:{curr_time:.0f}s | R:{curr_eng*100:.0f}%"
    
    # Line 2: Past YTD (Compare)
    line2 = f"A:{int(past_users)} | T:{past_time:.0f}s | R:{past_eng*100:.0f}%"
    
    # Line 3: Percentage Change
    user_pct = (curr_users - past_users) / past_users * 100
    time_pct = (curr_time - past_time) / past_time * 100
    eng_pct = (curr_eng - past_eng) / past_eng * 100
    
    u_sign = '+' if user_pct > 0 else ''
    t_sign = '+' if time_pct > 0 else ''
    e_sign = '+' if eng_pct > 0 else ''
    
    line3 = f"A:{u_sign}{user_pct:.0f}% | T:{t_sign}{time_pct:.0f}% | R:{e_sign}{eng_pct:.0f}%"
    
    return f"{line1}\n{line2}\n{line3}"

def main():
    try:
        sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        target_sheet_name = None
        for s in sheets:
            if s.get("properties", {}).get("sheetId") == target_gid:
                target_sheet_name = s.get("properties", {}).get("title")
                break
                
        print("Inserting column between N and O (index 15)...")
        batch_update_request = {
            "requests": [
                {
                    "insertDimension": {
                        "range": {
                            "sheetId": target_gid,
                            "dimension": "COLUMNS",
                            "startIndex": 15,
                            "endIndex": 16
                        },
                        "inheritFromBefore": True
                    }
                }
            ]
        }
        sheet.batchUpdate(spreadsheetId=sheet_id, body=batch_update_request).execute()
        print("Column inserted.")
        
        time.sleep(2)
        
        print("Fetching YTD data from GA4...")
        curr_yoy, past_yoy = fetch_ytd_data()

        print("Fetching URLs from Google Sheets...")
        result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!A:A").execute()
        rows = result.get('values', [])
        
        col_o = [["GA4 YoY Combined Summary\n(YTD)"]]
        
        print("Processing data...")
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
                
            combined_val = format_combined_cell(path, curr_yoy, past_yoy)
            col_o.append([combined_val])

        print(f"Updating Column O for {len(col_o)-1} rows...")
        sheet.values().update(
            spreadsheetId=sheet_id,
            range=f"'{target_sheet_name}'!O1:O{len(col_o)}",
            valueInputOption="USER_ENTERED",
            body={"values": col_o}
        ).execute()
        
        print("Update completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
