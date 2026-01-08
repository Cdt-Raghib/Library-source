CREATE TABLE IF NOT EXISTS  history(
    id INTEGER PRIMARY KEY,
    hdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    account TEXT DEFAULT 'assistant',
    activity_type TEXT,
    activity TEXT
);