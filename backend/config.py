import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Google Sheets
    GOOGLE_CREDENTIALS_FILE = 'credentials.json'
    SPREADSHEET_NAME = 'Event Poster Data'
    
    # Email
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    
    # Upload
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/app.log'