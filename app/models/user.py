from app.utils.db import execute_and_fetchone, execute_and_commit, transactional
from app.utils.password_utils import hash_password

class UserModel:
    @staticmethod
    def get_by_id(user_id, **kwargs):
        """Gets user by id."""
        return execute_and_fetchone(
            'SELECT * FROM users WHERE user_id = %s',
            (user_id,),
            **kwargs
        )


    @staticmethod
    def get_by_username(username, **kwargs):
        """Gets user by username."""
        return execute_and_fetchone(
            'SELECT * FROM users WHERE username = %s',
            (username,),
            **kwargs
        )


    @staticmethod
    def get_by_username_and_type(username, user_type, **kwargs):
        """Gets user by username and user_type."""
        assert user_type in ['admin', 'user'], 'Undefined user type.'
        return execute_and_fetchone(
            'SELECT * FROM users WHERE username = %s AND user_type = %s',
            (username, user_type),
            **kwargs
        )


    @staticmethod
    @transactional
    def create_user(username, password, user_type):
        """Creates a user."""
        assert user_type in ['admin', 'user'], 'Undefined user type.'
        password_hash = hash_password(password)
        execute_and_commit(
            'INSERT INTO users (username, password_hash, user_type) VALUES (%s, %s, %s)',
            (username, password_hash, user_type),
        )


    @staticmethod
    @transactional
    def update_password(user_id, new_password):
        """Updates user's password."""
        new_password_hash = hash_password(new_password)
        execute_and_commit('UPDATE users SET password_hash = %s WHERE user_id = %s', (new_password_hash, user_id))