import pandas as pd
import json
import os
import sys

# Add src to python path to import aqi_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.air_quality.aqi_engine import calculate_aqi

def build_dataset():
    input_file = 'data/raw/doe_nepal/mock_raw_data.csv'
    output_file = 'data/processed/nepaair_nepal_air_quality.csv'
    manifest_file = 'data/metadata/dataset_manifest.json'
    
    print(f"Reading raw data from {input_file}...")
    df = pd.read_csv(input_file)
    
    print("Calculating AQI...")
    aqi_data = df.apply(calculate_aqi, axis=1)
    df = pd.concat([df, aqi_data], axis=1)
    
    # Metadata for provenance
    df['aqi_methodology'] = 'US EPA Standard (Nepal Adopted)'
    df['aqi_methodology_version'] = 'v1.0'
    df['source'] = 'Department of Environment, Nepal (Mocked Proxy)'
    df['data_quality_flag'] = df['aqi'].apply(lambda x: 'Valid' if pd.notna(x) else 'Missing AQI')
    
    print(f"Saving processed dataset to {output_file}...")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    
    # Create dataset manifest
    manifest = {
        "dataset_name": "NepaAir Nepal Air Quality Dataset",
        "country": "Nepal",
        "source_count": 1,
        "sources": ["Department of Environment, Nepal (Mocked Proxy)"],
        "download_dates": [pd.Timestamp.utcnow().strftime('%Y-%m-%d')],
        "coverage_start": df['date'].min(),
        "coverage_end": df['date'].max(),
        "stations": df['station_name'].unique().tolist(),
        "pollutants": ["PM2.5", "PM10", "NO2", "SO2", "O3", "CO"],
        "row_count": len(df),
        "license_notes": ["Generated for academic proxy purposes. Simulates Nepal DoEnv data structure."],
        "processing_version": "1.0"
    }
    
    os.makedirs(os.path.dirname(manifest_file), exist_ok=True)
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=4)
        
    print(f"Generated manifest at {manifest_file}")

if __name__ == "__main__":
    build_dataset()
