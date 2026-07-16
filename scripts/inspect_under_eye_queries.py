import os
import sys
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Add scripts directory to path to import creds_info from the working script
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

from compare_gsc_fillers_only import creds_info

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
creds = service_account.Credentials.from_service_account_info(creds_info, scopes=SCOPES)
gsc_service = build('searchconsole', 'v1', credentials=creds)

url = 'https://rwcclinic.com/filler-under-eyes/'
site_url = 'https://rwcclinic.com/'

start_date = '2026-06-01'
end_date = '2026-06-30'

print(f"Querying GSC for {url} in June 2026...")

request = {
    'startDate': start_date,
    'endDate': end_date,
    'dimensions': ['query'],
    'dimensionFilterGroups': [{
        'filters': [{'dimension': 'page', 'expression': url, 'operator': 'equals'}]
    }],
    'rowLimit': 100
}

response = gsc_service.searchanalytics().query(siteUrl=site_url, body=request).execute()
rows = response.get('rows', [])

print(f"\n--- Search Queries for Under-Eye Filler Page (June 2026) ---")
print(f"{'Query':<45} | {'Clicks':<8} | {'Impressions':<12} | {'CTR (%)':<8} | {'Position':<8}")
print("-" * 85)

total_clicks = 0
total_imp = 0

for r in rows:
    query = r['keys'][0]
    clicks = r['clicks']
    imp = r['impressions']
    ctr = r['ctr'] * 100
    pos = r['position']
    total_clicks += clicks
    total_imp += imp
    print(f"{query:<45} | {clicks:<8} | {imp:<12} | {ctr:<8.1f}% | {pos:<8.1f}")

print(f"\nTotal Clicks: {total_clicks}")
print(f"Total Impressions: {total_imp}")
