import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import difflib

WP_USER = 'seo@warrior.in.th'
WP_PASS = 'tl50 hSv5 56Mq 2iEQ qTMu X8Jy'
WP_BASE = 'https://rwcclinic.com/wp-json/wp/v2'
auth = HTTPBasicAuth(WP_USER, WP_PASS)

slug = 'hip-filler-injection'
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
    if r.status_code != 200: break
    revs = r.json()
    if not revs: break
    all_revs.extend(revs)
    page += 1

print(f"Total Revisions for {slug}: {len(all_revs)}")
for r in all_revs:
    print(r['date'])

may_revs = [r for r in all_revs if r['date'].startswith('2026-05')]
june_revs = [r for r in all_revs if r['date'].startswith('2026-06')]

if not may_revs and not june_revs:
    print("No revisions in May or June 2026")
    exit()

# We want to compare state at end of May vs state at end of June
# So before = latest in May (or earlier if no May), after = latest in June
before_rev = may_revs[0] if may_revs else None
after_rev = june_revs[0] if june_revs else None

if not before_rev:
    before_revs = [r for r in all_revs if r['date'] < '2026-05-01']
    before_rev = before_revs[0] if before_revs else None

if not before_rev or not after_rev:
    print("Cannot compare. Missing before or after revision.")
    exit()

print(f"Comparing hip-filler-injection:")
print(f"Before (May 2026): {before_rev['date']} (ID: {before_rev['id']})")
print(f"After (June 2026): {after_rev['date']} (ID: {after_rev['id']})")

def extract_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator='\n')

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

print("\n--- REMOVED (Deleted between May and June) ---")
for text in removed: print(text[:150])
print("\n--- ADDED (Inserted between May and June) ---")
for text in added: print(text[:150])
