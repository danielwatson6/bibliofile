from controllers.core import BlobController
from models.book import BookModel

import logging
from lib.server import render_str

class Book(BlobController):
	r'/books'
	
	# Associated Model
	model = BookModel
	
	def show(self, *a):
		logging.info(render_str("book/show.html", **self._params))
