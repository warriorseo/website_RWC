import os
import datetime
from google.oauth2 import service_account
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

credentials = service_account.Credentials.from_service_account_info(credentials_info)
ga4_client = BetaAnalyticsDataClient(credentials=credentials)
property_id = "292925407"

def main():
    path = "/fat-grifting-forehead-physiognomy/"
    today = datetime.datetime.now()
    ytd_start = "2026-01-01"
    ytd_end = today.strftime("%Y-%m-%d")
    
    print(f"Querying GA4 API for {path} YTD ({ytd_start} to {ytd_end})...")
    req = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="userEngagementDuration"), Metric(name="engagementRate"), Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date=ytd_start, end_date=ytd_end)],
        dimension_filter=FilterExpression(
            filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value=path))
        )
    )
    res = ga4_client.run_report(req)
    if not res.rows:
        print("No rows found!")
        return
        
    for r in res.rows:
        duration = r.metric_values[0].value
        rate = r.metric_values[1].value
        users = r.metric_values[2].value
        print(f"Path: {r.dimension_values[0].value}")
        print(f"  userEngagementDuration: {duration}s")
        print(f"  engagementRate: {rate}")
        print(f"  activeUsers: {users}")

if __name__ == "__main__":
    main()
