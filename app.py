#Build SatelliteCollisionAPI
from fastapi import FastAPI
import joblib

app = FastAPI()
model = joblib.load('Satellite_model.pkl')

@app.post('/predict')
def predict(data: dict):
    prediction = model.predict([list(data.values())])
    return {"prediction": prediction[0]}

#Monitor API health.
@app.get('/health')
def health():
    return {"status":"healthy"}