from models.book import BookModel
from book import Book as BookController
from controllers.core import UploadController

import urllib
from lib import utils


class Book(UploadController):
	r'/books/upload'
	
	# Associated Controller
	default_class = BookController
