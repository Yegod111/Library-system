from wtforms import Form, StringField, PasswordField, SelectField, DateField, IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange

class RegisterForm(Form):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'), 
        Length(min=3, max=20, message='Username must be between 3 and 20 characters long')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'), 
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'), 
        EqualTo('password', message='Passwords must match')
    ])
    user_type = SelectField('User Type', choices=[
        ('admin', 'Admin'), 
        ('user', 'User')
    ], validators=[DataRequired(message='Please select a user type')])
    submit = SubmitField('Sign Up')


class LoginForm(Form):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])
    user_type = SelectField('User Type', choices=[
        ('admin', 'Admin'), 
        ('user', 'User')
    ], validators=[DataRequired(message='Please select a user type')])
    submit = SubmitField('Login')


class BookForm(Form):
    title = StringField('Title', validators=[
        DataRequired(message='Title is required')
    ])
    author = StringField('Author', validators=[
        DataRequired(message='Author is required')
    ])
    isbn = StringField('ISBN', validators=[
        DataRequired(message='ISBN is required')
    ])
    publisher = StringField('Publisher')
    published_date = DateField('Published Date', format='%Y-%m-%d')
    copies_available = IntegerField('Copies Available', validators=[
        DataRequired(message='Number of copies available is required'), 
        NumberRange(min=0, message='Number of copies must be a non-negative integer')
    ])
    submit = SubmitField('Add Book')


class SearchForm(Form):
    query = StringField('Search', validators=[
        DataRequired(message='Search query is required')
    ])
    submit = SubmitField('Search')


class BorrowForm(Form):
    submit = SubmitField('Borrow')


class ReturnForm(Form):
    book_id = HiddenField('Book ID', validators=[
        DataRequired(message='Book ID is required')
    ])
    submit = SubmitField('Return Book')


class RenewForm(Form):
    book_id = HiddenField('Book ID', validators=[
        DataRequired(message='Book ID is required')
    ])
    submit = SubmitField('Renew Book')


class ChangePasswordForm(Form):
    user_id = HiddenField('User ID', validators=[
        DataRequired(message='User ID is required')
    ])
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message='Current password is required')
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired(message='New password is required'), 
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Please confirm your new password'), 
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')