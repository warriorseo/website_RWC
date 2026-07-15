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

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly', 'https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_info(creds_info, scopes=SCOPES)
gsc_service = build('searchconsole', 'v1', credentials=creds)
sheets_service = build('sheets', 'v4', credentials=creds)

SPREADSHEET_ID = '1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ'
SHEET_NAME = 'URL Revision and Engagement'

# 1. Fetch URLs from the Sheet
sheet_data = sheets_service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID, range=f"'{SHEET_NAME}'!A1:A50"
).execute()
values = sheet_data.get('values', [])
if not values:
    print("No data found in sheet.")
    exit()

urls = [row[0] for row in values if row and row[0].startswith('http')]

# 2. Get last 6 months list
today = datetime.date.today()
months_to_fetch = []
# Calculate last 6 months (e.g. if today is July 2026, we want Feb to July)
for i in range(5, -1, -1):
    d = today.replace(day=1) - datetime.timedelta(days=30*i)
    # properly compute the month
    month_val = today.month - i
    year_val = today.year
    while month_val <= 0:
        month_val += 12
        year_val -= 1
    months_to_fetch.append(f"{year_val}-{month_val:02d}")

print(f"Months to fetch: {months_to_fetch}")

# Date range for GSC
start_date = f"{months_to_fetch[0]}-01"
# End date is usually today - 2 days for GSC data
end_date = (today - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
print(f"Date range: {start_date} to {end_date}")

# 3. Query GSC and calculate average position per month
results_for_urls = {}
for url in urls:
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['date'],
        'dimensionFilterGroups': [{
            'filters': [{'dimension': 'page', 'expression': url, 'operator': 'equals'}]
        }]
    }
    response = gsc_service.searchanalytics().query(siteUrl='https://rwcclinic.com/', body=request).execute()
    rows = response.get('rows', [])
    
    # Aggregate by month
    month_data = {m: {'sum_pos_x_imp': 0, 'impressions': 0} for m in months_to_fetch}
    for row in rows:
        date_str = row['keys'][0] # YYYY-MM-DD
        ym = date_str[:7] # YYYY-MM
        if ym in month_data:
            imp = row['impressions']
            pos = row['position']
            month_data[ym]['impressions'] += imp
            month_data[ym]['sum_pos_x_imp'] += pos * imp
            
    # Calculate avg position per month
    avg_positions = []
    for m in months_to_fetch:
        d = month_data[m]
        if d['impressions'] > 0:
            avg_pos = d['sum_pos_x_imp'] / d['impressions']
            avg_positions.append(f"{avg_pos:.1f}")
        else:
            avg_positions.append("-")
            
    results_for_urls[url] = ", ".join(avg_positions)
    print(f"{url}: {results_for_urls[url]}")

# 4. Write to Column S
# We need to construct the column S data
# Column S is index 18 (0-indexed), meaning it's the 19th column.
# Let's write directly to S1:S...
# We will match the rows
update_data = []
# Row 0 is header
update_data.append(["Avg Position (Last 6M)"])
for i in range(1, len(values)):
    row = values[i]
    if row and row[0] in results_for_urls:
        update_data.append([results_for_urls[row[0]]])
    else:
        update_data.append([""])

body = {
    'values': update_data
}
result = sheets_service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=f"'{SHEET_NAME}'!S1:S{len(update_data)}",
    valueInputOption="USER_ENTERED",
    body=body
).execute()
print(f"Updated {result.get('updatedCells')} cells in Column S.")
