from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db import get_db

bp = Blueprint('task', __name__, url_prefix='/tasks')

@bp.route('/')
def index():
    db = get_db()
    tasklists = db.execute('SELECT * FROM tasklist').fetchall()
    return render_template('task/index.html', tasklists=tasklists)

@bp.route('/add_list', methods=('POST',))
def add_list():
    name = request.form['name']
    if not name:
        flash('O nome da lista é obrigatório.')
        return redirect(url_for('task.index'))

    db = get_db()
    db.execute('INSERT INTO tasklist (name) VALUES (?)', (name,))
    db.commit()
    flash(f'Lista "{name}" criada com sucesso.')
    return redirect(url_for('task.index'))

@bp.route('/<int:list_id>')
def show_list(list_id):
    db = get_db()
    tasklist = db.execute('SELECT * FROM tasklist WHERE id = ?', (list_id,)).fetchone()
    if tasklist is None:
        flash('Lista não encontrada.')
        return redirect(url_for('task.index'))

    tasks = db.execute('SELECT * FROM task WHERE tasklist_id = ?', (list_id,)).fetchall()
    return render_template('task/list.html', tasklist=tasklist, tasks=tasks)

@bp.route('/<int:list_id>/add_task', methods=('POST',))
def add_task(list_id):
    description = request.form['description']
    if not description:
        flash('A descrição da tarefa é obrigatória.')
        return redirect(url_for('task.show_list', list_id=list_id))

    db = get_db()
    db.execute(
        'INSERT INTO task (description, tasklist_id) VALUES (?, ?)',
        (description, list_id)
    )
    db.commit()
    flash('Tarefa adicionada com sucesso.')
    return redirect(url_for('task.show_list', list_id=list_id))

@bp.route('/<int:list_id>/done/<int:task_id>', methods=('POST',))
def mark_done(list_id, task_id):
    db = get_db()
    db.execute('UPDATE task SET done = 1 WHERE id = ?', (task_id,))
    db.commit()
    flash('Tarefa marcada como feita.')
    return redirect(url_for('task.show_list', list_id=list_id))

@bp.route('/<int:list_id>/delete', methods=('POST',))
def delete_list(list_id):
    db = get_db()
    tasklist = db.execute('SELECT * FROM tasklist WHERE id = ?', (list_id,)).fetchone()
    if tasklist is None:
        flash('Lista não encontrada.')
        return redirect(url_for('task.index'))

    db.execute('DELETE FROM tasklist WHERE id = ?', (list_id,))
    db.commit()
    flash(f'Lista "{tasklist["name"]}" excluída com sucesso.')
    return redirect(url_for('task.index'))
