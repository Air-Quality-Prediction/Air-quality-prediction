import pandas as pd
import numpy as np
import os
import joblib
import json
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def engineer_features(df):
    df = df.sort_values(by=['station_name', 'date']).reset_index(drop=True)
    
    # Fill NA using forward fill then backward fill per station
    df['aqi_filled'] = df.groupby('station_name')['aqi'].transform(lambda x: x.ffill().bfill())
    
    # Lags
    df['aqi_lag1'] = df.groupby('station_name')['aqi_filled'].shift(1)
    df['aqi_lag3'] = df.groupby('station_name')['aqi_filled'].shift(3)
    df['aqi_lag7'] = df.groupby('station_name')['aqi_filled'].shift(7)
    
    # Rolling stats
    df['aqi_roll_mean7'] = df.groupby('station_name')['aqi_filled'].transform(lambda x: x.rolling(7, min_periods=1).mean())
    
    # Time features
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['dayofweek'] = df['date'].dt.dayofweek
    df['dayofyear'] = df['date'].dt.dayofyear
    
    # Drop rows with NaN from lags
    df = df.dropna(subset=['aqi_lag7']).reset_index(drop=True)
    return df

def train_model():
    input_file = 'data/processed/nepaair_nepal_air_quality.csv'
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    df = engineer_features(df)
    
    features = ['aqi_lag1', 'aqi_lag3', 'aqi_lag7', 'aqi_roll_mean7', 'month', 'dayofweek', 'dayofyear', 'temperature', 'humidity']
    target = 'aqi_filled'
    
    # Fill remaining NaNs in features
    df[features] = df[features].fillna(method='ffill').fillna(method='bfill')
    
    # Chronological Split
    split_date = df['date'].max() - pd.Timedelta(days=180) # Last 6 months for testing
    
    train_df = df[df['date'] < split_date]
    test_df = df[df['date'] >= split_date]
    
    X_train = train_df[features]
    y_train = train_df[target]
    
    X_test = test_df[features]
    y_test = test_df[target]
    
    print(f"Training Random Forest on {len(X_train)} samples...")
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    print("Evaluating...")
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"Metrics -> MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.2f}")
    
    # Save Model
    os.makedirs('models/metadata', exist_ok=True)
    model_path = 'models/rf_aqi_model_v1.joblib'
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    # Save Metadata
    metadata = {
        "model_version": "v1.0",
        "algorithm": "RandomForestRegressor",
        "dataset_version": "NepaAir Mock 1.0",
        "training_date": pd.Timestamp.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
        "features": features,
        "metrics": {
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "R2": round(r2, 2)
        },
        "training_period": f"{train_df['date'].min().strftime('%Y-%m-%d')} to {train_df['date'].max().strftime('%Y-%m-%d')}",
        "validation_period": f"{test_df['date'].min().strftime('%Y-%m-%d')} to {test_df['date'].max().strftime('%Y-%m-%d')}"
    }
    
    with open('models/metadata/rf_aqi_model_v1.json', 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print("Training complete.")

if __name__ == "__main__":
    train_model()
