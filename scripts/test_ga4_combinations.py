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

# We will test various combinations for pagePath "/vagina-filler/"
combinations = [
    # 1. Exact pagePath + sessionSourceMedium = google / organic
    ("pagePath EXACT /vagina-filler/ + sessionSourceMedium EXACT google / organic", 
     FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value="/vagina-filler/"))),
     FilterExpression(filter=Filter(field_name="sessionSourceMedium", string_filter=Filter.StringFilter(value="google / organic")))),
    
    # 2. Exact pagePath + sessionSource = google, sessionMedium = organic (just in case)
    ("pagePath EXACT /vagina-filler/ + sessionMedium EXACT organic", 
     FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value="/vagina-filler/"))),
     FilterExpression(filter=Filter(field_name="sessionMedium", string_filter=Filter.StringFilter(value="organic")))),
     
    # 3. Contains pagePath "vagina-filler" + sessionSourceMedium = google / organic
    ("pagePath CONTAINS vagina-filler + sessionSourceMedium EXACT google / organic", 
     FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value="vagina-filler", match_type=Filter.StringFilter.MatchType.CONTAINS))),
     FilterExpression(filter=Filter(field_name="sessionSourceMedium", string_filter=Filter.StringFilter(value="google / organic")))),
     
    # 4. Exact pagePath + firstUserSourceMedium = google / organic
    ("pagePath EXACT /vagina-filler/ + firstUserSourceMedium EXACT google / organic", 
     FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value="/vagina-filler/"))),
     FilterExpression(filter=Filter(field_name="firstUserSourceMedium", string_filter=Filter.StringFilter(value="google / organic")))),

    # 5. Exact pagePath + firstUserDefaultChannelGroup = Organic Search
    ("pagePath EXACT /vagina-filler/ + firstUserDefaultChannelGroup = Organic Search", 
     FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value="/vagina-filler/"))),
     FilterExpression(filter=Filter(field_name="firstUserDefaultChannelGroup", string_filter=Filter.StringFilter(value="Organic Search")))),
     
    # 6. Exact pagePath + NO CHANNEL FILTER
    ("pagePath EXACT /vagina-filler/ (All traffic)", 
     FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value="/vagina-filler/"))),
     None)
]

for desc, page_filter, channel_filter in combinations:
    exprs = [page_filter]
    if channel_filter:
        exprs.append(channel_filter)
        
    req = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="yearMonth")],
        metrics=[Metric(name="activeUsers"), Metric(name="userEngagementDuration")],
        date_ranges=[DateRange(start_date="2025-07-01", end_date="2025-07-31")],
        dimension_filter=FilterExpression(
            and_group=FilterExpressionList(expressions=exprs)
        )
    )
    res = ga4_client.run_report(req)
    if res.rows:
        row = res.rows[0]
        users = int(row.metric_values[0].value)
        dur = float(row.metric_values[1].value)
        print(f"{desc}:")
        print(f"  Users = {users}, Avg Eng = {dur/users:.2f}s (Total duration = {dur})")
    else:
        print(f"{desc}: No data")
