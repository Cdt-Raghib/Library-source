from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from utils.notificationbar import NotificationBar
#version: 2.0
"""
Fix it
"""
class DepositMultiple(MDScreen):
    help = StringProperty()
    db = None

    def deposit(self, numbers):
        nums = numbers.text.split(' ')
        self.db = self.parent.parent.parent.database
        self.history = self.parent.parent.parent.history
        self.main = self.parent.parent.parent.main

        self.err_list = []
        count = 0
        for f in nums:
            f.replace(' ', '')
            cn = self.db.fetchone('SELECT cadet_no FROM transactions WHERE book_no = ?', (int(f),), show_error=False)
            if isinstance(cn, int):
                self.err_list.append(f)
                continue
            self.db.execute('UPDATE users SET token=token+1 WHERE cadet_no = ?', (cn['cadet_no'],), show_error=False)
            self.db.execute('UPDATE books SET stock=stock+1 WHERE book_no = ?', (f,), show_error=False)
            a = self.db.execute('DELETE FROM transactions WHERE book_no = ?', (int(f),), show_error=False)
            count += 1
            cname = self.db.fetchone('SELECT cadet_name FROM users WHERE cadet_no=?', (cn['cadet_no'],))
            bname = self.db.fetchone('SELECT title FROM books WHERE book_no=?', (int(f),))
            self.history.execute('INSERT INTO history(activity_type, activity, account) VALUES (?,?,?)', ('DEPOSIT', f'{cname['cadet_name']}-{cn['cadet_no']} deposited {bname['title']}', self.main.current_account))
        
        if len(self.err_list) > 0:
            NotificationBar().open_with_text(text=f"Error with: {self.err_list}\nSuccessful: {count}", error=True)

        else:
            NotificationBar().open_with_text(text=f"{count} books successfully deposited")

        self.db.commit()

class DepositSingle(MDScreen):
    help = StringProperty()
    depo_info = StringProperty('Book name :---\nIssued to    :---')
    db = None
    issue = None

    def insert_comment(self, book_no, comment):
        pc = self.db.fetchone('SELECT comments FROM books WHERE book_no=?', (book_no,))
        if isinstance(pc, int):
            return
        pc = pc['comments']
        pc = '' if pc is None else pc
        print(pc)
        pc += f'<{self.issue['cadet_no']}>{comment}[end_comment]'
        print(pc)
        return self.db.execute('UPDATE books SET comments=? WHERE book_no=?', (pc,book_no))

    def deposit(self, number, comments):
        if self.db is None or self.issue is None:
            NotificationBar().open_with_text(text="Record not found", error=True)
            return
        a = self.db.execute('DELETE FROM transactions WHERE book_no = ?', (number.text,), on_error='<ec>: Record not found')
        if isinstance(a, int):
            return
        a = self.db.execute('UPDATE users SET token=token+1 WHERE cadet_no=?', (self.issue['cadet_no'],), on_error='<ec>: User token update failed')
        if isinstance(a, int):
            return
        a = self.db.execute('UPDATE books SET stock=stock+1 WHERE book_no = ?', (number.text,), on_error='<ec>: Stock update failed')
        if isinstance(a, int):
            return
        if comments.text != '':
            self.insert_comment(number.text, comments.text)
        
        NotificationBar().open_with_text(text='Deposited successfully.')
        cname = self.db.fetchone('SELECT cadet_name FROM users WHERE cadet_no=?', (self.issue['cadet_no'],))
        bname = self.db.fetchone('SELECT title FROM books WHERE book_no=?', (int(number.text),))
        self.history.execute('INSERT INTO history(activity_type, activity, account) VALUES (?,?,?)', ('DEPOSIT', f'{cname['cadet_name']} deposited {bname['title']}', self.main.current_account))
        self.db.commit()
        
        
    def search_in_issue(self, book_no):
        self.db = self.parent.parent.parent.database
        self.history = self.parent.parent.parent.history
        self.main = self.parent.parent.parent.main
        self.issue = self.db.fetchone('SELECT cadet_no FROM transactions WHERE book_no = ?', (book_no,), show_error = False)
        if isinstance(self.issue, int) or self.issue is None:
            return
        cname = self.db.fetchone('SELECT cadet_name FROM users WHERE cadet_no=?', (self.issue['cadet_no'],))
        bname = self.db.fetchone('SELECT title FROM books WHERE book_no=?', (int(book_no),))
        self.depo_info = f"Book name  : {bname['title']}\nIssued to    : {cname['cadet_name']} ({self.issue['cadet_no']})"
        


class Deposit(MDScreen):
    database = None
    main = None
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
        self.database = kwargs.get('databases').get('library.db')
        self.history = kwargs.get('databases').get('history.db')
        self.main = kwargs.get('main')

    def refresh(self, **kwargs):
        pass


Builder.load_file('kivymd/deposit.kv')
