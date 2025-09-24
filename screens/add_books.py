from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

'''
Feature to be added:
    multiple books add
'''
Builder.load_file('kivymd/add-books-single.kv')
class AddBooks(MDScreen):
    def app_request(self, **kwargs):
        pass
    
    def move_next(self, inst):
        print(self.children[0].children[0].children)
        ind = self.children[0].children[0].children.index(inst)
        print(f'found ind:{ind}')
        if ind!=-1 and ind-1>0:
            self.children[0].children[0].children[ind-1].focus = True

# class TestApp(MDApp):
#     def build(self):
#         return Builder.load_file('kivymd/add-books-single.kv')

# if __name__ == '__main__':
#     TestApp().run()