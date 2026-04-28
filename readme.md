# HOW TO RUN

- open new terminal
- change directory

```[bash]
cd api
```

- activate your venv (I use conda)

```[bash]
conda activate your_venv_name
```

- activate uvicorn

```[bash]
uvicorn main:app --reload
```

# WORKFLOW?

- Receive the new record json (only 1 new data input)
- Convert json to df with pandas.
- Get the truck ID data and query the historical data of that ID from database (max 10 records maybe)
  (atau backend Nest query dulu history data dari database lalu kirim sekalian ke FastAPI, `sort_by=date`)

## FastAPI preprocess the data function

- split the service_description to service_detail and service_type
- checks if maintenance_type and servie_type the same (if not then mark it as anomaly)
- calculate the speedometer difference from new data and old data (if the new speedo is lower then mark it as anomaly)
- calculate days_since_last column (if the new date is lower than previous date then mark it as anomaly, else if no historical data set to 0)
- get `categorical_cols = ['maintenance_type', service_type', 'facility_location']`
- get `numerical_cols = [
'odometer_reading', 'labor_hours', 'labor_cost', 'parts_cost', 'total_cost', 'downtime_hours',  days_since_last']`
- return the df

## FastAPI predict function

- get the new record
- input_df = preprocessed_data(newRecord)
- get the maintenance type
- run preprocessor to newRecords
- predict
- score
- return
  - is_anomaly
  - anomaly_score
  - (optional?) all numerical_cols deviation (%) from data mean

## Re-training? (maybe next time)

# DATA FLOW

NestJS sends JSON
↓
FastAPI receives as Pydantic model
↓
Step 1: Manual cleaning (date parsing, string splitting) ← your custom code
↓
Step 2: preprocessor.transform() ← from .pkl
↓
Step 3: model.predict() ← from .pkl
↓
FastAPI returns JSON
