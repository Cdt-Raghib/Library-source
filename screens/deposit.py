from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty

#version: 2.0

class DepositMultiple(MDScreen):
    help = StringProperty()
    depo_info = StringProperty('Book name :---\nIssued by    :---')

    def deposit(self, numbers):
        print(f"Depositing multiple books: {numbers.text}")

    def search_in_issue(self, book_no):
        pass

class DepositSingle(MDScreen):
    help = StringProperty()
    depo_info = StringProperty('Book name :---\nIssued by    :---')

    def deposit(self, number):
        print(f"Depositing single book: {number.text}")
    
    def search_in_issue(self, book_no):
        pass


class DepositScreen(MDScreen):
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

Builder.load_file('kivymd/deposit.kv')

# class TestApp(MDApp):
#     def build(self):
#         self.md_bg_color = self.theme_cls.backgroundColor
#         self.theme_cls.primary_palette = 'Snow'
#         self.theme_cls.theme_style = 'Dark'
#         self.theme_cls.secondary_palette = 'Teal'
#         return Builder.load_file('kivymd/deposit.kv')

#     def on_start(self):
#         # Default to "Single" tab
#         print(self.root.ids.text1.text)
#         self.root.ids.tab.switch_tab(text=self.root.ids.text1.text)


# if __name__ == '__main__':
#     TestApp().run()