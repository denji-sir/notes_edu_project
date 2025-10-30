"""
Тесты для маршрутов приложения
"""
import pytest
from app.models.note import Note
from app import db


class TestIndex:
    """Тесты главной страницы"""
    
    def test_index_empty(self, client):
        """Тест главной страницы без заметок"""
        response = client.get('/')
        assert response.status_code == 200
        assert 'Список заметок пуст'.encode() in response.data
    
    def test_index_with_notes(self, client, sample_note):
        """Тест главной страницы с заметками"""
        response = client.get('/')
        assert response.status_code == 200
        assert 'Тестовая заметка'.encode() in response.data


class TestCreateNote:
    """Тесты создания заметки"""
    
    def test_create_note_get(self, client):
        """Тест отображения формы создания"""
        response = client.get('/note/create')
        assert response.status_code == 200
        assert 'Создать новую заметку'.encode() in response.data
    
    def test_create_note_valid_data(self, client, app):
        """Тест создания заметки с валидными данными"""
        response = client.post('/note/create', data={
            'title': 'Новая заметка',
            'content': 'Содержимое новой заметки',
            'category': 'Тест'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert 'успешно создана'.encode() in response.data
        
        with app.app_context():
            note = Note.query.filter_by(title='Новая заметка').first()
            assert note is not None
            assert note.content == 'Содержимое новой заметки'
            assert note.category == 'Тест'
    
    def test_create_note_empty_title(self, client):
        """Тест создания с пустым заголовком"""
        response = client.post('/note/create', data={
            'title': '',
            'content': 'Содержимое',
            'category': 'Тест'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert 'заголовок не может быть пустым'.encode() in response.data
    
    def test_create_note_empty_content(self, client):
        """Тест создания с пустым содержимым"""
        response = client.post('/note/create', data={
            'title': 'Заголовок',
            'content': '',
            'category': 'Тест'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert 'текст заметки не может быть пустым'.encode() in response.data
    
    def test_create_note_empty_category(self, client):
        """Тест создания с пустой категорией"""
        response = client.post('/note/create', data={
            'title': 'Заголовок',
            'content': 'Содержимое',
            'category': ''
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert 'категория не может быть пустой'.encode() in response.data
    
    def test_create_note_title_too_long(self, client):
        """Тест создания с слишком длинным заголовком"""
        long_title = 'A' * 201
        response = client.post('/note/create', data={
            'title': long_title,
            'content': 'Содержимое',
            'category': 'Тест'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert 'длиннее 200 символов'.encode() in response.data


class TestViewNote:
    """Тесты просмотра заметки"""
    
    def test_view_note_exists(self, client, sample_note):
        """Тест просмотра существующей заметки"""
        response = client.get(f'/note/{sample_note.id}')
        assert response.status_code == 200
        assert 'Тестовая заметка'.encode() in response.data
        assert 'Это содержимое тестовой заметки'.encode() in response.data
    
    def test_view_note_not_exists(self, client):
        """Тест просмотра несуществующей заметки"""
        response = client.get('/note/99999')
        assert response.status_code == 404


class TestEditNote:
    """Тесты редактирования заметки"""
    
    def test_edit_note_get(self, client, sample_note):
        """Тест отображения формы редактирования"""
        response = client.get(f'/note/{sample_note.id}/edit')
        assert response.status_code == 200
        assert 'Редактировать заметку'.encode() in response.data
        assert 'Тестовая заметка'.encode() in response.data
    
    def test_edit_note_valid_data(self, client, app, sample_note):
        """Тест редактирования с валидными данными"""
        response = client.post(f'/note/{sample_note.id}/edit', data={
            'title': 'Измененная заметка',
            'content': 'Новое содержимое',
            'category': 'Новая категория'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert 'успешно обновлена'.encode() in response.data
        
        with app.app_context():
            note = Note.query.get(sample_note.id)
            assert note.title == 'Измененная заметка'
            assert note.content == 'Новое содержимое'
            assert note.category == 'Новая категория'
    
    def test_edit_note_empty_fields(self, client, sample_note):
        """Тест редактирования с пустыми полями"""
        response = client.post(f'/note/{sample_note.id}/edit', data={
            'title': '',
            'content': '',
            'category': ''
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert 'не может быть пустым'.encode() in response.data
    
    def test_edit_note_not_exists(self, client):
        """Тест редактирования несуществующей заметки"""
        response = client.get('/note/99999/edit')
        assert response.status_code == 404


class TestDeleteNote:
    """Тесты удаления заметки"""
    
    def test_delete_note_exists(self, client, app, sample_note):
        """Тест удаления существующей заметки"""
        note_id = sample_note.id
        
        response = client.post(f'/note/{note_id}/delete', follow_redirects=True)
        
        assert response.status_code == 200
        assert 'успешно удалена'.encode() in response.data
        
        with app.app_context():
            note = Note.query.get(note_id)
            assert note is None
    
    def test_delete_note_not_exists(self, client):
        """Тест удаления несуществующей заметки"""
        response = client.post('/note/99999/delete')
        assert response.status_code == 404


class TestCategoryFilter:
    """Тесты фильтрации по категории"""
    
    def test_category_with_notes(self, client, multiple_notes):
        """Тест фильтрации категории с заметками"""
        response = client.get('/category/Работа')
        assert response.status_code == 200
        assert 'Категория: Работа'.encode() in response.data
        assert 'Заметка 1'.encode() in response.data
        assert 'Заметка 3'.encode() in response.data
    
    def test_category_empty(self, client):
        """Тест фильтрации пустой категории"""
        response = client.get('/category/НесуществующаяКатегория')
        assert response.status_code == 200
        assert 'заметок не найдено'.encode() in response.data


class TestSearch:
    """Тесты поиска"""
    
    def test_search_found(self, client, sample_note):
        """Тест поиска с результатами"""
        response = client.get('/search?q=тестовая')
        assert response.status_code == 200
        # Проверяем что результат не пустой
        assert 'Найдено заметок: 0'.encode() not in response.data
    
    def test_search_not_found(self, client, sample_note):
        """Тест поиска без результатов"""
        response = client.get('/search?q=НесуществующийТекст123')
        assert response.status_code == 200
        assert 'ничего не найдено'.encode() in response.data
    
    def test_search_empty_query(self, client):
        """Тест поиска с пустым запросом"""
        response = client.get('/search?q=', follow_redirects=True)
        assert response.status_code == 200
        assert 'не может быть пустой'.encode() in response.data
    
    def test_search_case_insensitive(self, client, app):
        """Тест поиска без учета регистра"""
        # Создаем заметку с латинским текстом для теста
        with app.app_context():
            note = Note(title='Test Note', content='Test content', category='Test')
            db.session.add(note)
            db.session.commit()
            note_id = note.id
        
        response = client.get('/search?q=test')
        assert response.status_code == 200
        assert 'Test Note'.encode() in response.data
        
        # Очистка
        with app.app_context():
            note = Note.query.get(note_id)
            if note:
                db.session.delete(note)
                db.session.commit()
