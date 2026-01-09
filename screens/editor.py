from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivy.properties import StringProperty, ListProperty, ObjectProperty

Builder.load_file('kivymd/editor/editor.kv')

class EditorField(MDTextField):
	column = StringProperty('') 
	main_field = ObjectProperty({})

	def update(self, text):
		for f in self.main_field:
			if f['column'] == self.column:
				f['text'] = text
				break

class Editor(MDScreen):
	fields = ListProperty([])
	database = None
	all_info = None
	primary_key = None
	primary_value = None

	def refresh(self, **kwargs):
		pass

	def app_request(self, **kwargs):
		self.main = kwargs['main']

	def check(self, find, array):
		if array is None:
			return False
		return find in array

	def move_to_edit(self, primary_key, param:dict, **kwargs):
		"""
		param:
			which row to edit..
		"""
		self.primary_key = primary_key
		self.database = kwargs['database']
		self.all_info = kwargs
		self.trace = self.manager.current
		data = dict(self.database.fetchone(f'SELECT * FROM {kwargs['table']} WHERE {list(param.keys())[0]}={list(param.values())[0]}'))
		
		for k,v in data.items():
			if k==primary_key:
				self.primary_value = v
			self.fields.append({
				'column': k,
				'text': str(v),
				'multiline': self.check(k, kwargs.get('multilines')),
				'disabled': self.check(k, kwargs.get('disabled')) or k==primary_key,
				'readonly': self.check(k, kwargs.get('readonly')),
				'main_field': self.fields
				})

		self.manager.current = 'editor'

	def save(self):
		for f in self.fields:
			self.database.execute(f'UPDATE {self.all_info['table']} SET {f['column']}=? WHERE {self.primary_key}=?', (f['text'], self.primary_value))

		self.manager.current = self.trace


