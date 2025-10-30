from app import create_app, db
from app.models.note import Note
from datetime import datetime, timedelta
import random

demo_notes = [
    {
        'title': 'Список покупок',
        'content': 'Купить: молоко, хлеб, яйца, сыр, овощи, фрукты. Не забыть про корм для кота!',
        'category': 'Личное'
    },
    {
        'title': 'Идеи для проекта',
        'content': 'Добавить темную тему, экспорт в PDF, синхронизацию с облаком, поддержку Markdown.',
        'category': 'Работа'
    },
    {
        'title': 'Тренировка',
        'content': 'Понедельник: грудь и трицепс\nСреда: спина и бицепс\nПятница: ноги и плечи',
        'category': 'Спорт'
    },
    {
        'title': 'Книги к прочтению',
        'content': '1. "Чистый код" Роберт Мартин\n2. "Философия Java" Брюс Эккель\n3. "Алгоритмы. Построение и анализ"',
        'category': 'Образование'
    },
    {
        'title': 'План на неделю',
        'content': 'Понедельник: встреча с клиентом в 10:00\nВторник: презентация проекта\nСреда: код-ревью\nЧетверг: тестирование\nПятница: деплой',
        'category': 'Работа'
    },
    {
        'title': 'Рецепт пасты карбонара',
        'content': 'Ингредиенты: спагетти, бекон, яйца, пармезан, черный перец.\nВарить пасту 8-10 минут. Обжарить бекон. Смешать с яйцами и сыром.',
        'category': 'Рецепты'
    },
    {
        'title': 'Цели на год',
        'content': 'Выучить Python и Flask, создать 3 проекта для портфолио, начать фриланс, заниматься спортом 3 раза в неделю.',
        'category': 'Личное'
    },
    {
        'title': 'Командировка в Москву',
        'content': 'Даты: 15-20 ноября. Отель забронирован. Встреча с партнерами 16 числа в 14:00. Не забыть подготовить презентацию!',
        'category': 'Работа'
    },
    {
        'title': 'Фильмы к просмотру',
        'content': 'Интерстеллар, Начало, Матрица, Побег из Шоушенка, Зеленая миля, Бойцовский клуб',
        'category': 'Развлечения'
    },
    {
        'title': 'Заметки с конференции',
        'content': 'Новые технологии: GraphQL, Docker, Kubernetes. Интересные доклады про микросервисы и CI/CD.',
        'category': 'Образование'
    },
    {
        'title': 'Подарки на Новый Год',
        'content': 'Маме - книга, Папе - инструменты, Брату - наушники, Сестре - косметика',
        'category': 'Личное'
    },
    {
        'title': 'Баги в проекте',
        'content': 'Bug #1: Не работает поиск по категориям\nBug #2: Ошибка при удалении заметки\nBug #3: Проблема с адаптивностью на мобильных',
        'category': 'Работа'
    }
]


def seed_database():
    app = create_app()
    
    with app.app_context():
        Note.query.delete()
        db.session.commit()
        
        print("Создание демо-заметок...")
        
        for i, note_data in enumerate(demo_notes):
            created_time = datetime.utcnow() - timedelta(hours=len(demo_notes)-i, minutes=random.randint(0, 59))
            
            note = Note(
                title=note_data['title'],
                content=note_data['content'],
                category=note_data['category']
            )
            note.created_at = created_time
            
            db.session.add(note)
            print(f"  ✓ Создана: {note.title}")
        
        db.session.commit()
        print(f"\n✅ Успешно создано {len(demo_notes)} демо-заметок!")
        print(f"📊 Категории: {len(set(n['category'] for n in demo_notes))}")


if __name__ == '__main__':
    seed_database()
