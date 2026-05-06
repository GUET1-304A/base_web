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

    # 数据库：默认使用 SQLite，设置 DATABASE_URL 可切换到 MySQL 等
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(BASE_DIR, 'xingyu_cms.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 阿里云 OSS（配置后图片自动上传到 OSS，未配置则使用本地存储）
    ALIYUN_ACCESS_KEY_ID = os.environ.get('ALIYUN_ACCESS_KEY_ID', '')
    ALIYUN_ACCESS_KEY_SECRET = os.environ.get('ALIYUN_ACCESS_KEY_SECRET', '')
    ALIYUN_OSS_ENDPOINT = os.environ.get('ALIYUN_OSS_ENDPOINT', '')
    ALIYUN_OSS_BUCKET_NAME = os.environ.get('ALIYUN_OSS_BUCKET_NAME', '')
    ALIYUN_OSS_CDN_URL = os.environ.get('ALIYUN_OSS_CDN_URL', '')
    
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'xingyu-jwt-secret-2026'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173').split(',')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 10 * 1024 * 1024)
    FEISHU_WEBHOOK_URL = (os.environ.get('FEISHU_WEBHOOK_URL') or '').strip()
    FEISHU_APP_ENABLED = _get_bool('FEISHU_APP_ENABLED', False)
    FEISHU_APP_ID = (os.environ.get('FEISHU_APP_ID') or '').strip()
    FEISHU_APP_SECRET = (os.environ.get('FEISHU_APP_SECRET') or '').strip()
    FEISHU_APP_CHAT_ID = (os.environ.get('FEISHU_APP_CHAT_ID') or '').strip()
    FEISHU_APP_VERIFICATION_TOKEN = (os.environ.get('FEISHU_APP_VERIFICATION_TOKEN') or '').strip()
    FEISHU_APP_ENCRYPT_KEY = (os.environ.get('FEISHU_APP_ENCRYPT_KEY') or '').strip()
    FEISHU_HTTP_TIMEOUT = float(os.environ.get('FEISHU_HTTP_TIMEOUT') or 8)
    FEISHU_HTTP_RETRIES = int(os.environ.get('FEISHU_HTTP_RETRIES') or 0)
    FEISHU_HTTP_RETRY_BACKOFF_SECONDS = float(os.environ.get('FEISHU_HTTP_RETRY_BACKOFF_SECONDS') or 0.6)
    APPLICATION_RATE_LIMIT_MINUTES = int(os.environ.get('APPLICATION_RATE_LIMIT_MINUTES') or 10)
    DEFAULT_GITHUB_URL = os.environ.get('DEFAULT_GITHUB_URL') or 'https://github.com/GUET1-304A'
    DEFAULT_APPLICATION_GITHUB_URL = os.environ.get('DEFAULT_APPLICATION_GITHUB_URL') or ''
    APPLICATION_ACTION_BASE_URL = (os.environ.get('APPLICATION_ACTION_BASE_URL') or '').rstrip('/')
    MAIL_ENABLED = _get_bool('MAIL_ENABLED', False)
    SMTP_HOST = (os.environ.get('SMTP_SERVER') or os.environ.get('SMTP_HOST') or '').strip()
    SMTP_PORT = int(os.environ.get('SMTP_PORT') or 587)
    SMTP_USERNAME = (os.environ.get('SMTP_USER') or os.environ.get('SMTP_USERNAME') or '').strip()
    SMTP_PASSWORD = (os.environ.get('SMTP_PASSWORD') or '').strip()
    SMTP_USE_TLS = _get_bool('SMTP_USE_TLS', True)
    SMTP_USE_SSL = _get_bool('SMTP_USE_SSL', False)
    MAIL_FROM_NAME = (os.environ.get('MAIL_FROM_NAME') or '星雨作坊').strip()
    MAIL_FROM_EMAIL = (os.environ.get('SMTP_FROM') or os.environ.get('MAIL_FROM_EMAIL') or SMTP_USERNAME).strip()
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
