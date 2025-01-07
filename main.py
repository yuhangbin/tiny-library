import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict

def get_database_connection():
    """Establish a connection to the PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            dbname="library",
            user="postgres",
            password="password",  # Make sure this matches your docker-compose password
            host="localhost",
            port="15432"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        raise

def get_all_books() -> List[Dict]:
    """Retrieve all books from the database"""
    conn = get_database_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM book")
            books = cur.fetchall()
            return [dict(book) for book in books]
    finally:
        conn.close()

def add_book(title: str, author: str, isbn: str = None, published_date: str = None) -> None:
    """Add a new book to the database"""
    conn = get_database_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO book (title, author, isbn, published_date)
                VALUES (%s, %s, %s, %s)
                """,
                (title, author, isbn, published_date)
            )
            conn.commit()
    finally:
        conn.close()

def get_book_by_isbn(isbn: str) -> Dict:
    """Retrieve a book by its ISBN"""
    conn = get_database_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM book WHERE isbn = %s", (isbn,))
            book = cur.fetchone()
            return dict(book) if book else None
    finally:
        conn.close()

if __name__ == "__main__":
    # Example usage
    try:
        # Add some sample books
        add_book(
            "The Great Gatsby",
            "F. Scott Fitzgerald",
            "9780743273565",
            "1925-04-10"
        )
        add_book(
            "To Kill a Mockingbird",
            "Harper Lee",
            "9780446310789",
            "1960-07-11"
        )

        # Get all books
        all_books = get_all_books()
        print("\nAll books in database:")
        for book in all_books:
            print(f"Title: {book['title']}, Author: {book['author']}")

        # Get a specific book by ISBN
        isbn = "9780743273565"
        book = get_book_by_isbn(isbn)
        if book:
            print(f"\nFound book with ISBN {isbn}:")
            print(f"Title: {book['title']}, Author: {book['author']}")

    except Exception as e:
        print(f"An error occurred: {e}") 