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
		data = self.get_data("title",
		                     "blob",
		                     "author",
		                     "genre",
		                     "description",
		                     "author_description")
		
		if data["title"] and data["blob"] and data["author"] and data["genre"] \
		   and data["description"] and data["author_description"]:
			
			# HTML-Safe
			data["title"] = utils.escape(data["title"])
			data["author"] = utils.escape(data["author"])
			data["genre"] = utils.escape(data["genre"])
			data["description"] = utils.escape(data["description"])
			data["author_description"] = utils.escape(data["author_description"])
			return data
