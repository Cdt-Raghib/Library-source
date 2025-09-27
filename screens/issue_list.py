from kivymd.uix.button import MDButton,  MDButtonText
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog,\
MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDListItem
from kivy.properties import StringProperty, ListProperty

Builder.load_file('kivymd/issue-list.kv')
class MyList(MDListItem):
    book_name = StringProperty('')
    cadet_name = StringProperty('')
    book_no = StringProperty('')
    cadet_no = StringProperty('')
    issue_date = StringProperty('')

    def show_details(self):
        self.dial = MDDialog(
            MDDialogHeadlineText(
                text='Details'
                ),
            MDDialogSupportingText(
                text=f'\
                Book name : {self.book_name}\n\
                Book no.  : {self.book_no}\n\
                Issued to : {self.cadet_name} ({self.cadet_no})\n\
                Issue date: {self.issue_date}'
                ),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(
                        text='Close',
                        on_release=lambda x:self.dial.dismiss()
                    )
                )
            )
        )
        self.dial.open()

class IssueList(MDScreen):
    issue_database = None
    issue_data = ListProperty([])
    searchby = StringProperty('Cadet no')
    
    def open_options(self, caller):
        self.items = [
        {
        'text':'Book name',
        'on_release':lambda x='book_name', y='Book name':self.search_by(x,y),
        },
        {
        'text':'Book no.',
        'on_release':lambda x='book_no', y='Book no.':self.search_by(x,y),
        },
        {
        'text':'Cadet no.',
        'on_release':lambda x='cadet_no', y='Cadet no.':self.search_by(x,y),
        },
        {
        'text':'Cadet name',
        'on_release':lambda x='cadet_name', y='Cadet name':self.search_by(x,y),
        }
        ]
        self.options = MDDropdownMenu(items = self.items, caller=caller, position='bottom', theme_bg_color='Custom',
                                      md_bg_color='orange')
        self.options.open()

    def app_request(self, **kwargs):
        """
            Create a database object in main and pass it to here
        """
        self.issue_database = kwargs.get('db1', None)
        if self.issue_database is None:
            raise ValueError("No database object provided to issue_list screen")
        
    def search(self, text, search = True):
        if search:
            fetched = self.issue_database.fetchall(f'SELECT * FROM transactions WHERE {self.searchby} LIKE ?', (f'%{text}%',))
        else:
            fetched = self.issue_database.fetchall('SELECT * FROM transactions')
        self.issue_data.clear()
            

        for row in fetched:
            row = dict(row)
            cn = self.issue_database.fetchone('SELECT cadet_name FROM users WHERE cadet_no = ?', (row['cadet_no'],))
            bn = self.issue_database.fetchone('SELECT book_name FROM books WHERE book_no = ?', (row['book_no'],))
            self.issue_data.append(
                {
                    'viewclass': 'MyList',
                    'book_no': row['book_no'],
                    'cadet_no': row['cadet_no'],
                    'issue_date': row['issue_date'],
                    'book_name': bn['book_name'] if bn else 'Unknown',
                    'cadet_name': cn['cadet_name'] if cn else 'Unknown',
                }
            )

    def search_by(self, hint, plate_text):
        self.searchby = hint
        self.ids.search_plate.text = plate_text
        self.options.dismiss()


# class TestApp(MDApp):
#     def build(self):
#         return 
    
# if __name__ == '__main__':
#     TestApp().run()