import sqlite3

class DatabaseManager:
    """
    Advantage:
        Handle the errors and return error code
    """
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Access columns by name if needed

    def execute(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor  # Caller can fetch data or commit

    def fetchall(self, query, params=()):
        cursor = self.execute(query, params)
        return cursor.fetchall()

    def fetchone(self, query, params=()):
        cursor = self.execute(query, params)
        return cursor.fetchone()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()