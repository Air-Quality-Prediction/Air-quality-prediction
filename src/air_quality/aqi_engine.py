import math

def calculate_sub_aqi_pm25(pm25):
    if pd.isna(pm25) or pm25 < 0: return None
    if pm25 <= 12.0: return (50 - 0) / (12.0 - 0) * (pm25 - 0) + 0
    elif pm25 <= 35.4: return (100 - 51) / (35.4 - 12.1) * (pm25 - 12.1) + 51
    elif pm25 <= 55.4: return (150 - 101) / (55.4 - 35.5) * (pm25 - 35.5) + 101
    elif pm25 <= 150.4: return (200 - 151) / (150.4 - 55.5) * (pm25 - 55.5) + 151
    elif pm25 <= 250.4: return (300 - 201) / (250.4 - 150.5) * (pm25 - 150.5) + 201
    elif pm25 <= 350.4: return (400 - 301) / (350.4 - 250.5) * (pm25 - 250.5) + 301
    elif pm25 <= 500.4: return (500 - 401) / (500.4 - 350.5) * (pm25 - 350.5) + 401
    else: return 500

def calculate_sub_aqi_pm10(pm10):
    if pd.isna(pm10) or pm10 < 0: return None
    if pm10 <= 54: return (50 - 0) / (54 - 0) * (pm10 - 0) + 0
    elif pm10 <= 154: return (100 - 51) / (154 - 55) * (pm10 - 55) + 51
    elif pm10 <= 254: return (150 - 101) / (254 - 155) * (pm10 - 155) + 101
    elif pm10 <= 354: return (200 - 151) / (354 - 255) * (pm10 - 255) + 151
    elif pm10 <= 424: return (300 - 201) / (424 - 355) * (pm10 - 355) + 201
    elif pm10 <= 504: return (400 - 301) / (504 - 425) * (pm10 - 425) + 301
    elif pm10 <= 604: return (500 - 401) / (604 - 505) * (pm10 - 505) + 401
    else: return 500

def get_aqi_category(aqi):
    if pd.isna(aqi): return "Unknown"
    if aqi <= 50: return "Good"
    elif aqi <= 100: return "Moderate"
    elif aqi <= 150: return "Unhealthy for Sensitive Groups"
    elif aqi <= 200: return "Unhealthy"
    elif aqi <= 300: return "Very Unhealthy"
    else: return "Hazardous"

import pandas as pd
def calculate_aqi(row):
    aqi_pm25 = calculate_sub_aqi_pm25(row.get('pm25'))
    aqi_pm10 = calculate_sub_aqi_pm10(row.get('pm10'))
    
    aqis = {'PM2.5': aqi_pm25, 'PM10': aqi_pm10}
    valid_aqis = {k: v for k, v in aqis.items() if v is not None}
    
    if not valid_aqis:
        return pd.Series({'aqi': None, 'dominant_pollutant': None, 'aqi_category': "Unknown"})
    
    dominant_pollutant = max(valid_aqis, key=valid_aqis.get)
    max_aqi = round(valid_aqis[dominant_pollutant])
    
    return pd.Series({
        'aqi': max_aqi,
        'dominant_pollutant': dominant_pollutant,
        'aqi_category': get_aqi_category(max_aqi)
    })
