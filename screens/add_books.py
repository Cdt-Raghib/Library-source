from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from utils.book import Books
from utils.notificationbar import NotificationBar
from utils.historywriter import HistoryWriter

'''
Feature to be added:
    multiple books add
'''
Builder.load_file('kivymd/add-books-single.kv')
class AddBooks(MDScreen):
    database = None
    books = None
    input_info = {}

    def refresh(self, **kwargs):
        pass
    
    def app_request(self, **kwargs):
        self.database = kwargs.get('databases').get('library.db')
        self.history = HistoryWriter(master=kwargs.get('main'), database=kwargs.get('databases').get('history.db'), activity_type='ADD BOOK')
        self.books = Books(self.database)

    def move_next(self, inst):
        fields = [f for f in self.children[0].children[0].children if f.__class__.__name__ == "ATextField"]
        if inst in fields:
            idx = fields.index(inst)
            if idx - 1 >= 0:
                fields[idx - 1].focus = True
    
    def add_book(self):
        if not self.fetch_info():
            return 
        r = self.books.add(self.input_info)
        if not isinstance(r, int):
            NotificationBar().open_with_text(text='Book added successfully.')
            self.history.write(f'{self.input_info['title']} was added to book list.')

    def rectify(self, key):
        key = key.lower()
        key = key.replace(' ', '_')
        key = key.replace('.', '')
        return key
    
    def fetch_info(self):
        for f in self.children[0].children[0].children:
            if f.__class__.__name__ == "ATextField":
                print(f.hint_text, f.text)
                if f.required and f.text == '':
                    NotificationBar().open_with_text(text='Fill all required fields', error=True)
                    return False
                self.input_info[self.rectify(f.hint_text)] = f.text
        
        return True
        

# class TestApp(MDApp):
#     def build(self):
#         return Builder.load_file('kivymd/add-books-single.kv')

# if __name__ == '__main__':
#     TestApp().run()