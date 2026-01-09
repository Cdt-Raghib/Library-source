CREATE TABLE if NOT EXISTS users (
    cadet_no INTEGER PRIMARY KEY,
    cadet_name TEXT NOT NULL,
    batch INTEGER NOT NULL,
    token INTEGER DEFAULT 2,
    role TEXT DEFAULT 'Member',
    joined TEXT DEFAULT (DATE('now')) 
)STRICT;

CREATE TABLE if NOT EXISTS books (
    book_no INTEGER PRIMARY KEY,
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
--create book name also if necessary:done
CREATE TABLE if NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY,
    title TEXT REFERENCES books(title),
    cadet_no INTEGER,
    book_no INTEGER,
    issue_date DATE DEFAULT (DATE('now')),
    return_date DATE,
    FOREIGN KEY (cadet_no) REFERENCES users(cadet_no),
    FOREIGN KEY (book_no) REFERENCES books(book_no)
);

