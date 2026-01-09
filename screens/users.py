from kivymd.uix.button import MDButton,  MDButtonText
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog,\
MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer, MDDialogIcon
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDListItem
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.clock import Clock

Builder.load_file('kivymd/users.kv')

class UserList(MDListItem):
    icon = StringProperty('assets/img/nopic.png')
    name = StringProperty('')
    cadet_no = StringProperty('')
    batch = StringProperty('')
    joined = StringProperty('')
    role = StringProperty('')
    color = ListProperty([0,255,0])

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


class Users(MDScreen):
    user_database = None
    user_data = ListProperty([])
    searchby = StringProperty('cadet_name')
    total = NumericProperty()
    color_picker = {'Developer': [255,0,0], 'member': [255,255,255], 'Contributor':[34, 177, 76],
                    'Admin': [203, 46, 50]}

    def open_options(self, caller):
        self.items = [
        {
        'text':'Cadet name',
        'on_release':lambda x='cadet_name', y='Cadet name':self.search_by(x,y),
        },
        {
        'text':'Cadet no.',
        'on_release':lambda x='cadet_no', y='Cadet no.':self.search_by(x,y),
        }
        ]
        self.options = MDDropdownMenu(items = self.items, caller=caller, position='bottom', theme_bg_color='Custom')
        self.options.open()

    def app_request(self, **kwargs):
        """
            Create a database object in main and pass it to here
        """
        self.user_database = kwargs.get('databases', None).get('library.db')
        #self.search(search=False)
        Clock.schedule_once(lambda x, y=False:self.search(search=y))
        #self.search(search=False)
        #print('Issue list', self.issue_data)
        if self.user_database is None:
            raise ValueError("No database object provided to users screen")
    
    def refresh(self, **kwargs):
        Clock.schedule_once(lambda x, y=False:self.search(search=y))

    def search(self, text='', search = True):
        if search:
            fetched = self.user_database.fetchall(f'SELECT * FROM users WHERE {self.searchby} LIKE ?', (f'%{text}%',), show_error=True)
        else:
            cmd = '''
SELECT * FROM users ORDER BY 
    CASE role
        WHEN "Developer" THEN 1
        WHEN "Admin" THEN 2
        WHEN "Co-admin" THEN 3
        WHEN "Contributor" THEN 4
        WHEN "member" THEN 5
        ELSE 0
    END
'''
            fetched = self.user_database.fetchall(cmd)
        
        if isinstance(fetched, int):
            return
        self.user_data.clear()
        self.total = len(fetched)
        
        for row in fetched:
            row = dict(row)
        
            self.user_data.append(
                {
                    'viewclass': 'UserList',
                    'joined':str(row['joined']),
                    'batch':str(row['batch']),
                    'cadet_no': str(row['cadet_no']),
                    'name': str(row['cadet_name']) if row else 'Unknown',
                    'role': str(row['role']),
                    'color': self.color_picker[str(row['role'])],
                    'icon': "assets/img/profile1.png" if str(row['role']) == "Developer" else "assets/img/nopic.png"
                }
            )

    def search_by(self, hint, plate_text):
        print(hint, plate_text)
        self.searchby = hint
        self.ids.search_plate.text = plate_text
        self.options.dismiss()
