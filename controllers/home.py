from controllers.core import Controller

class Home(Controller):
	r'/'
	
	# For now, on GET request it will redirect
	# since the index page is useless
	def index(self, *a):
		self.redirect('/books')
