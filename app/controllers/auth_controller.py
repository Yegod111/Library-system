from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.forms import LoginForm, RegisterForm
from app.services.auth_service import AuthService
from app.utils.form_utils import flash_form_errors

auth_bp = Blueprint('auth', __name__, template_folder='../../templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form if request.method == 'POST' else None)
    if request.method == 'POST':
        if form.validate():
            message, category = AuthService.register_user(form.data)
            flash(message, category)
            return redirect(url_for('auth.login') if category == 'success' else url_for('auth.register'))
        else:
            flash_form_errors(form)
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form if request.method == 'POST' else None)
    if request.method == 'POST':
        if form.validate():
            user = AuthService.authenticate_user(form.data)
            if user:
                session['user_id'] = user['user_id']
                session['user_type'] = user['user_type']
                return redirect(url_for('admin.dashboard' if user['user_type'] == 'admin' else 'user.dashboard'))
            else:
                flash('Invalid username or password. Please try again.', 'danger')
        else:
            flash_form_errors(form)
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))