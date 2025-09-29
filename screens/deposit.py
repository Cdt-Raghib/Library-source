from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty

#version: 2.0
"""
Fix it
"""
class DepositMultiple(MDScreen):
    help = StringProperty()
    depo_info = StringProperty('Book name :---\nIssued by    :---')
    db = None

    def deposit(self, numbers):
        nums = numbers.split(',')
        self.db = self.parent.parent.parent.database
        for f in nums:
            f.replace(' ', '')
            self.db.execute('DELETE FROM transactions WHERE book_no = ?', (int(f),), on_error=f'<ec>: Record not found {f}',\
                            on_success='Successfully deposited')


class DepositSingle(MDScreen):
    help = StringProperty()
    depo_info = StringProperty('Book name :---\nIssued to    :---')
    db = None

    def deposit(self, number):
        if self.db is None:
            return
        self.db.execute('DELETE FROM transactions WHERE book_no = ?', (number.text,), on_error='<ec>: Record not found')
        
        
    def search_in_issue(self, book_no):
        self.db = self.parent.parent.parent.database
        issue = self.db.fetchone('SELECT book_no, cadet_no FROM transactions WHERE book_no = ?', (book_no,), show_error = False)
        if isinstance(issue, int) or issue is None:
            return
        self.depo_info = f"Book name : {issue[0]}\nIssued to    : {issue[1]}"
        


class DepositScreen(MDScreen):
    database = None

    def switch_content(self, instance_tabs, instance_tab, instance_tab_label):
        """Called when a secondary tab is switched."""
        tab_text = instance_tab.children[0].children[0].text
        self.ids.content_box.clear_widgets()
        if tab_text == "Single":
            self.ids.content_box.add_widget(DepositSingle())
        elif tab_text == "Multiple":
            self.ids.content_box.add_widget(DepositMultiple())
    
    def app_request(self, **kwargs):
        self.ids.tab.switch_tab(text = self.ids.text1.text)
        self.database = kwargs.get('db1')


Builder.load_file('kivymd/deposit.kv')
