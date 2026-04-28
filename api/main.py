from fastapi import FastAPI
import joblib

preprocessor = joblib.load('../models/preprocessor.joblib')
models = joblib.load('../models/models.joblib')

print('API is running')

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'API is running'}

