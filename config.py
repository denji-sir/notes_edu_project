import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

class Config:
    # Секретный ключ для защиты сессий
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    # Путь к базе данных SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'notes.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANG = 'ru'


# Настройки для разработки
class DevelopmentConfig(Config):
    DEBUG = True


# Настройки для тестирования
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # БД в памяти


# Настройки для продакшена
class ProductionConfig(Config):
    DEBUG = False


# Словарь всех конфигураций
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
