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
path = "/if-diet/"

# 180 days
req_180 = RunReportRequest(
    property=f"properties/{property_id}",
    metrics=[Metric(name="activeUsers"), Metric(name="userEngagementDuration")],
    date_ranges=[DateRange(start_date="180daysAgo", end_date="today")],
    dimension_filter=FilterExpression(
        and_group=FilterExpressionList(
            expressions=[
                FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.EXACT, value=path))),
                FilterExpression(filter=Filter(field_name="sessionDefaultChannelGroup", in_list_filter=Filter.InListFilter(values=["Organic Search", "Organic Video", "Organic Social", "Organic Shopping"])))
            ]
        )
    )
)

# 90 days
req_90 = RunReportRequest(
    property=f"properties/{property_id}",
    metrics=[Metric(name="activeUsers"), Metric(name="userEngagementDuration")],
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

res_180 = ga4_client.run_report(req_180)
res_90 = ga4_client.run_report(req_90)

print("180 Days Active Users:", res_180.rows[0].metric_values[0].value if res_180.rows else 0)
print("90 Days Active Users:", res_90.rows[0].metric_values[0].value if res_90.rows else 0)
