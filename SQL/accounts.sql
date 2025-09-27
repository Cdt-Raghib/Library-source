CREATE TABLE if NOT EXISTS accounts (
    username TEXT PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    role TEXT DEFAULT 'assistant',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT or IGNORE INTO accounts (username, password, role) VALUES
('ehqmr2veklmf', 't}vpmfvev}D6668', 'admin'),
('gsehqmr2pmfvev}', 'gsehqmrDpmfvev}', 'coadmin'),
('ewwx2pmfvev}', 'm$eq$e$zspyrxiiv', 'assistant');
