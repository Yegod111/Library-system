from app.utils.db import execute_and_fetchone, execute_and_fetchall, execute_and_commit, transactional

class BookModel:
    @staticmethod
    def get_all(**kwargs):
        """Gets all books."""
        return execute_and_fetchall('SELECT * FROM books', (), **kwargs)
    

    @staticmethod
    def get_by_id(book_id, **kwargs):
        """Gets a book by book_id."""
        return execute_and_fetchone('SELECT * FROM books WHERE book_id = %s', (book_id,), **kwargs)
    

    @staticmethod
    def get_by_title(title, **kwargs):
        """Gets books by title."""
        return execute_and_fetchall('SELECT * FROM books WHERE title LIKE %s', (f'%{title}%',), **kwargs)
    

    @staticmethod
    def get_by_author(author, **kwargs):
        """Gets books by author."""
        return execute_and_fetchall('SELECT * FROM books WHERE author LIKE %s', (f'%{author}',), **kwargs)
    

    @staticmethod
    def get_by_isbn(isbn, **kwargs):
        """Gets books by isbn."""
        return execute_and_fetchall('SELECT * FROM books WHERE isbn = %s', (isbn,), **kwargs)


    @staticmethod
    def get_by_publisher(publisher, **kwargs):
        """Gets books by publisher."""
        return execute_and_fetchall('SELECT * FROM books WHERE publisher LIKE %s', (f"%{publisher}%",), **kwargs)


    @staticmethod
    def get_books_by_published_date(published_date, **kwargs):
        """Gets books by published data."""
        return execute_and_fetchall('SELECT * FROM books WHERE published_date = %s', (published_date,), **kwargs)

    
    @staticmethod
    def get_by_copies_available(copies_available, **kwargs):
        """Gets books by copies_available."""
        return execute_and_fetchall('SELECT * FROM books WHERE copies_available = %s', (copies_available,), **kwargs)


    @staticmethod
    def get_by_query(query, **kwargs):
        """Gets books by a search query matching title, author, ISBN, publisher or published_date."""
        query = f"%{query}%"
        return execute_and_fetchall('''
            SELECT * FROM books 
            WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s OR publisher LIKE %s OR published_date LIKE %s
        ''', (query, query, query, query, query), **kwargs)


    @staticmethod
    @transactional
    def add(title, author, isbn, publisher, published_date, copies_available):
        """Adds a book."""
        execute_and_commit(
            'INSERT INTO books (title, author, isbn, publisher, published_date, copies_available) VALUES (%s, %s, %s, %s, %s, %s)',
            (title, author, isbn, publisher, published_date, copies_available)
        )

    
    @staticmethod
    @transactional
    def update(book_id, title=None, author=None, isbn=None, publisher=None, published_date=None, copies_available=None):
        """Updates a book."""
        query = 'UPDATE books SET '
        params = []
        if title:
            query += 'title = %s, '
            params.append(title)
        if author:
            query += 'author = %s, '
            params.append(author)
        if isbn:
            query += 'isbn = %s, '
            params.append(isbn)
        if publisher:
            query += 'publisher = %s, '
            params.append(publisher)
        if published_date:
            query += 'published_date = %s, '
            params.append(published_date)
        if copies_available is not None:
            query += 'copies_available = %s, '
            params.append(copies_available)
        query = query.rstrip(', ')
        query += ' WHERE book_id = %s'
        params.append(book_id)
        execute_and_commit(query, tuple(params))


    @staticmethod
    @transactional
    def delete(book_id):
        """Deletes a book."""
        execute_and_commit('DELETE FROM books WHERE book_id = %s', (book_id,))