import os
import sys
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest, FilterExpression, FilterExpressionList, Filter,
)

# Import credentials dynamically from the working script
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

from compare_gsc_fillers_only import creds_info

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/analytics.readonly']
creds = service_account.Credentials.from_service_account_info(creds_info, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
ga4_client = BetaAnalyticsDataClient(credentials=creds)

property_id = "292925407"
SPREADSHEET_ID = '1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ'
SHEET_NAME = 'URL Revision and Engagement'
START_DATE = '2025-07-01'

print("1. Reading current URLs from Column A (Rows 2 to 12) to match exact order...")
result = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range=f"'{SHEET_NAME}'!A2:A12"
).execute()

values = result.get('values', [])
urls_in_order = []
for row in values:
    if row and row[0].startswith('https://'):
        urls_in_order.append(row[0])
    else:
        urls_in_order.append(None) # Keep index aligned even if a row is empty/invalid

print(f"URLs in order: {urls_in_order}")

print("\n2. Querying GA4 for months list (July 2025 to today)...")
req_months = RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[Dimension(name="yearMonth")],
    metrics=[Metric(name="activeUsers")],
    date_ranges=[DateRange(start_date=START_DATE, end_date="today")],
)
res_months = ga4_client.run_report(req_months)
months = sorted([row.dimension_values[0].value for row in res_months.rows])
print(f"Months list ({len(months)}): {months}")

# Build GA4 hyperlink template
today_str = datetime.datetime.now().strftime('%Y%m%d')
date_params = f"%26_u.dateOption%3Dcustom%26_u.dateStart%3D20251101%26_u.dateEnd%3D{today_str}"
template = "https://analytics.google.com/analytics/web/?hl=en#/a149800124p292925407/reports/explorer?params=_u..nav%3Dmaui%26_r.explorerCard..filterTerm%3D%252F{slug}%252F%26_r.explorerCard..startRow%3D0%26_u..built_comparisons_enabled%3Dtrue%26_u..comparisons%3D%5B%7B%22savedComparisonId%22:%227523527606%22,%22name%22:%22Organic%20traffic%22,%22isEnabled%22:true,%22filters%22:%5B%7B%22fieldName%22:%22sessionDefaultChannelGrouping%22,%22evaluationType%22:8,%22expressionList%22:%5B%22Organic%20Search%22,%22Organic%20Video%22,%22Organic%20Social%22,%22Organic%20Shopping%22%5D,%22isCaseSensitive%22:true%7D%5D,%22systemDefinedSavedComparisonType%22:2,%22isSystemDefined%22:true%7D%5D%26_r.explorerCard..seldim%3D%5B%22unifiedPagePathScreen%22%5D%26_u.comparisonOption%3Ddisabled%26_r.explorerCard..dateGranularity%3DnthMonth%26_r.explorerCard..sortKey%3DuserEngagementDurationPerUser%26_r.explorerCard..selmet%3D%5B%22userEngagementDurationPerUser%22,%22screenPageViews%22%5D" + date_params + "&ruid=0d646679-6477-4cd0-a2cc-a3c33313c77f&collectionId=10576530072&r=15246722299"

update_rows = []

print("\n3. Fetching GA4 metrics and preparing update data for Columns B to P...")
for idx, url in enumerate(urls_in_order):
    if not url:
        # If the row doesn't have a valid URL, add an empty row of 15 elements
        update_rows.append([""] * 15)
        continue
        
    slug = url.replace('https://rwcclinic.com/', '').replace('/', '')
    print(f"  Fetching for {slug}...")
    
    req = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="yearMonth")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date=START_DATE, end_date="today")],
        dimension_filter=FilterExpression(
            and_group=FilterExpressionList(
                expressions=[
                    FilterExpression(
                        filter=Filter(
                            field_name="pagePath",
                            string_filter=Filter.StringFilter(value=f"/{slug}/"),
                        )
                    ),
                    FilterExpression(
                        filter=Filter(
                            field_name="sessionDefaultChannelGroup",
                            string_filter=Filter.StringFilter(value="Organic Search"),
                        )
                    )
                ]
            )
        )
    )
    
    res = ga4_client.run_report(req)
    data = {}
    total_users = 0
    count_months = len(months)
    
    for row in res.rows:
        ym = row.dimension_values[0].value
        users = int(row.metric_values[0].value)
        data[ym] = users
        total_users += users
        
    avg_monthly_users = total_users / count_months if count_months > 0 else 0
    
    # Construct update row: [avg_users, users_month_1, ..., users_month_13, hyperlink]
    row_data = [f"{avg_monthly_users:.1f}"]
    for m in months:
        if m in data:
            row_data.append(str(data[m]))
        else:
            row_data.append("0")
            
    ga4_link = template.replace('{slug}', slug)
    row_data.append(f'=HYPERLINK("{ga4_link}", "GA4 Data")')
    
    update_rows.append(row_data)

# Let's write specifically to B2:P12
update_range = f"'{SHEET_NAME}'!B2:P12"
print(f"\n4. Overwriting ONLY Columns B to P for Rows 2 to 12 (range: {update_range})...")

body = {
    'values': update_rows
}
result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=update_range,
    valueInputOption="USER_ENTERED",
    body=body
).execute()
print(f"Successfully updated {result.get('updatedCells')} cells in Google Sheet without affecting other columns or rows!")
