import cv2
from ultralytics import YOLO
from config.settings import settings
from src.camera import CameraManager

class BikeDetector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = YOLO(settings.model_path)
            cls._instance.camera = CameraManager()
        return cls._instance

    def detect(self):
        frame = self.camera.get_frame()
        if frame is None:
            return {"detected": False, "confidence": 0.0, "error": "no_frame"}

        results = self.model(frame, verbose=False, conf=settings.threshold)
        
        for r in results:
            for box in r.boxes:
                if int(box.cls) == 1:
                    conf = float(box.conf)
                    if conf >= settings.threshold:
                        return {
                            "detected": True,
                            "confidence": round(conf, 3),
                            # "timestamp": ...
                        }
        
        return {"detected": False, "confidence": 0.0}