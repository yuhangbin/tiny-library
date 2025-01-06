import pytest
from app import create_app
from app.database import db
from app.models import Book
import json
from datetime import date

@pytest.fixture
def app():
    app = create_app('config.TestConfig')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_book(client):
    data = {
        'title': 'Test Book',
        'author': 'Test Author',
        'isbn': '1234567890123',
        'published_date': '2024-03-20'
    }
    
    response = client.post('/api/books', 
                          data=json.dumps(data),
                          content_type='application/json')
    
    assert response.status_code == 201
    assert response.json['title'] == 'Test Book'
    assert response.json['author'] == 'Test Author'

def test_get_books(client):
    # Create a test book
    book = Book(title='Test Book', author='Test Author')
    with client.application.app_context():
        db.session.add(book)
        db.session.commit()
    
    response = client.get('/api/books')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['title'] == 'Test Book'

def test_get_book(client):
    book = Book(title='Test Book', author='Test Author')
    with client.application.app_context():
        db.session.add(book)
        db.session.commit()
        book_id = book.id
    
    response = client.get(f'/api/books/{book_id}')
    assert response.status_code == 200
    assert response.json['title'] == 'Test Book'

def test_update_book(client):
    book = Book(title='Test Book', author='Test Author')
    with client.application.app_context():
        db.session.add(book)
        db.session.commit()
        book_id = book.id
    
    update_data = {
        'title': 'Updated Book',
        'author': 'Updated Author'
    }
    
    response = client.put(f'/api/books/{book_id}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Book'
    assert response.json['author'] == 'Updated Author'

def test_delete_book(client):
    book = Book(title='Test Book', author='Test Author')
    with client.application.app_context():
        db.session.add(book)
        db.session.commit()
        book_id = book.id
    
    response = client.delete(f'/api/books/{book_id}')
    assert response.status_code == 204
    
    # Verify book is deleted
    response = client.get(f'/api/books/{book_id}')
    assert response.status_code == 404 