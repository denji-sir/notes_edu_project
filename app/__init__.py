from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import os
import logging
from logging.handlers import RotatingFileHandler

# Создаем объект базы данных
db = SQLAlchemy()


def create_app(config_name=None):
    # Создаем приложение Flask
    app = Flask(__name__)
    
    # Определяем окружение (разработка/тестирование/продакшен)
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Загружаем настройки
    app.config.from_object(config.get(config_name, config['default']))
    
    # Подключаем базу данных
    db.init_app(app)
    
    # Создаем таблицы в БД
    with app.app_context():
        from app.models import note
        db.create_all()
    
    # Подключаем маршруты
    from app.routes import main
    app.register_blueprint(main.bp)
    
    from flask import render_template
    
    # Обработка ошибки 404 (страница не найдена)
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    # Обработка ошибки 500 (ошибка сервера)
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(f'Внутренняя ошибка сервера: {error}')
        return render_template('errors/500.html'), 500
    
    # Настройка логирования (только для продакшена)
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Notes App startup')
    
    return app
