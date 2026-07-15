import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import difflib

WP_USER = 'seo@warrior.in.th'
WP_PASS = 'tl50 hSv5 56Mq 2iEQ qTMu X8Jy'
WP_BASE = 'https://rwcclinic.com/wp-json/wp/v2'
auth = HTTPBasicAuth(WP_USER, WP_PASS)

slug = 'nose-filler-injection'
res = requests.get(f'{WP_BASE}/pages?slug={slug}', auth=auth)
data = res.json()
if not data:
    res = requests.get(f'{WP_BASE}/posts?slug={slug}', auth=auth)
    data = res.json()

if not data:
    print("Post not found.")
    exit()

post_type = 'pages' if 'pages' in res.url else 'posts'
post_id = data[0]['id']

all_revs = []
page = 1
while True:
    rev_url = f'{WP_BASE}/{post_type}/{post_id}/revisions?per_page=100&page={page}'
    r = requests.get(rev_url, auth=auth)
    if r.status_code != 200:
        break
    revs = r.json()
    if not revs:
        break
    all_revs.extend(revs)
    page += 1

april_revs = [r for r in all_revs if r['date'].startswith('2024-04')]
may_revs = [r for r in all_revs if r['date'].startswith('2024-05')]

# The API returns newest first. So april_revs[0] is the latest in April, may_revs[0] is the latest in May.
before_rev = april_revs[0] if april_revs else None
after_rev = may_revs[0] if may_revs else None

if not before_rev or not after_rev:
    print("Could not find revisions to compare for 2024.")
    exit()

print(f"\nComparing '{slug}'")
print(f"April 2024 Latest: {before_rev['date']} (ID: {before_rev['id']})")
print(f"May 2024 Latest  : {after_rev['date']} (ID: {after_rev['id']})")

def extract_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator='\n')

before_text = extract_text(before_rev['content']['rendered']).splitlines()
after_text = extract_text(after_rev['content']['rendered']).splitlines()

# Clean empty lines
before_text = [line.strip() for line in before_text if line.strip()]
after_text = [line.strip() for line in after_text if line.strip()]

diff = difflib.ndiff(before_text, after_text)
added = []
removed = []
for line in diff:
    if line.startswith('+ '):
        added.append(line[2:])
    elif line.startswith('- '):
        removed.append(line[2:])

print("\n--- REMOVED (Deleted between April and May) ---")
for text in removed:
    print(text[:150] + "...") # Truncate to save space but get the gist

print("\n--- ADDED (Inserted between April and May) ---")
for text in added:
    print(text[:150] + "...")
