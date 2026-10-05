import pandas as pd
import sys

def validate_dataset():
    filepath = 'data/processed/nepaair_nepal_air_quality.csv'
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        sys.exit(1)
        
    print(f"Validating {len(df)} records from {filepath}")
    
    # 1. Zero India / Nepal-only check
    non_nepal = df[df['country'] != 'Nepal']
    if len(non_nepal) > 0:
        print(f"FAIL: Found {len(non_nepal)} records where country is not Nepal.")
        sys.exit(1)
    
    # 2. Coordinates validation (Nepal bounds roughly: Lat 26.3 to 30.5, Lon 80.0 to 88.3)
    invalid_coords = df[(df['latitude'] < 26.0) | (df['latitude'] > 31.0) | 
                        (df['longitude'] < 80.0) | (df['longitude'] > 89.0)]
    if len(invalid_coords) > 0:
        print(f"FAIL: Found {len(invalid_coords)} records with invalid coordinates outside Nepal.")
        sys.exit(1)
        
    # 3. Duplicate checks
    duplicates = df[df.duplicated(subset=['date', 'station_name'])]
    if len(duplicates) > 0:
        print(f"FAIL: Found {len(duplicates)} duplicate records.")
        sys.exit(1)
        
    # 4. Check missing critical metadata
    if df['station_name'].isnull().sum() > 0:
        print("FAIL: Missing station_name")
        sys.exit(1)
        
    if df['date'].isnull().sum() > 0:
        print("FAIL: Missing date")
        sys.exit(1)

    print("Total rows:", len(df))
    print("Nepal rows:", len(df))
    print("Non-Nepal rows: 0")
    print("Invalid coordinates: 0")
    print("Missing station: 0")
    print("Missing timestamp: 0")
    print("Duplicates: 0")
    
    print("\nSUCCESS: Dataset passed all Nepal-only and quality validation checks.")
    
if __name__ == "__main__":
    validate_dataset()
