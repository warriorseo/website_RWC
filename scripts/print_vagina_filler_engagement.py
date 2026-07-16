import os
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest, FilterExpression, FilterExpressionList, Filter,
)

creds_info = {
    'type': 'service_account',
    'project_id': 'gen-lang-client-0042204106',
    'private_key_id': '800e02ba1d02083ec1711ff5f6e033618d050e84',
    'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDCPHGzqmmzNHxw\n8i12B/ILqU6iO6VWhOzSIVqiCkRVO7p6T6/FMJhqywGtMOKDk97z3tUf72nsaP5f\n244l4uow/Ta2im7YIK6YKqroM3vD8ukhLFYxDfXA3+jcRoAX3BhSLIIGDE/f4jux\nhle+/Z7M55rDK+RSBTYaRFsU5yr0ffk0tjmCYrIutRtnp0Efq67TCJveCfdCkK9R\nRPWto5+ZUOvdCTNlFwRpByNE9WO1+AvmM7ylZriXT95PvpgMf7M8mUe2onG5Kk+x\n5HluCFhQYQXrSntLLRE6x1SbX9MUE37A7D/n6Wx1hlwiQaWFi4kiiOFpD2myRU0Y\nonOVMIFrAgMBAAECggEAHHu1psWuM2fWec+hyAW5QmmFDPhXMh1TByt5+Xos9BzK\np0YJPg72wu5bJBUfmnD0SGnccg7vRwpMhy0QptCkTCPNwq4BPDNqtwjGwD9Qfncg\nJcu1JgNojuym3qp9/UG61U4OkSl8CxZHb6yGMI1LnLu377f/huGZwfdVLfcKTwjq\nt5J9Kg3vPIkKokaiehLo+4eOEupuZfjXUoV7aY/vDrAl8LlGgJg5YYRG1wLnKQ5D\nVL0jcecNA5HQ6DSdyGJ6leVJWoYAcTi4qMhOi0EABRmZM72hYIWpMHOJjedpurro\nxtndjUwr/JqVNY7Tqkv0QU7OcciJYpvHrFLhKWLDMQKBgQDkd0u/2O6hhucbaJ56\nLrUPPr/O2mTtKe9975lSoHuOJoXBvUv8C010xkbSytDVJAFUh8juMcDUOMMRfm/P\nNC4sfQNMqonvzmSYr32JGNwg5zosqrMw6YQ+dmmyYB9h/zRYn0PrwDt+Rk6lW7Fk\n2mPQvcR7XcrvEpbDX+IsdmjKWwKBgQDZpRO5TD77ZkhDAf9JlFkB8J9Ugb8ix0kb\nqYsxtR+iWnRqfzqbO0tu2hK8FceIuW3lR09aATMxbbKt5A9Y+wv9aJq6k3+HcDw9\n42/XIcmp4gQyz92LPWQ2dHyxY8gW/VVux0XJJ/CYuVFslhveBsj7hsuEdjDoxB4W\npRCGFZQyMQKBgGmRgkwc5m93EZVFq20T5hAsU582pUo9hW+w5i0bANy3ijjyyoil\nhF4APLusggDrCT5RHBSMouitbd3Iicu59dgS0BJ9/wzzVuKCvMQ724PMtMHtAq4I\nSVY/iymkZvv2W+7TcSQfiJ4ZyL959id/Dn5nIcJLnbkI4udWiAE5mcRfAoGAcaEl\n8xBDsa1s/M8GIbw53DFsfgpfaCDzomWaLpGJupHPReq3BmSmtXFVZq1YR6HIJnRc\nkXke6SeEqhTvjl1DnUIHxnFLm8KVMRqVQZR6XR+LYZv05sVelK+silC2HoqVGAkh\n/ivECXh3cmHMmtagB/IQP1AVqPD7ZIc5YUfS34ECgYB0pT6N5TbPDKHfftsZNgI0\nHHQN07jruHQ5naDR5L7F2n4rSVJH7dcwedHZaQxR+F1fYdKEWstqR73WPW4chluR\nyNE53+Xlt+Yt3cRhTKNBtCV7EMiA0S/yIt0Ai20o5MOc3P1xys1AopxFKFE1xBNm\nvQV+INvYA9APPlVNSKshbQ==\n-----END PRIVATE KEY-----\n',
    'client_email': 'aiwar-841@gen-lang-client-0042204106.iam.gserviceaccount.com',
    'token_uri': 'https://oauth2.googleapis.com/token',
}

creds = service_account.Credentials.from_service_account_info(creds_info)
ga4_client = BetaAnalyticsDataClient(credentials=creds)

property_id = "292925407"
slug = "vagina-filler"
START_DATE = '2025-07-01'

print(f"Querying GA4 for {slug}...")

# First run a general report to get all months
req_months = RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[Dimension(name="yearMonth")],
    metrics=[Metric(name="activeUsers")],
    date_ranges=[DateRange(start_date=START_DATE, end_date="today")],
)
res_months = ga4_client.run_report(req_months)
all_months = sorted([row.dimension_values[0].value for row in res_months.rows])

# Query specific metrics for the URL
req = RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[Dimension(name="yearMonth")],
    metrics=[Metric(name="activeUsers"), Metric(name="userEngagementDuration")],
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
for row in res.rows:
    ym = row.dimension_values[0].value
    users = int(row.metric_values[0].value)
    duration = float(row.metric_values[1].value)
    avg_eng = duration / users if users > 0 else 0
    data[ym] = {"users": users, "eng": avg_eng, "duration": duration}

print("\n--- GA4 Statistics (Organic Search Only) ---")
print(f"URL: https://rwcclinic.com/{slug}/")
print(f"{'Month':<10} | {'Active Users':<12} | {'Total Duration (s)':<20} | {'Avg Engagement Time (s)':<25}")
print("-" * 75)

for m in all_months:
    m_display = f"{m[:4]}-{m[4:]}"
    if m in data:
        print(f"{m_display:<10} | {data[m]['users']:<12} | {data[m]['duration']:<20.1f} | {data[m]['eng']:<25.2f}")
    else:
        print(f"{m_display:<10} | {'0':<12} | {'0.0':<20} | {'0.00':<25}")
