from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    EXPRESS_API_URL: str
    
    class Config:
        env_file = ".env"
        
settings = Settings()