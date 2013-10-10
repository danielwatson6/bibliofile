from controllers.core import Controller

class Home(Controller):
	r'/'
	
	def index(self):
		self.redirect('/books')
