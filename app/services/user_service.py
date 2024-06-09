from app.models.borrow_record import BorrowRecordModel
from app.models.book import BookModel
from datetime import datetime, timedelta

class UserService:
    @staticmethod
    def borrow_book(book_id, user_id):
        """Borrows a book."""
        try:
            book = BookModel.get_by_id(book_id, dictionary=True)
            if not book or book.get('copies_available') < 1:
                return 'Book is not available for borrowing.', 'danger'
            record = BorrowRecordModel.get_validating_by_user_and_book(user_id, book_id, dictionary=True)
            if record:
                return 'You have borrowed this book.', 'danger'
            
            borrow_date = datetime.now()
            due_date = datetime.now() + timedelta(days=14)  # 2 weeks borrowing period
            BorrowRecordModel.add(user_id, book_id, borrow_date, due_date)
            BookModel.update(book_id, copies_available=book.get('copies_available') - 1)
            return 'Book borrowed successfully!', 'success'
        except Exception as e:
            return f'Error borrowing book: {e}', 'danger'


    @staticmethod
    def renew_book(user_id, book_id):
        """Renews a borrowed book."""
        try:
            record = BorrowRecordModel.get_validating_by_user_and_book(user_id, book_id, dictionary=True)
            if not record:
                return 'You have not borrowed this book or it has already been returned.', 'danger'
            
            new_due_date = record.get('borrow_date') + timedelta(days=21)  # Extend by 1 more week
            BorrowRecordModel.update(record.get('record_id'), due_date=new_due_date)
            return 'Book renewed successfully!', 'success'
        except Exception as e:
            return f'Error renewing book: {e}', 'danger'


    @staticmethod
    def return_book(book_id, user_id):
        """Returns a borrowed book."""
        try:
            record = BorrowRecordModel.get_validating_by_user_and_book(user_id, book_id, dictionary=True)
            if not record:
                return 'You have not borrowed this book or it has already been returned.', 'danger'
            
            BorrowRecordModel.update(record.get('record_id'), return_date=datetime.now())
            book = BookModel.get_by_id(book_id, dictionary=True)
            BookModel.update(book_id, copies_available=book.get('copies_available') + 1)
            return 'Book returned successfully!', 'success'  
        except Exception as e:
            return f'Error returning book: {e}', 'danger'


    @staticmethod
    def get_borrowed_books_by_user(user_id, **kwargs):
        """Gets all borrowed books by a user."""
        validating_borrow_records = BorrowRecordModel.get_all_validating_by_user(user_id, dictionary=True)
        borrowed_books = []
        for record in validating_borrow_records:
            borrowed_book = BookModel.get_by_id(record.get('book_id'), **kwargs)
            borrowed_book.update({'borrow_date': record.get('borrow_date')})
            borrowed_book.update({'due_date': record.get('due_date')})
            borrowed_books.append(borrowed_book)
        return borrowed_books
