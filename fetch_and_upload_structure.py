import os
import requests
from bs4 import BeautifulSoup
from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

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
sheets_service = build('sheets', 'v4', credentials=creds)

SPREADSHEET_ID = '1Iz97U0hcmSnyoZVVEA1SxxI3JkImbm4BgAlC_PkWypQ'
GID = '1460403152'

spreadsheet = sheets_service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
sheet_name = None
for s in spreadsheet.get('sheets', []):
    if str(s['properties']['sheetId']) == GID:
        sheet_name = s['properties']['title']
        break

if not sheet_name:
    print(f"Sheet with GID {GID} not found!")
    exit(1)

urls = [
    "https://rwcclinic.com/breaking-down-fillers/",
    "https://rwcclinic.com/filler-cheek-groove/",
    "https://rwcclinic.com/filler-under-eyes/",
    "https://rwcclinic.com/nose-filler-injection/",
    "https://rwcclinic.com/vagina-filler/",
    "https://rwcclinic.com/chin-filler/",
    "https://rwcclinic.com/forehead-filler-injection/",
    "https://rwcclinic.com/lips-filler/",
    "https://rwcclinic.com/temple-filler/",
    "https://rwcclinic.com/filler-injection-expert/"
]

WP_USER = "seo@warrior.in.th"
WP_PASS = "tl50 hSv5 56Mq 2iEQ qTMu X8Jy"
WP_BASE = "https://rwcclinic.com/wp-json/wp/v2"

sheet_data = sheets_service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID, range=f"'{sheet_name}'!A1:Z"
).execute()
values = sheet_data.get('values', [])
start_col_index = len(values[0]) if values else 0

def get_col_letter(col_idx):
    letter = ''
    while col_idx >= 0:
        letter = chr(col_idx % 26 + 65) + letter
        col_idx = col_idx // 26 - 1
    return letter

all_update_data = []

for i, url in enumerate(urls):
    slug = url.strip('/').split('/')[-1]
    print(f"Processing {slug}...")
    
    resp = requests.get(f"{WP_BASE}/posts?slug={slug}", auth=(WP_USER, WP_PASS))
    data = resp.json()
    if not data:
        resp = requests.get(f"{WP_BASE}/pages?slug={slug}", auth=(WP_USER, WP_PASS))
        data = resp.json()
        
    if not data:
        print(f"Could not find post/page for {slug}")
        continue
        
    html_content = data[0]['content']['rendered']
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style tags just in case
    for tag in soup(['script', 'style', 'noscript', 'meta', 'link']):
        tag.decompose()
    
    structure = [url]
    for elem in soup.find_all(['h2', 'h3', 'p']):
        text = elem.get_text(strip=True)
        if not text:
            continue
        if len(text) > 80:
            text = text[:77] + '...'
            
        if elem.name == 'h2':
            structure.append(f"  🔹 [H2] {text}")
        elif elem.name == 'h3':
            structure.append(f"      🔸 [H3] {text}")
        elif elem.name == 'p':
            structure.append(f"            📄 [P] {text}")
            
    all_update_data.append(structure)
    time.sleep(1)

data_to_write = []
for i, col_data in enumerate(all_update_data):
    col_letter = get_col_letter(start_col_index + i)
    range_name = f"'{sheet_name}'!{col_letter}1:{col_letter}{len(col_data)}"
    values_col = [[item] for item in col_data]
    data_to_write.append({
        'range': range_name,
        'values': values_col
    })

if data_to_write:
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data_to_write
    }
    sheets_service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID, body=body
    ).execute()
    print("Update successful!")
