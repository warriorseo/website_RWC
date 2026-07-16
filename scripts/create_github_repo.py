import json
import urllib.request
import urllib.error

import os

token = os.environ.get("GITHUB_TOKEN", "")
repo_name = "website_RWC"

# Create repo payload
data = json.dumps({
    "name": repo_name,
    "description": "Website backup for RWC Clinic",
    "private": False
}).encode('utf-8')

# Call github API to create user repo
url = "https://api.github.com/user/repos"
req = urllib.request.Request(url, data=data, method="POST")
req.add_header("Authorization", f"token {token}")
req.add_header("Accept", "application/vnd.github.v3+json")
req.add_header("Content-Type", "application/json")
req.add_header("User-Agent", "urllib-python")

try:
    with urllib.request.urlopen(req) as response:
        res_data = response.read().decode('utf-8')
        res_json = json.loads(res_data)
        print(f"Repository {repo_name} created successfully!")
        print(f"Clone URL: {res_json['clone_url']}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
