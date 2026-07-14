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

def fetch_90d_data():
    req = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="engagementRate")],
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
        eng_rate = float(row.metric_values[0].value) * 100
        data[path] = f"{eng_rate:.1f}%"
    return data

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

def process_yoy_diff(path, curr_data, past_data):
    curr = curr_data.get(path, (0.0, 0.0, 0.0))
    past = past_data.get(path, (0.0, 0.0, 0.0))
    
    curr_time, curr_eng, curr_users = curr
    past_time, past_eng, past_users = past
    
    if curr_users == 0 and past_users == 0:
        return "ข้อมูลไม่ครบ (เป็น 0 ทั้งสองปี)", "ข้อมูลไม่ครบ"
    elif curr_users == 0:
        return "ข้อมูลไม่ครบ (ปีนี้เป็น 0)", "ข้อมูลไม่ครบ"
    elif past_users == 0:
        return "ข้อมูลไม่ครบ (ปีที่แล้วเป็น 0)", "ข้อมูลไม่ครบ"
    
    user_diff = curr_users - past_users
    user_summary = f"ปีนี้: {int(curr_users)} | ปีก่อน: {int(past_users)}\n(ต่าง: {'+' if user_diff > 0 else ''}{int(user_diff)})"
    
    time_diff = curr_time - past_time
    eng_diff = (curr_eng - past_eng) * 100
    metric_summary = (
        f"Time: {'+' if time_diff > 0 else ''}{time_diff:.1f}s\n"
        f"Eng Rate: {'+' if eng_diff > 0 else ''}{eng_diff:.1f}%"
    )
    return user_summary, metric_summary

def main():
    sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    target_sheet_name = None
    for s in sheets:
        if s.get("properties", {}).get("sheetId") == target_gid:
            target_sheet_name = s.get("properties", {}).get("title")
            break

    print("Fetching data from GA4...")
    data_90d = fetch_90d_data()
    curr_yoy, past_yoy = fetch_yoy_data()

    print("Fetching URLs from Google Sheets...")
    result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!A:A").execute()
    rows = result.get('values', [])
    
    col_k = [["Engagement Rate\n(3 เดือนล่าสุด)"]]
    col_l = [["GA4 Link"]]
    col_m = [["GA4 Active Users\nYoY (6 เดือน)"]]
    col_n = [["GA4 YoY\nSummary (6 เดือน)"]]
    col_o = [["GA4 Link Compare\n(90 วัน)"]]
    
    print("Processing data...")
    for i, row in enumerate(rows):
        if i == 0:
            continue
            
        url = row[0] if len(row) > 0 else ""
        if not url or "rwcclinic.com" not in url:
            col_k.append([""])
            col_l.append([""])
            col_m.append([""])
            col_n.append([""])
            col_o.append([""])
            continue
            
        path = url.replace("https://rwcclinic.com", "")
        if not path.startswith("/"):
            path = "/" + path
            
        # 90d Engagement Rate (Col K)
        eng_rate_val = data_90d.get(path, "N/A")
        col_k.append([eng_rate_val])
        
        # GA4 Link (Col L)
        path_encoded = urllib.parse.quote(urllib.parse.quote(path, safe=''), safe='')
        ga4_url_base = f'https://analytics.google.com/analytics/web/?hl=en#/a149800124p292925407/reports/explorer?params=_u..nav%3Dmaui%26_u..built_comparisons_enabled%3Dtrue%26_u..comparisons%3D%5B%7B%22savedComparisonId%22:%227523527606%22,%22name%22:%22Organic%20traffic%22,%22isEnabled%22:true,%22filters%22:%5B%7B%22fieldName%22:%22sessionDefaultChannelGrouping%22,%22evaluationType%22:8,%22expressionList%22:%5B%22Organic%20Search%22,%22Organic%20Video%22,%22Organic%20Social%22,%22Organic%20Shopping%22%5D,%22isCaseSensitive%22:true%7D%5D,%22systemDefinedSavedComparisonType%22:2,%22isSystemDefined%22:true%7D%5D%26_u.dateOption%3Dlast90Days%26_u.comparisonOption%3Ddisabled%26_r.explorerCard..filterTerm%3D{path_encoded}%26_r.explorerCard..startRow%3D0&ruid=0d646679-6477-4cd0-a2cc-a3c33313c77f&collectionId=10576530072'
        col_l.append([f'=HYPERLINK("{ga4_url_base}", "View in GA4")'])
        
        # YoY Data (Col M, N)
        user_sum, metric_sum = process_yoy_diff(path, curr_yoy, past_yoy)
        col_m.append([user_sum])
        col_n.append([metric_sum])
        
        # GA4 Link Compare (Col O)
        ga4_url_compare = f'https://analytics.google.com/analytics/web/?hl=en#/a149800124p292925407/reports/explorer?params=_u..nav%3Dmaui%26_u..built_comparisons_enabled%3Dtrue%26_u..comparisons%3D%5B%7B%22savedComparisonId%22:%227523527606%22,%22name%22:%22Organic%20traffic%22,%22isEnabled%22:true,%22filters%22:%5B%7B%22fieldName%22:%22sessionDefaultChannelGrouping%22,%22evaluationType%22:8,%22expressionList%22:%5B%22Organic%20Search%22,%22Organic%20Video%22,%22Organic%20Social%22,%22Organic%20Shopping%22%5D,%22isCaseSensitive%22:true%7D%5D,%22systemDefinedSavedComparisonType%22:2,%22isSystemDefined%22:true%7D%5D%26_u.dateOption%3Dlast90Days%26_u.comparisonOption%3DyearOverYear%26_r.explorerCard..filterTerm%3D{path_encoded}%26_r.explorerCard..startRow%3D0&ruid=0d646679-6477-4cd0-a2cc-a3c33313c77f&collectionId=10576530072'
        col_o.append([f'=HYPERLINK("{ga4_url_compare}", "Compare in GA4")'])

    print(f"Updating 5 columns for {len(rows)} rows...")
    
    # We can batch update all 5 columns at once
    body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": f"'{target_sheet_name}'!K1:K{len(col_k)}", "values": col_k},
            {"range": f"'{target_sheet_name}'!L1:L{len(col_l)}", "values": col_l},
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

if __name__ == "__main__":
    main()
