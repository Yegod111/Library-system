from app.models.book import BookModel

class BookService:
    @staticmethod
    def get_all_books(**kwargs):
        """Lists all books."""
        return BookModel.get_all(**kwargs)


    @staticmethod
    def get_book_by_id(book_id, **kwargs):
        """Gets a book by ID."""
        return BookModel.get_by_id(book_id, **kwargs)


    @staticmethod
    def get_books_by_title(title, **kwargs):
        """Gets books by title."""
        return BookModel.get_by_title(title, **kwargs)


    @staticmethod
    def get_books_by_author(author, **kwargs):
        """Gets books by author."""
        return BookModel.get_by_author(author, **kwargs)


    @staticmethod
    def get_books_by_isbn(isbn, **kwargs):
        """Gets books by ISBN."""
        return BookModel.get_by_isbn(isbn, **kwargs)


    @staticmethod
    def get_books_by_publisher(publisher, **kwargs):
        """Gets books by publisher."""
        return BookModel.get_by_publisher(publisher, **kwargs)


    @staticmethod
    def get_books_by_published_date(published_date, **kwargs):
        """Gets books by published date."""
        return BookModel.get_books_by_published_date(published_date, **kwargs)


    @staticmethod
    def get_books_by_copies_available(copies_available, **kwargs):
        """Gets books by copies available."""
        return BookModel.get_by_copies_available(copies_available, **kwargs)


    @staticmethod
    def search_books(query, **kwargs):
        """Searched books by a general query."""
        return BookModel.get_by_query(query, **kwargs)
    

    @staticmethod
    def add_book(form_data):
        """Adds a new book."""
        title = form_data.get('title')
        author = form_data.get('author')
        isbn = form_data.get('isbn')
        publisher = form_data.get('publisher')
        published_date = form_data.get('published_date')
        copies_available = form_data.get('copies_available', 0)  # default to 0 if not provided

        try:
            BookModel.add(title, author, isbn, publisher, published_date, copies_available)
            return 'Book added successfully!', 'success'
        except Exception as e:
            return f'Error adding book: {e}', 'danger'
        
    
    @staticmethod
    def update_book(book_id, form_data):
        """Updates an existing book."""
        title = form_data.get('title')
        author = form_data.get('author')
        isbn = form_data.get('isbn')
        publisher = form_data.get('publisher')
        published_date = form_data.get('published_date')
        copies_available = form_data.get('copies_available')

        try:
            BookModel.update(book_id, title, author, isbn, publisher, published_date, copies_available)
            return 'Book updated successfully!', 'success'
        except Exception as e:
            return f'Error updating book: {e}', 'danger' 


    @staticmethod
    def delete_book(book_id):
        """Deletes a book."""
        try:
            BookModel.delete(book_id)
            return 'Book deleted successfully!', 'success'
        except Exception as e:
            return f'Error deleting book: {e}', 'danger'