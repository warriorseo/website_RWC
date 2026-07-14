import os
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
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

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)

client = BetaAnalyticsDataClient(credentials=credentials)
property_id = "292925407" # Extracted from the GA4 URL

try:
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[DateRange(start_date="yesterday", end_date="today")],
        limit=5
    )
    response = client.run_report(request)
    print("GA4 API Access Successful!")
    print("Report result:")
    for row in response.rows:
        print(f"{row.dimension_values[0].value}: {row.metric_values[0].value}")
except Exception as e:
    print(f"Error accessing GA4: {e}")
