from book import Book as BookController
from controllers.core import UploadController

class Book(UploadController):
	r'/books/upload'
	
	# Associated Controller
	default_class = BookController
	
	def create(self):
		data = self.get_data("title", "blob")
		if data["title"] and data["blob"]:
			return data
