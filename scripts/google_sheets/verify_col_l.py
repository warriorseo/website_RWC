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

def fetch_single_page_ytd(path):
    today = datetime.datetime.now()
    current_year = today.year
    
    # YTD: Jan 1st to Today
    ytd_start_dt = datetime.datetime(current_year, 1, 1)
    ytd_end_dt = today
    ytd_days = (ytd_end_dt - ytd_start_dt).days + 1
    
    # Previous YTD: lastPeriod
    prev_ytd_end_dt = ytd_start_dt - datetime.timedelta(days=1)
    prev_ytd_start_dt = prev_ytd_end_dt - datetime.timedelta(days=ytd_days - 1)
    
    ytd_start = ytd_start_dt.strftime("%Y-%m-%d")
    ytd_end = ytd_end_dt.strftime("%Y-%m-%d")
    prev_ytd_start = prev_ytd_start_dt.strftime("%Y-%m-%d")
    prev_ytd_end = prev_ytd_end_dt.strftime("%Y-%m-%d")
    
    from google.analytics.data_v1beta.types import FilterExpressionList
    # Using AND group filters in GA4
    req_curr = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="userEngagementDuration"), Metric(name="engagementRate"), Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date=ytd_start, end_date=ytd_end)],
        dimension_filter=FilterExpression(
            and_group=FilterExpressionList(
                expressions=[
                    FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value=path))),
                    FilterExpression(filter=Filter(field_name="sessionDefaultChannelGroup", in_list_filter=Filter.InListFilter(values=["Organic Search", "Organic Video", "Organic Social", "Organic Shopping"])))
                ]
            )
        )
    )
    
    req_past = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="userEngagementDuration"), Metric(name="engagementRate"), Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date=prev_ytd_start, end_date=prev_ytd_end)],
        dimension_filter=FilterExpression(
            and_group=FilterExpressionList(
                expressions=[
                    FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value=path))),
                    FilterExpression(filter=Filter(field_name="sessionDefaultChannelGroup", in_list_filter=Filter.InListFilter(values=["Organic Search", "Organic Video", "Organic Social", "Organic Shopping"])))
                ]
            )
        )
    )
    
    res_curr = ga4_client.run_report(req_curr)
    res_past = ga4_client.run_report(req_past)
    
    curr_metrics = (0.0, 0.0, 0.0)
    for r in res_curr.rows:
        if r.dimension_values[0].value == path:
            tot_time = float(r.metric_values[0].value)
            eng_rate = float(r.metric_values[1].value)
            users = float(r.metric_values[2].value)
            avg_time = tot_time / users if users > 0 else 0
            curr_metrics = (avg_time, eng_rate, users)
            break
            
    past_metrics = (0.0, 0.0, 0.0)
    for r in res_past.rows:
        if r.dimension_values[0].value == path:
            tot_time = float(r.metric_values[0].value)
            eng_rate = float(r.metric_values[1].value)
            users = float(r.metric_values[2].value)
            avg_time = tot_time / users if users > 0 else 0
            past_metrics = (avg_time, eng_rate, users)
            break
            
    return curr_metrics, past_metrics

def format_expected_cell(curr, past):
    curr_time, curr_eng, curr_users = curr
    past_time, past_eng, past_users = past
    
    if curr_users == 0 or past_users == 0 or past_time == 0 or past_eng == 0:
        return "N/A"
        
    line1 = f"A:{int(curr_users)} | T:{curr_time:.0f}s | E:{curr_eng*100:.0f}%"
    line2 = f"A:{int(past_users)} | T:{past_time:.0f}s | E:{past_eng*100:.0f}%"
    
    user_pct = (curr_users - past_users) / past_users * 100
    time_pct = (curr_time - past_time) / past_time * 100
    eng_pct = (curr_eng - past_eng) / past_eng * 100
    
    u_sign = '+' if user_pct > 0 else ''
    t_sign = '+' if time_pct > 0 else ''
    e_sign = '+' if eng_pct > 0 else ''
    
    line3 = f"A:{u_sign}{user_pct:.0f}% | T:{t_sign}{time_pct:.0f}% | E:{e_sign}{eng_pct:.0f}%"
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
                
        # Read Column A (URL) and Column L (Combined Summary)
        # Check rows 2, 8, 12 as samples
        test_rows = [2, 8, 12]
        print("Fetching sample rows from Google Sheets...")
        
        for row_num in test_rows:
            result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!A{row_num}:L{row_num}").execute()
            values = result.get('values', [[]])[0]
            if len(values) < 12:
                print(f"Row {row_num} has incomplete columns.")
                continue
                
            url = values[0]
            sheet_val = values[11] # Column L is index 11
            
            path = url.replace("https://rwcclinic.com", "")
            if not path.startswith("/"):
                path = "/" + path
                
            print(f"\n--- Checking Row {row_num}: {path} ---")
            print("Value in Google Sheets:")
            print(sheet_val)
            
            print("Querying GA4 API directly...")
            curr, past = fetch_single_page_ytd(path)
            expected_val = format_expected_cell(curr, past)
            print("Expected Value from GA4 API:")
            print(expected_val)
            
            # Remove whitespace for comparison
            if sheet_val.strip() == expected_val.strip():
                print(">>> VERIFICATION SUCCESS: Data matches perfectly! <<<")
            else:
                print(">>> VERIFICATION FAILED: Data mismatch! <<<")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    from google.analytics.data_v1beta.types import FilterExpressionList
    main()
