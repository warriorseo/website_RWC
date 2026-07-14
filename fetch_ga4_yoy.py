import os
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    FilterExpression,
    FilterExpressionList,
    Filter
)
from dotenv import load_dotenv

load_dotenv(r"d:\AI-Cyborg-2558\00_agents\.env")

private_key = os.environ.get("GOOGLE_PRIVATE_KEY", "")
if "\\n" in private_key:
    private_key = private_key.replace("\\n", "\n")

credentials_info = {
    "type": os.environ.get("GOOGLE_SERVICE_ACCOUNT_TYPE"),
    "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
    "private_key_id": os.environ.get("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": private_key,
    "client_email": os.environ.get("GOOGLE_CLIENT_EMAIL"),
    "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
    "auth_uri": os.environ.get("GOOGLE_AUTH_URI"),
    "token_uri": os.environ.get("GOOGLE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.environ.get("GOOGLE_CLIENT_X509_CERT_URL")
}

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly', 'https://www.googleapis.com/auth/spreadsheets']
credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)

# Sheets client
sheets_service = build('sheets', 'v4', credentials=credentials)
sheet = sheets_service.spreadsheets()
sheet_id = "1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ"
target_gid = 199841076

# GA4 client
ga4_client = BetaAnalyticsDataClient(credentials=credentials)
property_id = "292925407"

def fetch_ga4_metrics_for_path(path):
    # Date ranges: last 90 days vs 90 days a year ago (455 days ago to 365 days ago)
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[
            Metric(name="userEngagementDuration"),
            Metric(name="engagementRate"),
            Metric(name="bounceRate")
        ],
        date_ranges=[
            DateRange(start_date="90daysAgo", end_date="today"),
            DateRange(start_date="455daysAgo", end_date="365daysAgo")
        ],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="pagePath",
                string_filter=StringFilter(match_type=StringFilter.MatchType.EXACT, value=path)
            )
        )
    )
    
    response = ga4_client.run_report(request)
    
    data_current = {"time": 0.0, "rate": 0.0, "bounce": 0.0}
    data_past = {"time": 0.0, "rate": 0.0, "bounce": 0.0}
    
    for row in response.rows:
        date_range = row.dimension_values[1].value # dimension 0 is pagePath, 1 is dateRange (implicit when using date_ranges)
        # Wait, if we don't explicitly add dateRange as dimension, they might not be separated?
        # Actually, let's just make two separate calls or add dateRange dimension? 
        # Adding dimension 'dateRange' is safer if we want rows split by date range.
        pass
    
    return None

def fetch_ga4_separately(path):
    # Current 6 months
    req_curr = RunReportRequest(
        property=f"properties/{property_id}",
        metrics=[Metric(name="userEngagementDuration"), Metric(name="engagementRate"), Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="365daysAgo", end_date="today")],
        dimension_filter=FilterExpression(
            and_group=FilterExpressionList(
                expressions=[
                    FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.EXACT, value=path))),
                    FilterExpression(filter=Filter(field_name="sessionDefaultChannelGroup", in_list_filter=Filter.InListFilter(values=["Organic Search", "Organic Video", "Organic Social", "Organic Shopping"])))
                ]
            )
        )
    )
    
    # Past 6 months
    req_past = RunReportRequest(
        property=f"properties/{property_id}",
        metrics=[Metric(name="userEngagementDuration"), Metric(name="engagementRate"), Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="730daysAgo", end_date="366daysAgo")],
        dimension_filter=FilterExpression(
            and_group=FilterExpressionList(
                expressions=[
                    FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.EXACT, value=path))),
                    FilterExpression(filter=Filter(field_name="sessionDefaultChannelGroup", in_list_filter=Filter.InListFilter(values=["Organic Search", "Organic Video", "Organic Social", "Organic Shopping"])))
                ]
            )
        )
    )
    
    try:
        res_curr = ga4_client.run_report(req_curr)
        res_past = ga4_client.run_report(req_past)
        
        def parse_res(res):
            if res.rows:
                total_time = float(res.rows[0].metric_values[0].value)
                eng_rate = float(res.rows[0].metric_values[1].value)
                users = float(res.rows[0].metric_values[2].value)
                avg_time = total_time / users if users > 0 else 0
                return avg_time, eng_rate, users
            return 0.0, 0.0, 0.0

        curr_time, curr_eng, curr_users = parse_res(res_curr)
        past_time, past_eng, past_users = parse_res(res_past)
        
        if curr_users == 0 and past_users == 0:
            user_summary = "ข้อมูลไม่ครบ (เป็น 0 ทั้งสองปี)"
            metric_summary = "ข้อมูลไม่ครบ"
        elif curr_users == 0:
            user_summary = "ข้อมูลไม่ครบ (ปีนี้เป็น 0)"
            metric_summary = "ข้อมูลไม่ครบ"
        elif past_users == 0:
            user_summary = "ข้อมูลไม่ครบ (ปีที่แล้วเป็น 0)"
            metric_summary = "ข้อมูลไม่ครบ"
        else:
            user_diff = curr_users - past_users
            user_summary = f"ปีนี้: {int(curr_users)} | ปีก่อน: {int(past_users)}\n(ต่าง: {'+' if user_diff > 0 else ''}{int(user_diff)})"
            
            time_diff = curr_time - past_time
            eng_diff = (curr_eng - past_eng) * 100
            metric_summary = (
                f"Time: {'+' if time_diff > 0 else ''}{time_diff:.1f}s\n"
                f"Eng Rate: {'+' if eng_diff > 0 else ''}{eng_diff:.1f}%"
            )
        return user_summary, metric_summary
    except Exception as e:
        print(f"Error fetching data for {path}: {e}")
        return None, None

def main():
    try:
        sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        target_sheet_name = None
        for s in sheets:
            if s.get("properties", {}).get("sheetId") == target_gid:
                target_sheet_name = s.get("properties", {}).get("title")
                break
                
        result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!A:A").execute()
        rows = result.get('values', [])
        if not rows:
            print("No data found.")
            return

        summary_user_column = [["GA4 Active Users YoY"]]
        summary_metric_column = [["GA4 YoY Summary"]]
        
        print("Fetching GA4 metrics for the first 20 URLs...")
        for i, row in enumerate(rows):
            if i == 0:
                continue
            if i > 20: 
                break
                
            url = row[0]
            path = url.replace("https://rwcclinic.com", "")
            if not path.startswith("/"):
                path = "/" + path
                
            print(f"Fetching {path}...")
            user_sum, metric_sum = fetch_ga4_separately(path)
            if user_sum:
                summary_user_column.append([user_sum])
                summary_metric_column.append([metric_sum])
            else:
                summary_user_column.append([""])
                summary_metric_column.append([""])

        print("Inserting column between K and L (index 11) for Active Users...")
        batch_update_request = {
            "requests": [
                {
                    "insertDimension": {
                        "range": {
                            "sheetId": target_gid,
                            "dimension": "COLUMNS",
                            "startIndex": 11,
                            "endIndex": 12
                        },
                        "inheritFromBefore": True
                    }
                }
            ]
        }
        
        sheet.batchUpdate(spreadsheetId=sheet_id, body=batch_update_request).execute()
        print("Column inserted successfully.")
        
        time.sleep(2)
        
        print("Writing data to the new columns L and M...")
        
        # Write Active Users YoY to L
        sheet.values().update(
            spreadsheetId=sheet_id,
            range=f"'{target_sheet_name}'!L1:L{len(summary_user_column)}",
            valueInputOption="USER_ENTERED",
            body={"values": summary_user_column}
        ).execute()
        
        # Write Metrics YoY to M
        sheet.values().update(
            spreadsheetId=sheet_id,
            range=f"'{target_sheet_name}'!M1:M{len(summary_metric_column)}",
            valueInputOption="USER_ENTERED",
            body={"values": summary_metric_column}
        ).execute()
        
        print("Update completed successfully!")
        
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
