from datetime import datetime
from app import db


class Note(db.Model):
    __tablename__ = 'notes'
    
    # Поля таблицы
    id = db.Column(db.Integer, primary_key=True)  # Уникальный номер
    title = db.Column(db.String(200), nullable=False, index=True)  # Заголовок
    content = db.Column(db.Text, nullable=False)  # Текст заметки
    category = db.Column(db.String(100), nullable=False, index=True)  # Категория
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)  # Дата создания
    
    def __repr__(self):
        # Как отображается объект при печати
        return f'<Note {self.id}: {self.title}>'
    
    def to_dict(self):
        # Преобразование в словарь для удобной работы
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'created_at': self.created_at.strftime('%d.%m.%Y %H:%M')
        }
