import urllib.request
import json
import csv
import time
import os
from datetime import datetime, timedelta

def download_openaq_nepal():
    url = "https://api.openaq.org/v2/locations?country=NP&limit=1000"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    print("Fetching locations in Nepal...")
    with urllib.request.urlopen(req) as response:
        locations = json.loads(response.read().decode())['results']
    
    print(f"Found {len(locations)} locations.")
    
    output_dir = os.path.join("data", "raw", "openaq_nepal")
    os.makedirs(output_dir, exist_ok=True)
    
    all_data = []
    
    for loc in locations:
        loc_id = loc['id']
        name = loc['name'].replace('/', '_').replace('\\', '_')
        print(f"Processing {name} (ID: {loc_id})...")
        
        try:
            # Let's get the measurements
            date_from = (datetime.utcnow() - timedelta(days=90)).strftime('%Y-%m-%d')
            meas_url = f"https://api.openaq.org/v2/measurements?location_id={loc_id}&limit=10000&date_from={date_from}"
            meas_req = urllib.request.Request(meas_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(meas_req) as m_res:
                measurements = json.loads(m_res.read().decode())['results']
            
            if not measurements:
                continue
            
            filepath = os.path.join(output_dir, f"{loc_id}_{name}.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(measurements, f)
            time.sleep(1) # rate limiting
        except Exception as e:
            print(f"Error fetching data for {name}: {e}")

if __name__ == "__main__":
    download_openaq_nepal()
