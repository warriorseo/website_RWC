import os
from google.oauth2 import service_account
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

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
ga4_client = BetaAnalyticsDataClient(credentials=credentials)
property_id = "292925407"
path = "/trans-fat/"

# Test ALL traffic 90 days
req_all = RunReportRequest(
    property=f"properties/{property_id}",
    metrics=[Metric(name="activeUsers")],
    date_ranges=[DateRange(start_date="90daysAgo", end_date="today")],
    dimension_filter=FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.EXACT, value=path)))
)

# Test Organic traffic 90 days
req_org = RunReportRequest(
    property=f"properties/{property_id}",
    metrics=[Metric(name="activeUsers")],
    date_ranges=[DateRange(start_date="90daysAgo", end_date="today")],
    dimension_filter=FilterExpression(
        and_group=FilterExpressionList(
            expressions=[
                FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.EXACT, value=path))),
                FilterExpression(filter=Filter(field_name="sessionDefaultChannelGroup", string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.EXACT, value="Organic Search")))
            ]
        )
    )
)

print("All traffic users:", ga4_client.run_report(req_all).rows[0].metric_values[0].value if ga4_client.run_report(req_all).rows else 0)
print("Organic traffic users:", ga4_client.run_report(req_org).rows[0].metric_values[0].value if ga4_client.run_report(req_org).rows else 0)
