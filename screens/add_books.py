from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from utils.book import Books

'''
Feature to be added:
    multiple books add
'''
Builder.load_file('kivymd/add-books-single.kv')
class AddBooks(MDScreen):
    database = None
    books = None
    input_info = {}

    def app_request(self, **kwargs):
        self.database = kwargs.get('db1')
        self.books = Books(self.database)

    def move_next(self, inst):
        print(self.children[0].children[0].children)
        ind = self.children[0].children[0].children.index(inst)
        print(f'found ind:{ind}')
        if ind!=-1 and ind-1>0:
            self.children[0].children[0].children[ind-1].focus = True
    
    def add_book(self):
        self.fetch_info()
        self.books.add(self.input_info)

    def rectify(self, key):
        key = key.lower()
        key = key.replace(' ', '_')
        key = key.replace('.', '')
        return key
    
    def fetch_info(self):
        print(self.children[0].children[0].children)
        for f in self.children[0].children[0].children:
            if f.__class__.__name__ == "ATextField":
                print(f.hint_text, f.text)
                self.input_info[self.rectify(f.hint_text)] = f.text
        
        print(self.input_info)
        

# class TestApp(MDApp):
#     def build(self):
#         return Builder.load_file('kivymd/add-books-single.kv')

# if __name__ == '__main__':
#     TestApp().run()