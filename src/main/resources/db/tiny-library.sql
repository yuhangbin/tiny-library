\c ollama;

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS hstore;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"

CREATE TABLE IF NOT EXISTS book_segments (
	id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    book_id VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS book_segments_embedding_idx ON book_segments
USING HNSW (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS book_segments_book_id_idx ON book_segments(book_id);