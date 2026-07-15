import csv

CSV_FILE = r"d:\AI-Cyborg-2558\_SEO_Clients\RWC\sheet_data.csv"

service_filler_pages = []

with open(CSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        if len(row) > 1:
            url = row[0]
            page_type = row[1]
            
            # Check if Type is Service and url contains 'filler'
            if page_type == 'Service' and 'filler' in url.lower():
                service_filler_pages.append(url)

print(f"Found {len(service_filler_pages)} Service pages related to filler:")
for p in service_filler_pages:
    print(p)
