from bs4 import BeautifulSoup

with open(r'd:\AI-Cyborg-2558\_SEO_Clients\RWC\web\hip_filler_injection.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Remove script, style, and noscript tags
for tag in soup(['script', 'style', 'noscript', 'meta', 'link']):
    tag.decompose()

text = soup.get_text(separator='\n', strip=True)

# Print the first 2000 characters and maybe some headings to understand the structure
print("Title:", soup.title.string if soup.title else "No Title")
headings = soup.find_all(['h1', 'h2', 'h3'])
print("\nHeadings:")
for h in headings:
    print(f"{h.name}: {h.get_text(strip=True)}")

print("\nContent Sample:")
print(text[:2000])
