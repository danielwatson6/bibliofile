from book import Book as BookController
from controllers.core import UploadController

from lib import utils

class Book(UploadController):
	r'/books/upload'
	
	# Associated Controller
	default_class = BookController
	
	# On POST request
	def create(self):
		
		# Get all params from the html form
		data = self.get_data("title", "blob")
		
		if data["title"] and data["blob"]:
			
			# HTML-Safe
			data["title"] = utils.escape(data["title"])
			return data
