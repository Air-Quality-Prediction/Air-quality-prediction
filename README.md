# NepaAir - Nepal Air Quality Intelligence & Prediction Platform

NepaAir is a comprehensive air quality monitoring and prediction platform tailored specifically for Nepal. It provides historical data tracking, machine-learning-based forecasting, and actionable health guidance for major cities across Nepal.

## Core Features
- **Nepal-Only Data**: Fully restructured to use datasets conforming to Nepalese locations (Kathmandu, Pokhara, etc.).
- **US EPA AQI Methodology**: Accurate calculation of PM2.5 and PM10 AQI according to adopted Nepal standards.
- **Machine Learning Forecasting**: Predicts AQI for the next 72 hours using a custom RandomForestRegressor trained on Nepal historical data.
- **Modern UI/UX**: Glassmorphism design, dark-mode support, English/Nepali bilingual interface.
- **Automated Data Pipeline**: Scripts to regenerate the dataset from raw files.

## Installation
```bash
pip install -r requirements.txt
```

## Data Generation & Training Pipeline
Due to external API limitations, this repository includes a script to generate a highly realistic dataset proxy mirroring Department of Environment, Nepal structures.
```bash
python scripts/generate_mock_data.py
python scripts/build_dataset.py
python scripts/validate_nepal_data.py
python scripts/train_models.py
```

## Running the Application
```bash
python app.py
```
Visit `http://localhost:5000`

## Disclaimer
The historical data used in the public build is derived/synthesized for academic purposes due to immediate network restrictions on the DoEnv / OpenAQ APIs at the time of construction. The architecture, ML pipeline, and validation scripts are entirely production-ready for real telemetry insertion.

