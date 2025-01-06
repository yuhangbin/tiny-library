import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, init_db
from app.repositories.book_repository import BookRepository
from app.models import Book

@pytest.fixture(scope="function")
def session():
    # Create an in-memory SQLite database for testing
    engine = create_engine('sqlite:///:memory:')
    init_db('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    
    yield
    
    Base.metadata.drop_all(engine)

@pytest.fixture
def book_repository(session):
    return BookRepository()

def test_create_book(book_repository):
    book = book_repository.create(
        title='Test Book',
        author='Test Author',
        isbn='1234567890123',
        published_date='2024-03-20'
    )
    
    assert book.title == 'Test Book'
    assert book.author == 'Test Author'
    assert book.isbn == '1234567890123'
    assert book.published_date == datetime.strptime('2024-03-20', '%Y-%m-%d').date()

def test_get_books(book_repository):
    book_repository.create(title='Test Book 1', author='Test Author 1')
    book_repository.create(title='Test Book 2', author='Test Author 2')
    
    books = book_repository.get_all()
    assert len(books) == 2
    assert books[0].title == 'Test Book 1'
    assert books[1].title == 'Test Book 2'

def test_get_book(book_repository):
    book = book_repository.create(title='Test Book', author='Test Author')
    retrieved_book = book_repository.get_by_id(book.id)
    
    assert retrieved_book.title == 'Test Book'
    assert retrieved_book.author == 'Test Author'

def test_update_book(book_repository):
    book = book_repository.create(title='Test Book', author='Test Author')
    
    updated_book = book_repository.update(book.id, {
        'title': 'Updated Book',
        'author': 'Updated Author'
    })
    
    assert updated_book.title == 'Updated Book'
    assert updated_book.author == 'Updated Author'

def test_delete_book(book_repository):
    book = book_repository.create(title='Test Book', author='Test Author')
    book_repository.delete(book.id)
    
    with pytest.raises(ValueError):
        book_repository.get_by_id(book.id) 