import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import difflib
from google.oauth2 import service_account
from googleapiclient.discovery import build

WP_USER = 'seo@warrior.in.th'
WP_PASS = 'tl50 hSv5 56Mq 2iEQ qTMu X8Jy'
WP_BASE = 'https://rwcclinic.com/wp-json/wp/v2'
auth = HTTPBasicAuth(WP_USER, WP_PASS)

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

def get_revisions(slug):
    res = requests.get(f'{WP_BASE}/pages?slug={slug}', auth=auth)
    data = res.json()
    if not data:
        res = requests.get(f'{WP_BASE}/posts?slug={slug}', auth=auth)
        data = res.json()
    if not data: return []
    post_type = 'pages' if 'pages' in res.url else 'posts'
    post_id = data[0]['id']
    all_revs = []
    page = 1
    while True:
        rev_url = f'{WP_BASE}/{post_type}/{post_id}/revisions?per_page=100&page={page}'
        r = requests.get(rev_url, auth=auth)
        if r.status_code != 200: break
        revs = r.json()
        if not revs: break
        all_revs.extend(revs)
        page += 1
    return all_revs

# 1. Add header "WP Link" to R1 (R is index 17)
service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=f"'{SHEET_NAME}'!R1",
    valueInputOption="USER_ENTERED",
    body={'values': [["WP Link"]]}
).execute()

# 2. Add WP Link for Row 2 (nose-filler-injection)
# From previous fetch, we know IDs are 50209 (April 2024) and 52237 (May 2024)
r2_link = '=HYPERLINK("https://rwcclinic.com/wp-admin/revision.php?from=50209&to=52237", "Compare Revisions")'
service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=f"'{SHEET_NAME}'!R2",
    valueInputOption="USER_ENTERED",
    body={'values': [[r2_link]]}
).execute()

# 3. Analyze filler-injection-expert
revs_expert = get_revisions('filler-injection-expert')

# Group by month. Look for 2026 first, if none, 2025, if none 2024
april_revs = [r for r in revs_expert if r['date'].startswith('2026-04')]
may_revs = [r for r in revs_expert if r['date'].startswith('2026-05')]

if not april_revs and not may_revs:
    april_revs = [r for r in revs_expert if r['date'].startswith('2025-04')]
    may_revs = [r for r in revs_expert if r['date'].startswith('2025-05')]

if not april_revs and not may_revs:
    april_revs = [r for r in revs_expert if r['date'].startswith('2024-04')]
    may_revs = [r for r in revs_expert if r['date'].startswith('2024-05')]

# Find the latest in April and latest in May
before_rev = april_revs[0] if april_revs else None
after_rev = may_revs[0] if may_revs else None

if not before_rev:
    # Get last revision BEFORE May
    before_revs = [r for r in revs_expert if r['date'] < '2026-05-01']
    before_rev = before_revs[0] if before_revs else None

if not before_rev or not after_rev:
    print("No revisions found to compare for filler-injection-expert")
else:
    print(f"Comparing filler-injection-expert:")
    print(f"Before: {before_rev['date']} (ID: {before_rev['id']})")
    print(f"After : {after_rev['date']} (ID: {after_rev['id']})")
    
    r3_link = f'=HYPERLINK("https://rwcclinic.com/wp-admin/revision.php?from={before_rev["id"]}&to={after_rev["id"]}", "Compare Revisions")'
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"'{SHEET_NAME}'!R3",
        valueInputOption="USER_ENTERED",
        body={'values': [[r3_link]]}
    ).execute()
    
    from bs4 import BeautifulSoup
    def extract_text(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator='\\n')

    before_text = extract_text(before_rev['content']['rendered']).splitlines()
    after_text = extract_text(after_rev['content']['rendered']).splitlines()

    before_text = [line.strip() for line in before_text if line.strip()]
    after_text = [line.strip() for line in after_text if line.strip()]

    diff = difflib.ndiff(before_text, after_text)
    added = []
    removed = []
    for line in diff:
        if line.startswith('+ '): added.append(line[2:])
        elif line.startswith('- '): removed.append(line[2:])
    
    print("\\n--- REMOVED ---")
    for text in removed[:20]: print(text[:100])
    print("\\n--- ADDED ---")
    for text in added[:20]: print(text[:100])
