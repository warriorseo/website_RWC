import re

# Read working creds_info from compare_gsc_fillers_only.py
with open('d:/AI-Cyborg-2558/_SEO_Clients/RWC/scripts/compare_gsc_fillers_only.py', 'r', encoding='utf-8') as f:
    content_working = f.read()

match = re.search(r'creds_info = \{.*?\}', content_working, re.DOTALL)
if not match:
    print("Could not find creds_info in working file.")
    exit(1)
creds_info_str = match.group(0)

# Read inspect_under_eye_queries.py
with open('d:/AI-Cyborg-2558/_SEO_Clients/RWC/scripts/inspect_under_eye_queries.py', 'r', encoding='utf-8') as f:
    content_target = f.read()

# Replace creds_info in target file
content_new = re.sub(r'creds_info = \{.*?\}', creds_info_str, content_target, flags=re.DOTALL)

with open('d:/AI-Cyborg-2558/_SEO_Clients/RWC/scripts/inspect_under_eye_queries.py', 'w', encoding='utf-8') as f:
    f.write(content_new)

print("Successfully copied working credentials to inspect_under_eye_queries.py.")
