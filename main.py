from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import List, Optional

# Create base class for declarative models
Base = declarative_base()

# Define Book model
class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(13), unique=True)
    published_date = Column(Date)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class DatabaseManager:
    def __init__(self):
        # Create database connection
        self.engine = create_engine(
            'postgresql://postgres:password@localhost:15432/library',
            echo=False  # Set to True for SQL query logging
        )
        # Create session factory
        self.Session = sessionmaker(bind=self.engine)
        # Add this at the end of the DatabaseManager.__init__ method if you want automatic table creation
        Base.metadata.create_all(self.engine)

    def get_all_books(self) -> List[dict]:
        """Retrieve all books from the database"""
        session = self.Session()
        try:
            books = session.query(Book).all()
            return [book.to_dict() for book in books]
        finally:
            session.close()

    def add_book(self, title: str, author: str, isbn: Optional[str] = None, 
                published_date: Optional[str] = None) -> None:
        """Add a new book to the database"""
        session = self.Session()
        try:
            book = Book(
                title=title,
                author=author,
                isbn=isbn,
                published_date=datetime.strptime(published_date, '%Y-%m-%d').date() if published_date else None
            )
            session.add(book)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_book_by_isbn(self, isbn: str) -> Optional[dict]:
        """Retrieve a book by its ISBN"""
        session = self.Session()
        try:
            book = session.query(Book).filter(Book.isbn == isbn).first()
            return book.to_dict() if book else None
        finally:
            session.close()

    def update_book(self, isbn: str, **kwargs) -> bool:
        """Update a book's information"""
        session = self.Session()
        try:
            book = session.query(Book).filter(Book.isbn == isbn).first()
            if not book:
                return False
            
            for key, value in kwargs.items():
                if hasattr(book, key):
                    if key == 'published_date' and value:
                        value = datetime.strptime(value, '%Y-%m-%d').date()
                    setattr(book, key, value)
            
            session.commit()
            return True
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_book(self, isbn: str) -> bool:
        """Delete a book by ISBN"""
        session = self.Session()
        try:
            book = session.query(Book).filter(Book.isbn == isbn).first()
            if not book:
                return False
            session.delete(book)
            session.commit()
            return True
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

if __name__ == "__main__":
    # Example usage
    db = DatabaseManager()
    try:
        # Add some sample books
        db.add_book(
            "The Great Gatsby",
            "F. Scott Fitzgerald",
            "9780743273565",
            "1925-04-10"
        )
        db.add_book(
            "To Kill a Mockingbird",
            "Harper Lee",
            "9780446310789",
            "1960-07-11"
        )

        # Get all books
        all_books = db.get_all_books()
        print("\nAll books in database:")
        for book in all_books:
            print(f"Title: {book['title']}, Author: {book['author']}")

        # Get a specific book by ISBN
        isbn = "9780743273565"
        book = db.get_book_by_isbn(isbn)
        if book:
            print(f"\nFound book with ISBN {isbn}:")
            print(f"Title: {book['title']}, Author: {book['author']}")

        # Update a book
        db.update_book(
            isbn="9780743273565",
            title="The Great Gatsby (Updated Edition)"
        )

        # Delete a book
        db.delete_book("9780446310789")

    except Exception as e:
        print(f"An error occurred: {e}") 