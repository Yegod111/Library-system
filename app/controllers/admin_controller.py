from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.book_service import BookService
from app.forms import BookForm
from app.utils.form_utils import flash_form_errors
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='../../templates')

def admin_required(func):
    """Ensures the user is an admin"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session or 'user_type' not in session or session.get('user_type') != 'admin':
            flash('You do not have the necessary permissions to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')


@admin_bp.route('/books', methods=['GET'])
@admin_required
def list_books():
    books = BookService.get_all_books(dictionary=True)
    return render_template('admin/list_books.html', books=books)


@admin_bp.route('/books/add', methods=['GET', 'POST'])
@admin_required
def add_book():
    form = BookForm(request.form if request.method == 'POST' else None)
    if request.method == 'POST':
        if form.validate():
            return render_template('admin/confirm_add_book.html', form=form)
        else:
            flash_form_errors(form)
    return render_template('admin/add_book.html', form=form)


@admin_bp.route('/books/add/confirm', methods=['POST'])
@admin_required
def confirm_add_book():
    form = BookForm(request.form)
    if form.validate():
        message, category = BookService.add_book(form.data)
        flash(message, category)
        if category == 'success':
            return redirect(url_for('admin.list_books'))
    else:
        flash_form_errors(form)
    return redirect(url_for('admin.add_book'))


@admin_bp.route('/books/<int:book_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_book(book_id):
    book = BookService.get_book_by_id(book_id, dictionary=True)
    if not book:
        flash('Book does not exist!', 'danger')
        return redirect(url_for('admin.list_books'))

    form = BookForm(request.form if request.method == 'POST' else None)
    if request.method == 'POST':
        if form.validate():
            return render_template('admin/confirm_edit_book.html', form=form, book_id=book_id)
        else:
            flash_form_errors(form)
    return render_template('admin/edit_book.html', form=form, book=book)


@admin_bp.route('/books/<int:book_id>/edit/confirm', methods=['POST'])
@admin_required
def confirm_edit_book(book_id):
    form = BookForm(request.form)
    if form.validate():
        message, category = BookService.update_book(book_id, form.data)
        flash(message, category)
        if category == 'success':
            return redirect(url_for('admin.list_books'))
    else:
        flash_form_errors(form)
    return redirect(url_for('admin.edit_book', book_id=book_id))


@admin_bp.route('/books/<int:book_id>/delete', methods=['POST'])
@admin_required
def delete_book(book_id):
    book = BookService.get_book_by_id(book_id, dictionary=True)
    if not book:
        flash('Book does not exist!', 'danger')
        return redirect(url_for('admin.list_books'))

    return render_template('admin/confirm_delete_book.html', book=book)


@admin_bp.route('/books/<int:book_id>/delete/confirm', methods=['POST'])
@admin_required
def confirm_delete_book(book_id):
    message, category = BookService.delete_book(book_id)
    flash(message, category)
    return redirect(url_for('admin.list_books'))

