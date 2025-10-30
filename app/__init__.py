from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import os
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()


def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app.config.from_object(config.get(config_name, config['default']))
    
    db.init_app(app)
    
    with app.app_context():
        from app.models import note
        db.create_all()
    
    from app.routes import main
    app.register_blueprint(main.bp)
    
    from flask import render_template
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(f'Внутренняя ошибка сервера: {error}')
        return render_template('errors/500.html'), 500
    
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
