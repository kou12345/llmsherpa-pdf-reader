-- PostgreSQL

-- books テーブルの作成
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- pages テーブルの作成
CREATE TABLE pages (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL,
    content TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

-- updated_at カラムを自動更新するための関数とトリガーの作成
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- books テーブルに対するトリガー
CREATE TRIGGER update_books_modtime
    BEFORE UPDATE ON books
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- pages テーブルに対するトリガー
CREATE TRIGGER update_pages_modtime
    BEFORE UPDATE ON pages
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();
