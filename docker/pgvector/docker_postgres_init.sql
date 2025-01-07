-- First check if database exists, then create if it doesn't
SELECT 'CREATE DATABASE library'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'library')

\c library;

CREATE TABLE IF NOT EXISTS book (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(13) UNIQUE,
    published_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

