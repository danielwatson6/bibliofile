from controllers.core import Controller

class Home(Controller):
	r'/'
	
	# For now, on GET request it will redirect
	# since the index page is useless
	def index(self):
		self.redirect('/books')
