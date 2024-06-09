from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.book_service import BookService
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.forms import BorrowForm, SearchForm, ChangePasswordForm, ReturnForm, RenewForm
from app.utils.form_utils import flash_form_errors
from functools import wraps

user_bp = Blueprint('user', __name__, url_prefix='/user', template_folder='../../templates')

def user_required(func):
    """Ensures the user is logged in"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session or 'user_type' not in session or session.get('user_type') != 'user':
            flash('You need to be logged in to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper


@user_bp.route('/dashboard')
@user_required
def dashboard():
    return render_template('user/dashboard.html')


@user_bp.route('/books', methods=['GET', 'POST'])
@user_required
def search_books():
    form = SearchForm(request.form if request.method == 'POST' else None)
    books = []
    if request.method == 'POST':
        if form.validate():
            query = form.data.get('query')
            books = BookService.search_books(query, dictionary=True)
            if not books:
                flash('No books found matching your query.', 'info')
        else:
            flash_form_errors(form)
    recommended_books = BookService.get_all_books(dictionary=True)
    return render_template('user/search_books.html', form=form, books=books, recommended_books=recommended_books)


@user_bp.route('/books/<int:book_id>/details', methods=['GET'])
@user_required
def list_book_details(book_id):
    book = BookService.get_book_by_id(book_id, dictionary=True)
    if not book:
        flash('Book not found!', 'danger')
        return redirect(url_for('user.search_books'))
    return render_template('user/list_book_details.html', book=book)


@user_bp.route('/books/<int:book_id>/borrow', methods=['GET', 'POST'])
@user_required
def borrow_book(book_id):
    form = BorrowForm(request.form if request.method == 'POST' else None)
    if request.method == 'POST':
        if form.validate():
            message, category = UserService.borrow_book(book_id, session.get('user_id'))
            flash(message, category)
            if category == 'success':
                return redirect(url_for('user.dashboard'))
        else:
            flash_form_errors(form)
    return render_template('user/borrow_book.html', form=form, book_id=book_id)


@user_bp.route('/books/<int:book_id>/renew', methods=['GET', 'POST'])
@user_required
def renew_book(book_id):
    form = RenewForm(request.form if request.method == 'POST' else None)

    if request.method == 'POST':
        form.book_id.data = book_id
        if form.validate():
            message, category = UserService.renew_book(session.get('user_id'), book_id)
            flash(message, category)
            if category == 'success':
                return list_borrowed_books()
        else:
            flash_form_errors(form)

    return render_template('user/renew_book.html', form=form, book_id=book_id)


@user_bp.route('/books/<int:book_id>/return', methods=['GET', 'POST'])
@user_required
def return_book(book_id):
    form = ReturnForm(request.form if request.method == 'POST' else None)
    if request.method == 'POST':
        form.book_id.data = book_id
        if form.validate():
            message, category = UserService.return_book(book_id, session.get('user_id'))
            flash(message, category)
            if category == 'success':
                return list_borrowed_books()
        else:
            flash_form_errors(form)
    return render_template('user/return_book.html', form=form, book_id=book_id)


@user_bp.route('/borrowed_books', methods=['GET'])
@user_required
def list_borrowed_books():
    borrowed_books = UserService.get_borrowed_books_by_user(session.get('user_id'), dictionary=True)
    return render_template('user/borrowed_books.html', borrowed_books=borrowed_books)


@user_bp.route('/change_password', methods=['GET', 'POST'])
@user_required
def change_password():
    form = ChangePasswordForm(request.form if request.method == 'POST' else None)
    if request.method == 'POST':
        form.user_id.data = session.get('user_id')
        if form.validate():
            message, category = AuthService.change_password(form.data)
            flash(message, category)
            if category == 'success':
                return redirect(url_for('user.dashboard'))
        else:
            flash_form_errors(form)
    return render_template('user/change_password.html', form=form)