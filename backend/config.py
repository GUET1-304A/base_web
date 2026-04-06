import os
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))


def _get_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ('1', 'true', 'yes', 'on')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xingyu-studio-secret-key-2026'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'xingyu_cms'
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'xingyu-jwt-secret-2026'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173').split(',')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 10 * 1024 * 1024)
    FEISHU_WEBHOOK_URL = (os.environ.get('FEISHU_WEBHOOK_URL') or '').strip()
    APPLICATION_RATE_LIMIT_MINUTES = int(os.environ.get('APPLICATION_RATE_LIMIT_MINUTES') or 10)
    DEFAULT_GITHUB_URL = os.environ.get('DEFAULT_GITHUB_URL') or 'https://github.com/GUET1-304A'
    DEFAULT_APPLICATION_GITHUB_URL = os.environ.get('DEFAULT_APPLICATION_GITHUB_URL') or 'https://github.com'
    APP_HOST = os.environ.get('APP_HOST') or '0.0.0.0'
    APP_PORT = int(os.environ.get('APP_PORT') or 5000)
    APP_DEBUG = _get_bool('APP_DEBUG', True)


class DevelopmentConfig(Config):
    DEBUG = Config.APP_DEBUG


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
