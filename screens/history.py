from kivymd.uix.button import MDButton,  MDButtonText
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog,\
MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer, MDDialogIcon
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.recycleview import RecycleView
# RecycleView.refresh_from_data
from kivymd.uix.list import MDListItem
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivymd.uix.button import MDButton
from kivy.uix.widget import Widget
from kivymd.uix.divider import MDDivider

Builder.load_file('kivymd/history.kv')

class HistoryList(MDListItem):
    icon = StringProperty('')
    activity = StringProperty('')
    date = StringProperty('')
    icon_color = StringProperty('white')

    def _convert_rgba(self, color:list, alpha=1):
        for f in color:
            yield f/255.
        yield alpha
    
    def convert_rgba(self, color:list, alpha=1) -> list:
        return list(self._convert_rgba(color, alpha))

    def show_details(self):
        self.dial = MDDialog(
            #MDDialogIcon(source = self.icon, size=(100,100), allow_stretch=True),
            MDDialogHeadlineText(
                text=self.name
                ),

            MDDialogSupportingText(
                text=f'\
                Cadet no. :  {self.cadet_no}\n\
                Batch       :  {self.batch}\n\
                Joined      :  {self.joined}\n',
                halign = "left"
                ),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text='Close'),
                    on_release=lambda x:self.dial.dismiss()
                )
            )
        )
        self.dial.open()


class History(MDScreen):
    history_database = None
    user_data = ListProperty([])
    searchby = StringProperty('ALL')
    total = NumericProperty()
    color_picker = {'Developer': [255,0,0], 'member': [255,255,255], 'Contributor':[34, 177, 76],
                    'Admin': [203, 46, 50]}
    icon_picker = {
        'DEPOSIT':['book-arrow-down-outline','green'], 
        'ISSUE':['book-arrow-up-outline', 'red'],
        'REGISTER': ['account-plus', 'green'],
        'ADD BOOK': ['book-plus', 'green'],
        'DELETED': ['trash-can-outline','red']
        }
    def open_options(self, caller):                                                                                                                                                                                                                      
        self.items = [                                                                                                                  
        {
        'text':'Deposit',
        'on_release':lambda x='DEPOSIT', y='Deposit':self.search_by(x,y),
        },
        {
        'text':'Books Added',
        'on_release':lambda x='ADD BOOK', y='Books Added':self.search_by(x,y),
        },
        {
        'text':'Registers',
        'on_release':lambda x='REGISTER', y='Registers':self.search_by(x,y),
        },
        {
        'text':'Book Issues',
        'on_release':lambda x='ISSUE', y='Book Issues':self.search_by(x,y),
        },
        {
        'text':'Deleted',
        'on_release':lambda x='DELETED', y='Deleted':self.search_by(x,y),
        },
        {
        'text':'All',
        'on_release': lambda x='ALL', y='All':self.search_by(x,y),
        }
        ]
        self.options = MDDropdownMenu(items = self.items, caller=caller, position='bottom', theme_bg_color='Custom')
        self.options.open()

    def app_request(self, **kwargs):
        """
            Create a database object in main and pass it to here
        """
        self.history_database = kwargs.get('databases', None).get('history.db')
        #self.search(search=False)
        Clock.schedule_once(lambda x, y=False:self.search(search=y))
        #self.search(search=False)
        #print('Issue list', self.issue_data)
        if self.history_database is None:
            raise ValueError("No database object provided to users screen")
    
    def refresh(self, **kwargs):
        Clock.schedule_once(lambda x, y=False:self.search(search=y))

    def search(self, text='', search = True):
        if search:
            fetched = self.history_database.fetchall(f'SELECT * FROM history WHERE activity LIKE ?', (f'%{text}%',), show_error=True)
        else:
            cmd = f'SELECT * FROM history ORDER BY id DESC'
            fetched = self.history_database.fetchall(cmd)
        
        if isinstance(fetched, int):
            return
        self.user_data = []
        self.total = len(fetched)
 
        for row in fetched:
            row = dict(row)
        
            self.user_data.append(
                {
                    'viewclass': 'HistoryList',
                    'icon':str(self.icon_picker[row['activity_type']][0]),
                    'icon_color':str(self.icon_picker[row['activity_type']][1]),
                    'activity': str(row['activity']),
                    'date': str(row['hdate'])
                }
            )

    def catagorize(self, catagory='ALL'):
        if catagory == 'ALL':
            fetched = self.history_database.fetchall(f'SELECT * FROM history ORDER BY id DESC', show_error=True)

        else:
            fetched = self.history_database.fetchall(f'SELECT * FROM history WHERE activity_type=? ORDER BY id DESC', (catagory,), show_error=True)
        
        if isinstance(fetched, int):
            return
        self.user_data = []
        self.total = len(fetched)
 
        for row in fetched:
            row = dict(row)
        
            self.user_data.append(
                {
                    'viewclass': 'HistoryList',
                    'icon':str(self.icon_picker[row['activity_type']][0]),
                    'icon_color':str(self.icon_picker[row['activity_type']][1]),
                    'activity': str(row['activity']),
                    'date': str(row['hdate'])
                }
            )

    def search_by(self, hint, plate_text):
        print(hint, plate_text)
        self.ids.filter_plate.text = plate_text
        self.options.dismiss()
        self.catagorize(catagory=hint)
    
    def delete_all(self):
        self.confirmation = MDDialog(
            MDDialogHeadlineText(text='Permanently Delete All?', halign='left'),
            MDDialogSupportingText(text='Are you sure to delete all items permanently? This action cannot be undone.', halign='left'),
            MDDialogButtonContainer(
                Widget(size_hint_x=0.6),
                MDButton(
                    MDButtonText(text='Cancel'),
                    on_release=lambda dt:self.confirmation.dismiss(),
                    adaptive_size = True,
                    style = 'text'
                    ),
                MDButton(
                    MDButtonText(text='Delete'),
                    on_release=lambda x:self.confirm_delete(),
                    adaptive_size = True,
                    style = 'text'
                    ),
                spacing = 15
                )
            )
        self.confirmation.open()

    def confirm_delete(self):
        self.history_database.execute('DELETE FROM history')
        self.refresh(none = None)
