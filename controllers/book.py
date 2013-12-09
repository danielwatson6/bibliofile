from controllers.core import BlobController
from models.book import BookModel

class Book(BlobController):
	r'/book'
	
	# Associated Model
	model = BookModel
	
	def new(self):
		data = self.get_data("errors", "blob_error")
		
		if data["errors"]:
			for i in data["errors"]:
				self.send_data(data={'error%s' % i: "This field is empty."})
		if data["blob_error"]:
			
			self.send_data(blob_error = data["blob_error"])
