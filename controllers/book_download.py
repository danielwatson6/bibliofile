from book import Book as BookController
from controllers.core import DownloadController

class Book(DownloadController):
	r'/books/serve/([^/]+)?'
	
	# Associated Controller
	default_class = BookController
