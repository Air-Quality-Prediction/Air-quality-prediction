import urllib.request
import json
import os

def search_github_for_csv():
    # Search for Nepal Air Quality csv in github
    url = "https://api.github.com/search/code?q=Nepal+Air+Quality+extension:csv"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"Found {data.get('total_count')} results")
            for item in data.get('items', [])[:5]:
                print(item['name'], item['repository']['full_name'], item['html_url'])
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    search_github_for_csv()
