import avro

class Books:
    """
    Book class to handle book information from database/library.db
    Support for bangla will be added later
    Using queries directly
    """
    keys = ['book_no', 'icon', 'title', 'author', 'donated_by', 'average_rating','stock', 'comments', 'category']
    database = None

    def __init__(self, db):
        self.database = db
    
    def _decode(self, text):
        if not isinstance(text, str):
            return text
        
        if '[bn]' in text:
            # Depricated
            bntext = text.split('[bn]', 1)[1].split('[/bn]', 1)[0]
            text.replace(f'[bn]{bntext}[/bn]',avro.parse(bntext))
        
        return text

    def _encode(self, text):
        """
        Bangla text will be encoded in [bn]...[/bn] tags
        """
        return text

    def get(self, book_no, key, show_error=True, on_error=''):
        if key not in self.keys:
            raise ValueError(f"Unknown option: {key}. Permitted options are: {self.keys}")  
        query = f"SELECT {key} FRoM books WHERE book_no = ?"
        value = self.database.fetchone(query, (book_no,), on_error=on_error, show_error=show_error)
        return self._decode(value)

    def search(self, search_in, value, get='*') -> list:
        if search_in not in self.keys:
            raise ValueError(f"Unknown option: {search_in}. Permitted options are: {self.keys}")
        if get not in self.keys:
            raise ValueError(f"Unknown option: {get}. Permitted options are: {self.keys}")
        query = f"SELECT {get} FROM books WHERE {search_in} LIKE ?"
        results = self.database.fetchall(query, (f'%{value}%',), show_error=False)
        if isinstance(results, int):
            return results
        books = []
        for row in results:
            row = dict(row)
            book = {key: self._decode(row[key]) for key in self.keys}
            books.append(book)
        return books

    def set(self, key, value, where_key, where_value, commit=True) -> int:
        """
        Returns error code from database.execute() if any error occurs
        Otherwise returns None
        """
        if key not in self.keys:
            raise ValueError(f"Unknown option: {key}. Permitted options are: {self.keys}")
        if where_key not in self.keys:
            raise ValueError(f"Unknown option: {where_key}. Permitted options are: {self.keys}")
        value = self._encode(value)
        query = f"UPDATE books SET {key} = ? WHERE {where_key} = ?"
        result = self.database.execute(query, (value, where_value))
        if isinstance(result, int):
            return result
        if commit:
            self.database.commit()

    def add(self, book_info: dict, commit=True) -> int:
        """
        book_info should contain all keys in self.keys except 'available'
        'available' will be set to 'stock' value
        Returns error code from database.execute() if any error occurs
        Otherwise returns None
        """
        columns = ''
        placeholders = ''
        for key,value in book_info.items():
            column += f'{key}, '
            placeholders += f'{value}, '
        
        columns = columns.rstrip(', ')
        placeholders = placeholders.rstrip(', ')

        query = f"INSERT INTO books ({columns}) VALUES ({placeholders});"
        result = self.database.execute(query, on_error='<ec>:Book already exists.')
        if isinstance(result, int):
            return result
        if commit:
            self.database.commit()  