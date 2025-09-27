import sqlite3
import shutil
import datetime
from kivy.lang import Builder
from kivymd.uix.snackbar import MDSnackbar
from kivy.properties import StringProperty

Builder.load_file('kivymd/error-bar.kv')
class ErrorBar(MDSnackbar):
    text = StringProperty('')

    def open_with_text(self, text):
        self.text = text
        self.open()

    def help(self):
        pass

    def play_sound(self):
        pass

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

    def execute(self, query, params=(), show_error=True, on_error=''):
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
        
        except sqlite3.IntegrityError as e:
            if show_error:
                if on_error != '':
                    on_error = on_error.replace('<ec>', 101)
                    ErrorBar().open_with_text(on_error)
                
                else:
                    ErrorBar().open_with_text(f"IntegrityError: {e} from {self.db_path}")
            return 101
        
        except sqlite3.OperationalError as e:
            if show_error:
                if on_error != '':
                    on_error = on_error.replace('<ec>', 102)
                    ErrorBar().open_with_text(on_error)
                
                else:
                    ErrorBar().open_with_text(f"OperationalError: {e} from {self.db_path}")
            return 102
        
        return cursor  # Caller can fetch data or commit

    def fetchall(self, query, params=(), on_error='', show_error=True):
        cursor = self.execute(query, params, show_error, on_error)
        if isinstance(cursor, int):
            return cursor  # Return error code if execute failed
        return cursor.fetchall()

    def fetchone(self, query, params=()):
        cursor = self.execute(query, params)
        if isinstance(cursor, int):
            return cursor  # Return error code if execute failed    
        return cursor.fetchone()
    
    def executescript(self, script_path):
        with open(script_path, 'r') as file:
            script_text = file.read()

        cursor = self.conn.cursor()
        cursor.executescript(script_text)
        
        return cursor

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
    
    def backup(self, backup_folder):
        backup_file = backup_folder+f'{self.db_path}_backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        shutil.copy(self.db_path, backup_file)