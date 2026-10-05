import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
import os

def generate_mock_raw_data():
    np.random.seed(42)
    # 7 Provinces of Nepal and a major city in each
    locations = [
        {"city": "Biratnagar", "province": "Koshi", "station": "Biratnagar City AQMS", "lat": 26.452, "lon": 87.271},
        {"city": "Janakpur", "province": "Madhesh", "station": "Janakpur Hub AQMS", "lat": 26.728, "lon": 85.925},
        {"city": "Kathmandu", "province": "Bagmati", "station": "Ratnapark AQMS", "lat": 27.705, "lon": 85.315},
        {"city": "Pokhara", "province": "Gandaki", "station": "Pokhara University AQMS", "lat": 28.209, "lon": 83.985},
        {"city": "Butwal", "province": "Lumbini", "station": "Butwal Center AQMS", "lat": 27.698, "lon": 83.456},
        {"city": "Birendranagar", "province": "Karnali", "station": "Birendranagar AQMS", "lat": 28.599, "lon": 81.634},
        {"city": "Dhangadhi", "province": "Sudurpashchim", "station": "Dhangadhi City AQMS", "lat": 28.685, "lon": 80.590}
    ]

    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=5*365)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    all_data = []
    
    for loc in locations:
        # Base pollution levels
        if loc['city'] == "Kathmandu":
            base_pm25, base_pm10 = 55, 80
        elif loc['city'] in ["Biratnagar", "Janakpur", "Butwal"]:
            base_pm25, base_pm10 = 65, 90
        else:
            base_pm25, base_pm10 = 35, 55

        # Create seasonal variations (higher in winter/spring, lower in monsoon)
        day_of_year = dates.dayofyear
        seasonality = np.cos(2 * np.pi * (day_of_year - 15) / 365) * 0.5 + 1.0 # peaks around mid-Jan
        
        pm25 = np.maximum(5, np.random.normal(base_pm25, base_pm25*0.3, len(dates)) * seasonality)
        pm10 = np.maximum(10, np.random.normal(base_pm10, base_pm10*0.3, len(dates)) * seasonality)
        no2 = np.maximum(2, np.random.normal(base_pm25*0.4, 5, len(dates)) * seasonality)
        so2 = np.maximum(1, np.random.normal(base_pm25*0.1, 2, len(dates)))
        o3 = np.maximum(5, np.random.normal(30, 10, len(dates)))
        co = np.maximum(0.1, np.random.normal(0.8, 0.3, len(dates)) * seasonality)
        
        temp = np.random.normal(20, 7, len(dates)) - (seasonality * 5)
        humidity = np.clip(np.random.normal(60, 15, len(dates)) - (seasonality * 10), 10, 100)
        
        df = pd.DataFrame({
            'country': 'Nepal',
            'province': loc['province'],
            'city': loc['city'],
            'station_name': loc['station'],
            'latitude': loc['lat'],
            'longitude': loc['lon'],
            'date': dates,
            'pm25': pm25.round(2),
            'pm10': pm10.round(2),
            'no2': no2.round(2),
            'so2': so2.round(2),
            'o3': o3.round(2),
            'co': co.round(2),
            'temperature': temp.round(1),
            'humidity': humidity.round(1)
        })
        
        # Introduce some missing data
        mask = np.random.rand(len(df)) < 0.05
        for col in ['pm25', 'pm10', 'no2', 'so2', 'o3', 'co']:
            df.loc[mask, col] = np.nan
            mask = np.random.rand(len(df)) < 0.05
            
        all_data.append(df)
        
    final_df = pd.concat(all_data, ignore_index=True)
    os.makedirs('data/raw/doe_nepal', exist_ok=True)
    final_df.to_csv('data/raw/doe_nepal/mock_raw_data.csv', index=False)
    print(f"Generated mock raw data with {len(final_df)} rows at data/raw/doe_nepal/mock_raw_data.csv")

if __name__ == "__main__":
    generate_mock_raw_data()
