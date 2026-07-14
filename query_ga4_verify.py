import os
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

def verify_page(path):
    req = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="activeUsers"), Metric(name="userEngagementDuration"), Metric(name="engagementRate")],
        date_ranges=[DateRange(start_date="90daysAgo", end_date="today")],
        dimension_filter=FilterExpression(
            filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value=path))
        )
    )
    res = ga4_client.run_report(req)
    if not res.rows:
        print(f"No GA4 data found for path: {path}")
        return
        
    for r in res.rows:
        users = r.metric_values[0].value
        tot_time = float(r.metric_values[1].value)
        eng_rate = float(r.metric_values[2].value) * 100
        avg_time = tot_time / float(users) if float(users) > 0 else 0
        print(f"GA4 Data for {path} (Organic not isolated):")
        print(f"  Active Users: {users}")
        print(f"  Avg Engagement Time: {avg_time:.1f}s")
        print(f"  Engagement Rate: {eng_rate:.1f}%")

    # Now run with Organic Traffic filter:
    req_org = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="activeUsers"), Metric(name="userEngagementDuration"), Metric(name="engagementRate")],
        date_ranges=[DateRange(start_date="90daysAgo", end_date="today")],
        dimension_filter=FilterExpression(
            filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value=path))
        ),
        metric_aggregations=[],
        dimension_filter_expression_list=[]
    )
    # Actually, we need channel grouping filter
    req_org.dimension_filter = FilterExpression(
        and_group=FilterExpressionList(
            expressions=[
                FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value=path))),
                FilterExpression(filter=Filter(field_name="sessionDefaultChannelGroup", in_list_filter=Filter.InListFilter(values=["Organic Search", "Organic Video", "Organic Social", "Organic Shopping"])))
            ]
        )
    )
    
    # We need to construct filter expression list
    # The SDK requires FilterExpression containing and_group which has FilterExpressionList
    from google.analytics.data_v1beta.types import FilterExpressionList
    res_org = ga4_client.run_report(req_org)
    if not res_org.rows:
        print(f"No GA4 Organic data found for path: {path}")
        return
    for r in res_org.rows:
        users = r.metric_values[0].value
        tot_time = float(r.metric_values[1].value)
        eng_rate = float(r.metric_values[2].value) * 100
        avg_time = tot_time / float(users) if float(users) > 0 else 0
        print(f"GA4 Organic Data for {path}:")
        print(f"  Active Users: {users}")
        print(f"  Avg Engagement Time: {avg_time:.1f}s")
        print(f"  Engagement Rate: {eng_rate:.1f}%")

if __name__ == "__main__":
    from google.analytics.data_v1beta.types import FilterExpressionList
    verify_page("/thread-lift-vs-botox/")
