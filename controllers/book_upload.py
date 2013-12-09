from models.book import BookModel
from book import Book as BookController
from controllers.core import UploadController

import urllib
from lib import utils


class Book(UploadController):
	r'/books/upload'
	
	# Associated Controller
	default_class = BookController
	
	# Custom actions in create() failure
	controls_create_fail = True
	
	# On POST request
	def create(self):
		
		# Get all params from the html form
		data = self.get_data("title",
		                     "blob",
		                     "author",
		                     "genre",
		                     "description",
		                     "author_description")
		
		fields = [data["title"], data["author"], data["genre"],
				  data["description"], data["author_description"]]
		
		invalid_form = BookModel.invalid_form(fields, data["blob"])
		
		if not invalid_form:
			for f in fields:
				f = utils.escape(f) # HTML-Safe
			return data
		else:
			self.redirect('/books/new')
	
	

