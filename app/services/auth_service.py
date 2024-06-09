from app.models.user import UserModel
from app.utils.password_utils import check_password

class AuthService:
    @staticmethod
    def register_user(form_data):
        """Register a user."""
        username = form_data.get('username')
        password = form_data.get('password')
        user_type = form_data.get('user_type')

        if UserModel.get_by_username(username):
            return 'Username already exists. Please choose a different username.', 'danger'

        UserModel.create_user(username, password, user_type)
        return 'Registration successful! Please log in.', 'success'


    @staticmethod
    def authenticate_user(form_data):
        """Authenticates a user."""
        username = form_data.get('username')
        password = form_data.get('password')
        user_type = form_data.get('user_type')

        user = UserModel.get_by_username_and_type(username, user_type, dictionary=True)
        if user and check_password(password, user['password_hash']):
            return user
        return None
    

    @staticmethod
    def change_password(form_data):
        """Change user's password."""
        user_id = form_data.get('user_id')
        current_password = form_data.get('current_password')
        new_password = form_data.get('new_password')
        try:
            user = UserModel.get_by_id(user_id, dictionary=True)
            if not user or not check_password(current_password, user.get('password_hash')):
                return 'Current password is incorrect.', 'danger'

            UserModel.update_password(user_id, new_password)
            return 'Password changed successfully!', 'success'
        except Exception as e:
            return f'Error changing password: {e}', 'danger'