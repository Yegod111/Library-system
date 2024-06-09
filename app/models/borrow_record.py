from app.utils.db import execute_and_fetchone, execute_and_fetchall, execute_and_commit, transactional

class BorrowRecordModel:
    @staticmethod
    def get_by_user_and_book(user_id, book_id, **kwargs):
        """Gets a borrow record by user_id and book_id."""
        return execute_and_fetchall(
            'SELECT * FROM borrow_records WHERE user_id = %s AND book_id = %s',
            (user_id, book_id),
            **kwargs
        )
    

    @staticmethod
    def get_validating_by_user_and_book(user_id, book_id, **kwargs):
        """Gets a borrow record by user_id and book_id."""
        return execute_and_fetchone(
            'SELECT * FROM borrow_records WHERE user_id = %s AND book_id = %s AND return_date IS NULL',
            (user_id, book_id),
            **kwargs
        )


    @staticmethod
    def get_all_by_user(user_id, **kwargs):
        """Gets all borrow records by user_id."""
        return execute_and_fetchall(
            'SELECT * FROM borrow_records WHERE user_id = %s',
            (user_id,),
            **kwargs
        )


    @staticmethod
    def get_all_validating_by_user(user_id, **kwargs):
        """Gets all validating borrow records by user_id."""
        return execute_and_fetchall(
            'SELECT * FROM borrow_records WHERE user_id = %s AND return_date IS NULL',
            (user_id,),
            **kwargs
        )


    @staticmethod
    @transactional
    def add(user_id, book_id, borrow_date, due_date):
        """Adds a new borrow record."""
        execute_and_commit(
            'INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date) VALUES (%s, %s, %s, %s)',
            (user_id, book_id, borrow_date, due_date)
        )


    @staticmethod
    @transactional
    def update(borrow_record_id, due_date=None, return_date=None):
        """Updates a borrow record."""
        query = 'UPDATE borrow_records SET '
        params = []
        if due_date:
            query += 'due_date = %s, '
            params.append(due_date)
        if return_date:
            query += 'return_date = %s, '
            params.append(return_date)
        query = query.rstrip(', ')
        query += 'WHERE record_id = %s'
        params.append(borrow_record_id)
        execute_and_commit(query, tuple(params))