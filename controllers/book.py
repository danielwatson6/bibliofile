from controllers.core import BlobController
from models.book import BookModel

class Book(BlobController):
	r'/books'
	
	# Associated Model
	model = BookModel
