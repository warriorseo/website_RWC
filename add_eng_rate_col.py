import os
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Metric,
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

def fetch_ga4_eng_rate(path):
    req = RunReportRequest(
        property=f"properties/{property_id}",
        metrics=[Metric(name="engagementRate")],
        date_ranges=[DateRange(start_date="90daysAgo", end_date="today")],
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
        res = ga4_client.run_report(req)
        if res.rows:
            eng_rate = float(res.rows[0].metric_values[0].value) * 100
            return f"{eng_rate:.1f}%"
        return "N/A"
    except Exception as e:
        print(f"Error for {path}: {e}")
        return "Error"

def main():
    sheet_metadata = sheet.get(spreadsheetId=sheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    target_sheet_name = None
    for s in sheets:
        if s.get("properties", {}).get("sheetId") == target_gid:
            target_sheet_name = s.get("properties", {}).get("title")
            break

    # Read the current headers G to J to modify them
    header_res = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!G1:J1").execute()
    headers = header_res.get('values', [[]])[0]
    
    new_headers = []
    for h in headers:
        if "(3 เดือนล่าสุด)" not in h:
            new_headers.append(f"{h} (3 เดือนล่าสุด)")
        else:
            new_headers.append(h)
            
    # Update G1:J1
    sheet.values().update(
        spreadsheetId=sheet_id,
        range=f"'{target_sheet_name}'!G1:J1",
        valueInputOption="USER_ENTERED",
        body={"values": [new_headers]}
    ).execute()
    print("Headers G1:J1 updated.")

    # Read URLs from Column A
    result = sheet.values().get(spreadsheetId=sheet_id, range=f"'{target_sheet_name}'!A:A").execute()
    rows = result.get('values', [])
    
    eng_rate_col = [["Engagement Rate (3 เดือนล่าสุด)"]]
    
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
        eng_rate = fetch_ga4_eng_rate(path)
        eng_rate_col.append([eng_rate])

    # Insert column after J (index 10)
    print("Inserting column after J (index 10)...")
    batch_update_request = {
        "requests": [
            {
                "insertDimension": {
                    "range": {
                        "sheetId": target_gid,
                        "dimension": "COLUMNS",
                        "startIndex": 10,
                        "endIndex": 11
                    },
                    "inheritFromBefore": True
                }
            }
        ]
    }
    
    sheet.batchUpdate(spreadsheetId=sheet_id, body=batch_update_request).execute()
    print("Column inserted successfully.")
    
    time.sleep(2)
    
    # Write new column to K
    print("Writing data to the new column K...")
    sheet.values().update(
        spreadsheetId=sheet_id,
        range=f"'{target_sheet_name}'!K1:K{len(eng_rate_col)}",
        valueInputOption="USER_ENTERED",
        body={"values": eng_rate_col}
    ).execute()
    
    print("Update completed successfully!")

if __name__ == "__main__":
    main()
