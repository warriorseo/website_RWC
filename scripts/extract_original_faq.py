import subprocess
import re

result = subprocess.run(['git', 'show', 'HEAD:web/hip_filler_injection.html'], capture_output=True)
try:
    html = result.stdout.decode('utf-8')
except:
    html = result.stdout.decode('utf-16', errors='ignore')

matches = re.finditer(r'<div class="accordion-inner".*?>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
for m in matches:
    print('---')
    print(m.group(1).strip())
