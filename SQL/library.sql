CREATE TABLE if NOT EXISTS users (
    cadet_no INTEGER PRIMARY KEY,
    cadet_name TEXT NOT NULL,
    token INTEGER DEFAULT 2,
    role TEXT DEFAULT 'member',
    joined DATE DEFAULT (DATE('now'))
);

CREATE TABLE if NOT EXISTS books (
    book_NO INTEGER PRIMARY KEY,
    icon TEXT DEFAULT 'book-open-page-variant',
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    donated_by INTEGER,
    stock INTEGER DEFAULT 1,
    average_rating FLOAT DEFAULT 0.0,
    category TEXT,
    comments TEXT,
    FOREIGN KEY (donated_by) REFERENCES users(cadet_no)
);

CREATE TABLE if NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY,
    cadet_no INTEGER,
    book_NO INTEGER,
    issue_date DATE DEFAULT (DATE('now')),
    return_date DATE,
    FOREIGN KEY (cadet_no) REFERENCES users(cadet_no),
    FOREIGN KEY (book_NO) REFERENCES books(book_NO)
);

