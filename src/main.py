from fastapi import FastAPI
from src.detector import BikeDetector
from config.settings import settings

app = FastAPI(title="Bike Detector API - Raspberry Pi 4")

detector = BikeDetector()

@app.get("/detect-bike")
def detect_bike():
    result = detector.detect()
    return result

@app.get("/health")
async def health():
    return {"status": "healthy", "threshold": settings.threshold}