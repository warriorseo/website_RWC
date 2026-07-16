import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

creds_info = {
    'type': 'service_account',
    'project_id': 'gen-lang-client-0042204106',
    'private_key_id': '800e02ba1d02083ec1711ff5f6e033618d050e84',
    'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDCPHGzqmmzNHxw\n8i12B/ILqU6iO6VWhOzSIVqiCkRVO7p6T6/FMJhqywGtMOKDk97z3tUf72nsaP5f\n244l4uow/Ta2im7YIK6YKqroM3vD8ukhLFYxDfXA3+jcRoAX3BhSLIIGDE/f4jux\nhle+/Z7M55rDK+RSBTYaRFsU5yr0ffk0tjmCYrIutRtnp0Efq67TCJveCfdCkK9R\nRPWto5+ZUOvdCTNlFwRpByNE9WO1+AvmM7ylZriXT95PvpgMf7M8mUe2onG5Kk+x\n5HluCFhQYQXrSntLLRE6x1SbX9MUE37A7D/n6Wx1hlwiQaWFi4kiiOFpD2myRU0Y\nonOVMIFrAgMBAAECggEAHHu1psWuM2fWec+hyAW5QmmFDPhXMh1TByt5+Xos9BzK\np0YJPg72wu5bJBUfmnD0SGnccg7vRwpMhy0QptCkTCPNwq4BPDNqtwjGwD9Qfncg\nJcu1JgNojuym3qp9/UG61U4OkSl8CxZHb6yGMI1LnLu377f/huGZwfdVLfcKTwjq\nt5J9Kg3vPIkKokaiehLo+4eOEupuZfjXUoV7aY/vDrAl8LlGgJg5YYRG1wLnKQ5D\nVL0jcecNA5HQ6DSdyGJ6leVJWoYAcTi4qMhOi0EABRmZM72hYIWpMHOJjedpurro\nxtndjUwr/JqVNY7Tqkv0QU7OcciJYpvHrFLhKWLDMQKBgQDkd0u/2O6hhucbaJ56\nLrUPPr/O2mTtKe9975lSoHuOJoXBvUv8C010xkbSytDVJAFUh8juMcDUOMMRfm/P\nNC4sfQNMqonvzmSYr32JGNwg5zosqrMw6YQ+dmmyYB9h/zRYn0PrwDt+Rk6lW7Fk\n2mPQvcR7XcrvEpbDX+IsdmjKWwKBgQDZpRO5TD77ZkhDAf9JlFkB8J9Ugb8ix0kb\nqYsxtR+iWnRqfzqbO0tu2hK8FceIuW3lR09aATMxbbKt5A9Y+wv9aJq6k3+HcDw9\n42/XIcmp4gQyz92LPWQ2dHyxY8gW/VVux0XJJ/CYuVFslhveBsj7hsuEdjDoxB4W\npRCGFZQyMQKBgGmRgkwc5m93EZVFq20T5hAsU582pUo9hW+w5i0bANy3ijjyyoil\nhF4APLusggDrCT5RHBSMouitbd3Iicu59dgS0BJ9/wzzVuKCvMQ724PMtMHtAq4I\nSVY/iymkZvv2W+7TcSQfiJ4ZyL959id/Dn5nIcJLnbkI4udWiAE5mcRfAoGAcaEl\n8xBDsa1s/M8GIbw53DFsfgpfaCDzomWaLpGJupHPReq3BmSmtXFVZq1YR6HIJnRc\nkXke6SeEqhTvjl1DnUIHxnFLm8KVMRqVQZR6XR+LYZv05sVelK+silC2HoqVGAkh\n/ivECXh3cmHMmtagB/IQP1AVqPD7ZIc5YUfS34ECgYB0pT6N5TbPDKHfftsZNgI0\nHHQN07jruHQ5naDR5L7F2n4rSVJH7dcwedHZaQxR+F1fYdKEWstqR73WPW4chluR\nyNE53+Xlt+Yt3cRhTKNBtCV7EMiA0S/yIt0Ai20o5MOc3P1xys1AopxFKFE1xBNm\nvQV+INvYA9APPlVNSKshbQ==\n-----END PRIVATE KEY-----\n',
    'client_email': 'aiwar-841@gen-lang-client-0042204106.iam.gserviceaccount.com',
    'token_uri': 'https://oauth2.googleapis.com/token',
}

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
creds = service_account.Credentials.from_service_account_info(creds_info, scopes=SCOPES)
gsc_service = build('searchconsole', 'v1', credentials=creds)

site_url = 'https://rwcclinic.com/'

end_date = (datetime.date.today() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
start_date = (datetime.date.today() - datetime.timedelta(days=92)).strftime('%Y-%m-%d')

print(f"Querying GSC from {start_date} to {end_date} (90 Days) specifically for FILLER keywords...")

request = {
    'startDate': start_date,
    'endDate': end_date,
    'dimensions': ['query', 'page'],
    'rowLimit': 10000
}

response = gsc_service.searchanalytics().query(siteUrl=site_url, body=request).execute()
rows = response.get('rows', [])

nongsaw_fillers = []
chongkhlot_fillers = []

for r in rows:
    query = r['keys'][0]
    page = r['keys'][1]
    clicks = r['clicks']
    imp = r['impressions']
    ctr = r['ctr']
    pos = r['position']
    
    # Filter keywords containing 'ฟิลเลอร์' AND ('น้องสาว' or 'ช่องคลอด')
    if 'ฟิลเลอร์' in query or 'filler' in query.lower():
        if 'น้องสาว' in query:
            nongsaw_fillers.append({'query': query, 'page': page, 'clicks': clicks, 'imp': imp, 'ctr': ctr, 'pos': pos})
        elif 'ช่องคลอด' in query:
            chongkhlot_fillers.append({'query': query, 'page': page, 'clicks': clicks, 'imp': imp, 'ctr': ctr, 'pos': pos})

# Aggregate Group 1: ฟิลเลอร์น้องสาว
total_clicks_ns = sum(item['clicks'] for item in nongsaw_fillers)
total_imp_ns = sum(item['imp'] for item in nongsaw_fillers)
avg_pos_ns = sum(item['pos'] * item['imp'] for item in nongsaw_fillers) / total_imp_ns if total_imp_ns > 0 else 0

# Aggregate Group 2: ฟิลเลอร์ช่องคลอด
total_clicks_ck = sum(item['clicks'] for item in chongkhlot_fillers)
total_imp_ck = sum(item['imp'] for item in chongkhlot_fillers)
avg_pos_ck = sum(item['pos'] * item['imp'] for item in chongkhlot_fillers) / total_imp_ck if total_imp_ck > 0 else 0

print("\n================== FILLER KEYWORDS SUMMARY ==================")
print(f"{'Category':<20} | {'Total Clicks':<12} | {'Total Impressions':<18} | {'Weighted Avg Position':<20}")
print("-" * 75)
print(f"{'ฟิลเลอร์น้องสาว':<20} | {total_clicks_ns:<12} | {total_imp_ns:<18} | {avg_pos_ns:<20.1f}")
print(f"{'ฟิลเลอร์ช่องคลอด':<20} | {total_clicks_ck:<12} | {total_imp_ck:<18} | {avg_pos_ck:<20.1f}")

# Print individual keywords
print("\n--- Top Keywords for 'ฟิลเลอร์น้องสาว' group ---")
nongsaw_fillers.sort(key=lambda x: x['clicks'], reverse=True)
for idx, item in enumerate(nongsaw_fillers[:10]):
    print(f"  {idx+1}. {item['query']:<35} | Clicks: {item['clicks']:<3} | Imp: {item['imp']:<5} | Pos: {item['pos']:.1f}")

print("\n--- Top Keywords for 'ฟิลเลอร์ช่องคลอด' group ---")
chongkhlot_fillers.sort(key=lambda x: x['clicks'], reverse=True)
for idx, item in enumerate(chongkhlot_fillers[:10]):
    print(f"  {idx+1}. {item['query']:<35} | Clicks: {item['clicks']:<3} | Imp: {item['imp']:<5} | Pos: {item['pos']:.1f}")
