from flask import Blueprint, request, jsonify
from .models import Book
from .database import db
from datetime import datetime

book_bp = Blueprint('book', __name__)

@book_bp.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    
    try:
        published_date = datetime.strptime(data.get('published_date'), '%Y-%m-%d').date() if data.get('published_date') else None
        new_book = Book(
            title=data['title'],
            author=data['author'],
            isbn=data.get('isbn'),
            published_date=published_date
        )
        
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.to_dict()), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@book_bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@book_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

@book_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    
    try:
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'isbn' in data:
            book.isbn = data['isbn']
        if 'published_date' in data:
            book.published_date = datetime.strptime(data['published_date'], '%Y-%m-%d').date() if data['published_date'] else None
        
        db.session.commit()
        return jsonify(book.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@book_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    try:
        db.session.delete(book)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 