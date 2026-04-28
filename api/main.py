from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from datetime import date

from dataPreprocessing import clean_record

preprocessor = joblib.load('../models/preprocessor.joblib')
models = joblib.load('../models/isolation_forest_models.joblib')

print('API is running')

app = FastAPI()

class MaintenanceRecord(BaseModel):
    truck_id: str
    maintenance_date: date        # Pydantic parses "2024-01-21" string → date object automatically
    service_information: str      # raw value e.g. "Emergency Tires"
    maintenance_type: str
    odometer_reading: float
    labor_hours: float
    labor_cost: float
    parts_cost: float
    total_cost: float
    facility_location: str
    downtime_hours: float
    days_since_last: float        # NestJS calculates this before sending

@app.get('/')
def root():
    models_info = ""
    if preprocessor and models:
        models_info = 'Preprocessor and models loaded successfully'
    return {'message': 'API is running', 'models_info': models_info}

@app.post("/predict")
def predict(record: MaintenanceRecord):
    mtype = record.maintenance_type

    if mtype not in models:
        return {"error": f"Unknown maintenance_type: {mtype}"}

    input_df = clean_record(record)
    X = preprocessor.transform(input_df)

    score = float(models[mtype].decision_function(X)[0])
    pred = int(models[mtype].predict(X)[0])

    return {
        "is_anomaly": pred == -1,
        "anomaly_score": score
    }