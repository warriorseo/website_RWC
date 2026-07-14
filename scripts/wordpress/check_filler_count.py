import requests
import json

def main():
    cat_id = 112
    urls = []
    page = 1
    
    while True:
        res = requests.get(f"https://rwcclinic.com/wp-json/wp/v2/posts?categories={cat_id}&per_page=100&page={page}")
        if res.status_code != 200:
            break
            
        posts = res.json()
        if not posts:
            break
            
        for p in posts:
            urls.append(p['link'])
            
        page += 1
        
    print(f"Total posts found in category 112: {len(urls)}")
    
if __name__ == "__main__":
    main()
