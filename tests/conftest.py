"""
Конфигурация pytest и фикстуры для тестирования
"""
import pytest
from app import create_app, db
from app.models.note import Note


@pytest.fixture
def app():
    """
    Фикстура Flask приложения для тестирования
    
    Создает приложение с тестовой конфигурацией
    """
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Тестовый клиент Flask
    
    Args:
        app: Фикстура приложения
        
    Returns:
        FlaskClient: Тестовый клиент для HTTP запросов
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    CLI runner для тестирования команд
    
    Args:
        app: Фикстура приложения
        
    Returns:
        FlaskCliRunner: Runner для CLI команд
    """
    return app.test_cli_runner()


@pytest.fixture
def sample_note(app):
    """
    Создает тестовую заметку в БД
    
    Args:
        app: Фикстура приложения
        
    Returns:
        Note: Созданная тестовая заметка
    """
    with app.app_context():
        note = Note(
            title='Тестовая заметка',
            content='Это содержимое тестовой заметки',
            category='Тест'
        )
        db.session.add(note)
        db.session.commit()
        
        # Обновляем объект после коммита
        db.session.refresh(note)
        note_id = note.id
        
        yield note
        
        # Очистка после теста
        note_to_delete = Note.query.get(note_id)
        if note_to_delete:
            db.session.delete(note_to_delete)
            db.session.commit()


@pytest.fixture
def multiple_notes(app):
    """
    Создает несколько тестовых заметок
    
    Args:
        app: Фикстура приложения
        
    Returns:
        list: Список созданных заметок
    """
    with app.app_context():
        notes = [
            Note(title='Заметка 1', content='Содержимое 1', category='Работа'),
            Note(title='Заметка 2', content='Содержимое 2', category='Личное'),
            Note(title='Заметка 3', content='Содержимое 3', category='Работа'),
        ]
        
        for note in notes:
            db.session.add(note)
        db.session.commit()
        
        # Обновляем объекты
        note_ids = [note.id for note in notes]
        
        yield notes
        
        # Очистка
        for note_id in note_ids:
            note_to_delete = Note.query.get(note_id)
            if note_to_delete:
                db.session.delete(note_to_delete)
        db.session.commit()
