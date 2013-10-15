from controllers.core import BlobController
from models.book import BookModel

class Book(BlobController):
	r'/book'
	
	# Associated Model
	model = BookModel
