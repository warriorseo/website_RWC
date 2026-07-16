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

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_info(creds_info, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

SPREADSHEET_ID = '1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ'
SHEET_NAME = 'URL Revision and Engagement'

# Fetch existing data
result = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range=f"'{SHEET_NAME}'!A1:Z100"
).execute()
values = result.get('values', [])

if not values:
    print('No data found.')
    exit()

template = "https://analytics.google.com/analytics/web/?hl=en#/a149800124p292925407/reports/explorer?params=_u..nav%3Dmaui%26_r.explorerCard..filterTerm%3D%252F{slug}%252F%26_r.explorerCard..startRow%3D0%26_u..built_comparisons_enabled%3Dtrue%26_u..comparisons%3D%5B%7B%22savedComparisonId%22:%227523527606%22,%22name%22:%22Organic%20traffic%22,%22isEnabled%22:true,%22filters%22:%5B%7B%22fieldName%22:%22sessionDefaultChannelGrouping%22,%22evaluationType%22:8,%22expressionList%22:%5B%22Organic%20Search%22,%22Organic%20Video%22,%22Organic%20Social%22,%22Organic%20Shopping%22%5D,%22isCaseSensitive%22:true%7D%5D,%22systemDefinedSavedComparisonType%22:2,%22isSystemDefined%22:true%7D%5D%26_r.explorerCard..seldim%3D%5B%22unifiedPagePathScreen%22%5D%26_u.comparisonOption%3Ddisabled%26_r.explorerCard..dateGranularity%3DnthMonth%26_r.explorerCard..sortKey%3DuserEngagementDurationPerUser%26_r.explorerCard..selmet%3D%5B%22userEngagementDurationPerUser%22,%22screenPageViews%22%5D%26_u.dateStart%3D20250701%26_u.dateEnd%3D20260715%26_u.date00%3D20250701%26_u.date01%3D20260715&ruid=0d646679-6477-4cd0-a2cc-a3c33313c77f&collectionId=10576530072&r=15246722299"

# Update the GA4 Check Link column (last column)
rows = []
header_len = len(values[0])
for idx, row in enumerate(values):
    if idx == 0:
        rows.append(row)
        continue
    
    url = row[0]
    slug = url.replace('https://rwcclinic.com/', '').replace('/', '')
    
    ga4_link = template.replace('{slug}', slug)
    
    # Pad the row to match the header length to prevent overwriting wrong columns
    while len(row) < header_len:
        row.append('')
        
    # Replace the last element with HYPERLINK formula
    row[header_len - 1] = f'=HYPERLINK("{ga4_link}", "GA4 Data")'
    rows.append(row)

# Update sheet
body = {
    'values': rows
}
result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=f"'{SHEET_NAME}'!A1",
    valueInputOption="USER_ENTERED",
    body=body
).execute()
print(f"Updated {result.get('updatedCells')} cells with 12 months GA4 URL template.")
