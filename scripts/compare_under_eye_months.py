import os
import sys
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

from compare_gsc_fillers_only import creds_info

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
creds = service_account.Credentials.from_service_account_info(creds_info, scopes=SCOPES)
gsc_service = build('searchconsole', 'v1', credentials=creds)

url = 'https://rwcclinic.com/filler-under-eyes/'
site_url = 'https://rwcclinic.com/'

periods = [
    ('Month 5 (May 2026)', '2026-05-01', '2026-05-31'),
    ('Month 6 (June 2026)', '2026-06-01', '2026-06-30'),
    ('Month 7 (July 2026)', '2026-07-01', '2026-07-14') # July partial data
]

keywords_of_interest = ['ฟิลเลอร์ใต้ตา', 'ฉีดฟิลเลอร์ใต้ตา', 'filler ใต้ ตา', 'ฟิ ล เลอ ร์ ใต้ ตา']

for label, start, end in periods:
    request = {
        'startDate': start,
        'endDate': end,
        'dimensions': ['query'],
        'dimensionFilterGroups': [{
            'filters': [{'dimension': 'page', 'expression': url, 'operator': 'equals'}]
        }],
        'rowLimit': 100
    }
    try:
        response = gsc_service.searchanalytics().query(siteUrl=site_url, body=request).execute()
        rows = response.get('rows', [])
        
        # Calculate summary metrics
        total_clicks = sum(r['clicks'] for r in rows)
        total_imp = sum(r['impressions'] for r in rows)
        avg_pos = sum(r['position'] * r['impressions'] for r in rows) / total_imp if total_imp > 0 else 0
        
        print(f"\n================== {label} ({start} to {end}) ==================")
        print(f"Total Clicks: {total_clicks} | Total Impressions: {total_imp} | Weighted Avg Position: {avg_pos:.1f}")
        
        # Find specific keyword rankings
        kw_data = {kw: "No Imp" for kw in keywords_of_interest}
        for r in rows:
            q = r['keys'][0]
            if q in kw_data:
                kw_data[q] = f"Pos: {r['position']:.1f} | Clicks: {r['clicks']} | Imp: {r['impressions']}"
                
        print("Keyword Rankings:")
        for kw, details in kw_data.items():
            print(f"  - {kw:<22}: {details}")
            
    except Exception as e:
        print(f"Error querying {label}: {e}")
