from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app import db
from app.models.note import Note

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    sort_by = request.args.get('sort', 'date_desc')
    
    if sort_by == 'date_asc':
        notes = Note.query.order_by(Note.created_at.asc()).all()
    elif sort_by == 'title_asc':
        notes = Note.query.order_by(Note.title.asc()).all()
    elif sort_by == 'title_desc':
        notes = Note.query.order_by(Note.title.desc()).all()
    elif sort_by == 'category':
        notes = Note.query.order_by(Note.category.asc(), Note.created_at.desc()).all()
    else:
        notes = Note.query.order_by(Note.created_at.desc()).all()
    
    categories = db.session.query(Note.category).distinct().order_by(Note.category).all()
    categories = [cat[0] for cat in categories]
    
    return render_template('index.html', notes=notes, categories=categories, current_sort=sort_by)


@bp.route('/note/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', '').strip()
        
        errors = []
        
        if not title:
            errors.append('Ошибка: заголовок не может быть пустым')
        elif len(title) > 200:
            errors.append('Ошибка: заголовок не может быть длиннее 200 символов')
            
        if not content:
            errors.append('Ошибка: текст заметки не может быть пустым')
            
        if not category:
            errors.append('Ошибка: категория не может быть пустой')
        elif len(category) > 100:
            errors.append('Ошибка: категория не может быть длиннее 100 символов')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('create_note.html', title=title, content=content, category=category)
        
        try:
            new_note = Note(title=title, content=content, category=category)
            db.session.add(new_note)
            db.session.commit()
            
            current_app.logger.info(f'Создана заметка ID: {new_note.id}, Заголовок: "{new_note.title}"')
            flash(f'Заметка успешно создана с ID: {new_note.id}', 'success')
            return redirect(url_for('main.index'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Ошибка при создании заметки: {str(e)}')
            flash(f'Ошибка при создании заметки: {str(e)}', 'error')
            return render_template('create_note.html', title=title, content=content, category=category)
    
    return render_template('create_note.html')


@bp.route('/note/<int:note_id>')
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('view_note.html', note=note)


@bp.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', '').strip()
        
        errors = []
        
        if not title:
            errors.append('Ошибка: заголовок не может быть пустым')
        elif len(title) > 200:
            errors.append('Ошибка: заголовок не может быть длиннее 200 символов')
            
        if not content:
            errors.append('Ошибка: текст заметки не может быть пустым')
            
        if not category:
            errors.append('Ошибка: категория не может быть пустой')
        elif len(category) > 100:
            errors.append('Ошибка: категория не может быть длиннее 100 символов')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('edit_note.html', note=note, title=title, content=content, category=category)
        
        try:
            note.title = title
            note.content = content
            note.category = category
            db.session.commit()
            
            current_app.logger.info(f'Обновлена заметка ID: {note.id}, Заголовок: "{note.title}"')
            flash(f'Заметка с ID {note.id} успешно обновлена', 'success')
            return redirect(url_for('main.view_note', note_id=note.id))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Ошибка при обновлении заметки ID {note.id}: {str(e)}')
            flash(f'Ошибка при обновлении заметки: {str(e)}', 'error')
            return render_template('edit_note.html', note=note, title=title, content=content, category=category)
    
    return render_template('edit_note.html', note=note)


@bp.route('/note/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    try:
        note_title = note.title
        db.session.delete(note)
        db.session.commit()
        
        current_app.logger.info(f'Удалена заметка ID: {note_id}, Заголовок: "{note_title}"')
        flash(f'Заметка с ID {note_id} успешно удалена', 'success')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Ошибка при удалении заметки ID {note_id}: {str(e)}')
        flash(f'Ошибка при удалении заметки: {str(e)}', 'error')
    
    return redirect(url_for('main.index'))


@bp.route('/category/<category_name>')
def category(category_name):
    notes = Note.query.filter_by(category=category_name).order_by(Note.created_at.desc()).all()
    all_categories = db.session.query(Note.category).distinct().order_by(Note.category).all()
    all_categories = [cat[0] for cat in all_categories]
    
    return render_template('category.html', notes=notes, category_name=category_name, all_categories=all_categories, count=len(notes))


@bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    
    if not query:
        flash('Ошибка: поисковая фраза не может быть пустой', 'error')
        return redirect(url_for('main.index'))
    
    all_notes = Note.query.order_by(Note.created_at.desc()).all()
    query_lower = query.lower()
    
    notes = [note for note in all_notes if query_lower in note.title.lower() or query_lower in note.content.lower()]
    
    return render_template('search_results.html', notes=notes, query=query, count=len(notes))


@bp.route('/categories')
def categories():
    categories_query = db.session.query(Note.category, db.func.count(Note.id).label('count')).group_by(Note.category).order_by(Note.category).all()
    categories_list = [{'name': cat[0], 'count': cat[1]} for cat in categories_query]
    
    return render_template('categories_list.html', categories=categories_list, total_categories=len(categories_list))
