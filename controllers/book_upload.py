from book import Book as BookController
from controllers.core import UploadController

from lib import utils


BOOK_EXTENSIONS = ['azw', 'azw1', 'azw4', 'epub', 'kf8', 'mobi', 'pdb', 'pdf', 'prc', 'tpz']
IMG_EXTENSIONS = ['jpg', 'jpeg', 'gif', 'png']

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
		
		fields = [data["title"], data["author"], data["genre"],
				  data["description"], data["author_description"],
				  data["blob"]]
		
		if self.validate(fields, data["blob"]):
			for f in fields:
				f = utils.escape(f) # HTML-Safe
			return data
	
	# Validate form
	def validate(self, fields, blob):
		for i in fields:
			if not i: return
		try:
			return blob.split('.')[-1] in BOOK_EXTENSIONS
		except IndexError: return
	
