from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from ..database import get_session
from ..models import Book

class BookRepository:
    def create(self, title: str, author: str, isbn: str = None, published_date: str = None) -> Book:
        """Create a new book."""
        session = get_session()
        try:
            parsed_date = datetime.strptime(published_date, '%Y-%m-%d').date() if published_date else None
            book = Book(
                title=title,
                author=author,
                isbn=isbn,
                published_date=parsed_date
            )
            session.add(book)
            session.commit()
            return book
        except Exception as e:
            session.rollback()
            raise e

    def get_all(self) -> list[Book]:
        """Get all books."""
        session = get_session()
        return session.query(Book).all()

    def get_by_id(self, book_id: int) -> Book:
        """Get a book by ID."""
        session = get_session()
        book = session.query(Book).get(book_id)
        if not book:
            raise ValueError(f"Book with id {book_id} not found")
        return book

    def update(self, book_id: int, data: dict) -> Book:
        """Update a book."""
        session = get_session()
        try:
            book = self.get_by_id(book_id)
            
            if 'title' in data:
                book.title = data['title']
            if 'author' in data:
                book.author = data['author']
            if 'isbn' in data:
                book.isbn = data['isbn']
            if 'published_date' in data:
                book.published_date = datetime.strptime(data['published_date'], '%Y-%m-%d').date() if data['published_date'] else None

            session.commit()
            return book
        except Exception as e:
            session.rollback()
            raise e

    def delete(self, book_id: int) -> None:
        """Delete a book."""
        session = get_session()
        try:
            book = self.get_by_id(book_id)
            session.delete(book)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e 