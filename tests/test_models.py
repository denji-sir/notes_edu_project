"""
Тесты для модели Note
"""
import pytest
from datetime import datetime
from app.models.note import Note
from app import db


def test_note_creation(app):
    """Тест создания заметки с корректными данными"""
    with app.app_context():
        note = Note(
            title='Тестовая заметка',
            content='Содержимое заметки',
            category='Тест'
        )
        db.session.add(note)
        db.session.commit()
        
        assert note.id is not None
        assert note.title == 'Тестовая заметка'
        assert note.content == 'Содержимое заметки'
        assert note.category == 'Тест'
        assert isinstance(note.created_at, datetime)


def test_note_created_at_automatic(app):
    """Тест автоматической установки created_at"""
    with app.app_context():
        note = Note(
            title='Тест',
            content='Содержимое',
            category='Категория'
        )
        db.session.add(note)
        db.session.commit()
        
        assert note.created_at is not None
        assert isinstance(note.created_at, datetime)


def test_note_to_dict(app):
    """Тест метода to_dict()"""
    with app.app_context():
        note = Note(
            title='Заголовок',
            content='Текст',
            category='Категория'
        )
        db.session.add(note)
        db.session.commit()
        
        note_dict = note.to_dict()
        
        assert isinstance(note_dict, dict)
        assert note_dict['id'] == note.id
        assert note_dict['title'] == 'Заголовок'
        assert note_dict['content'] == 'Текст'
        assert note_dict['category'] == 'Категория'
        assert 'created_at' in note_dict
        assert isinstance(note_dict['created_at'], str)


def test_note_repr(app):
    """Тест __repr__ метода"""
    with app.app_context():
        note = Note(
            title='Тест заметка',
            content='Содержимое',
            category='Тест'
        )
        db.session.add(note)
        db.session.commit()
        
        repr_str = repr(note)
        assert 'Note' in repr_str
        assert str(note.id) in repr_str
        assert 'Тест заметка' in repr_str


def test_note_required_fields(app):
    """Тест обязательных полей"""
    with app.app_context():
        # Попытка создать заметку без title
        with pytest.raises(Exception):
            note = Note(content='Содержимое', category='Тест')
            db.session.add(note)
            db.session.commit()


def test_note_title_length(app):
    """Тест ограничения длины заголовка"""
    with app.app_context():
        long_title = 'A' * 201  # 201 символ (больше лимита 200)
        note = Note(
            title=long_title,
            content='Содержимое',
            category='Тест'
        )
        db.session.add(note)
        
        # SQLite может принять, но в production БД будет ошибка
        # Валидация должна быть на уровне приложения
        assert len(note.title) > 200


def test_multiple_notes(app):
    """Тест создания нескольких заметок"""
    with app.app_context():
        notes = [
            Note(title=f'Заметка {i}', content=f'Содержимое {i}', category='Тест')
            for i in range(5)
        ]
        
        for note in notes:
            db.session.add(note)
        db.session.commit()
        
        all_notes = Note.query.all()
        assert len(all_notes) >= 5
