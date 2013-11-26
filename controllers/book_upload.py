from book import Book as BookController
from controllers.core import UploadController

import urllib
from lib import utils


BOOK_EXTENSIONS = ['azw', 'azw1', 'azw4', 'epub', 'kf8', 'mobi', 'pdb', 'pdf', 'prc', 'tpz']
IMG_EXTENSIONS = ['jpg', 'jpeg', 'gif', 'png']

class Book(UploadController):
	r'/books/upload'
	
	# Associated Controller
	default_class = BookController
	
	# Custom actions in create() failure
	controls_create_fail = True
	
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
				  data["description"], data["author_description"]]
		
		invalid_form = self.invalid_form(fields, data["blob"])
		
		if not invalid_form:
			for f in fields:
				f = utils.escape(f) # HTML-Safe
			return data
		else:
			bounce_url = urllib.urlencode({"errors": invalid_form[0],
			                               "blob_error": invalid_form[1]})
			self.redirect('/books/new?' + bounce_url)
	
	# Validate form
	def invalid_form(self, fields, blob):
		errors = []
		blob_error = "This field is empty."
		
		# All fields must have some content
		n = 0
		for i in fields:
			if not i or str(i) == '':
				errors.append(n)
			n += 1
		
		# Blob extension
		if blob:
			try:
				filename = blob.split('filename="')[1]
				filename = filename.split('"')[0]
				if not filename.split('.')[-1] in BOOK_EXTENSIONS:
					blob_error = "Please select a file with a valid extension."
			except IndexError:
				blob_error = "The server has rejected this file."
		
		if not (errors == [] and not blob_error):
			error_str = str(errors)[1:-1].replace(' ','')
			return (error_str, blob_error)

