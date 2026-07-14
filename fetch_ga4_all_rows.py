import os
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Metric,
    Dimension,
    RunReportRequest,
    FilterExpression,
    FilterExpressionList,
    Filter
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
    
    print("Running GA4 reports for YoY...")
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
    try:
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
        
        # Read existing headers for K, L, M
        header_result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!K1:M1").execute()
        headers = header_result.get('values', [["", "", ""]])[0]
        
        col_k = [[headers[0]] if len(headers) > 0 else ["Engagement Rate\n(3 เดือนล่าสุด)"]]
        col_l = [[headers[1]] if len(headers) > 1 else ["GA4 Active Users\nYoY"]]
        col_m = [[headers[2]] if len(headers) > 2 else ["GA4 YoY\nSummary"]]
        
        print("Processing data...")
        for i, row in enumerate(rows):
            if i == 0:
                continue
                
            url = row[0] if len(row) > 0 else ""
            if not url or "rwcclinic.com" not in url:
                col_k.append([""])
                col_l.append([""])
                col_m.append([""])
                continue
                
            path = url.replace("https://rwcclinic.com", "")
            if not path.startswith("/"):
                path = "/" + path
                
            # 90d
            eng_rate_val = data_90d.get(path, "N/A")
            # YoY
            user_sum, metric_sum = process_yoy_diff(path, curr_yoy, past_yoy)
            
            col_k.append([eng_rate_val])
            col_l.append([user_sum])
            col_m.append([metric_sum])

        print(f"Updating {len(col_k)-1} rows...")
        
        sheet.values().update(
            spreadsheetId=sheet_id,
            range=f"'{target_sheet_name}'!K1:K{len(col_k)}",
            valueInputOption="USER_ENTERED",
            body={"values": col_k}
        ).execute()
        
        sheet.values().update(
            spreadsheetId=sheet_id,
            range=f"'{target_sheet_name}'!L1:L{len(col_l)}",
            valueInputOption="USER_ENTERED",
            body={"values": col_l}
        ).execute()
        
        sheet.values().update(
            spreadsheetId=sheet_id,
            range=f"'{target_sheet_name}'!M1:M{len(col_m)}",
            valueInputOption="USER_ENTERED",
            body={"values": col_m}
        ).execute()
        
        print("Update completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
