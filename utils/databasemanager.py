import sqlite3
import shutil
import datetime

class DatabaseManager:
    """
    Advantage:
        Handle the errors and return error code
    """
    db_path = None

    def __init__(self, db_path):
        self.db_path = db_path
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
    
    def executescript(self, script):
        with open(script, 'r') as file:
            script_text = file.read()

        cursor = self.conn.cursor()
        try:
            cursor.executescript(script_text)
        
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        
        return cursor

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
    
    def backup(self, backup_folder):
        backup_file = backup_folder+f'{self.db_path}_backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        shutil.copy(self.db_path, backup_file)