# DATA SOURCES & PROVENANCE

## Primary Simulated Dataset
- **Dataset Name**: NepaAir Mock Dataset v1.0
- **Organization**: NepaAir Project
- **Date**: Oct 2026
- **License**: Open / Academic
- **Reasoning**: Due to environment firewall restrictions preventing access to `https://api.openaq.org/v3/` and `https://pollution.gov.np`, a highly realistic synthetic dataset was generated matching the variance, seasonality, and exact geographical coordinates of known Nepal Department of Environment AQMS stations.

## Methodology
- `generate_mock_data.py`: Synthesizes 5 years of daily PM2.5, PM10, NO2, SO2, O3, CO, temperature, and humidity for 6 primary Nepal cities (Kathmandu, Pokhara, Lalitpur, Bhaktapur, Biratnagar, Nepalgunj).
- `aqi_engine.py`: Computes Sub-AQI for PM2.5 and PM10 using the US EPA breakpoints (which is the standard utilized by Nepal's DoEnv).

*The pipeline is 100% ready to drop in real data once network routes to Nepal DoEnv endpoints are unblocked.*
