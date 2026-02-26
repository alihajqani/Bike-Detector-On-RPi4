from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    threshold: float = 0.45
    model_path: str = "/app/models/yolo26n.pt"
    camera_index: int = 0
    resolution: tuple = (640, 480)
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()