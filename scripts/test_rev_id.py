import requests
from requests.auth import HTTPBasicAuth
WP_USER = 'seo@warrior.in.th'
WP_PASS = 'tl50 hSv5 56Mq 2iEQ qTMu X8Jy'
WP_BASE = 'https://rwcclinic.com/wp-json/wp/v2'
auth = HTTPBasicAuth(WP_USER, WP_PASS)
post_id = 47343
revs = []
try:
    r = requests.get(f'{WP_BASE}/pages/{post_id}/revisions?per_page=10', auth=auth, timeout=30)
    revs = r.json()
except Exception as e: print(e)
if 'code' in revs and revs['code'] == 'rest_no_route':
    try:
        r = requests.get(f'{WP_BASE}/posts/{post_id}/revisions?per_page=10', auth=auth, timeout=30)
        revs = r.json()
    except Exception as e: print(e)

if isinstance(revs, list):
    print(f'Found {len(revs)} revisions on first page')
    for r in revs:
        print(f'{r["id"]}: {r["date"]}')
else:
    print('Error:', revs)
