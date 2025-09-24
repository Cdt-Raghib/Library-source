from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.properties import StringProperty

'''
Feature to be added:
    add a seperator before cadet no.: Done
    add something to understand screen is scrollable: Done

'''

Builder.load_file('kivymd/issue.kv')

class IssueBooks(MDScreen):
    issue_cadet_name = StringProperty('None')
    issue_cadet_batch = StringProperty('None')
    
    def app_request(self, **kwargs):
        pass

    def move_next(self, inst):
        print(self.children[0].children[0].children)
        ind = self.children[0].children[0].children.index(inst)
        print(f'found ind:{ind}')
        if ind!=-1 and ind-1>0:
            self.children[0].children[0].children[ind-1].focus = True
    
    def search(self, cadet_no):
        print(cadet_no.text)