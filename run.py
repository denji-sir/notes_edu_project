# Точка входа в приложение
from app import create_app

# Создаем приложение
app = create_app()

# Запускаем сервер
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
