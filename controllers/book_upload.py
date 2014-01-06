from models.book import BookModel
from book import Book as BookController
from controllers.core import UploadController

import urllib
from lib import utils


class Book(UploadController):
	r'/books/upload'
	
	# Associated Controller
	default_class = BookController
	
	# On POST request
	def create(self):
		
		# Get all params from the html form
		data = self.get_data("title",
		                     "author",
		                     "genre",
		                     "description",
		                     "author_description",
		                     "blob")
		
		fields = [(BookModel.title, data["title"]),
				  (BookModel.author, data["author"]),
				  (BookModel.genre, data["genre"]),
				  (BookModel.description, data["description"]),
				  (BookModel.author_description, data["author_description"]),
				  (BookModel.blob_key, data["blob"])]
		
		# TO-DO!!!
		valid_form = True
		
		if valid_form:
			# HTML-safe
			for key in data:
				data[key] = utils.escape(data[key])
			return data
