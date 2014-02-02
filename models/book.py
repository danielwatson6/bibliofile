from lib import db, utils
from lib.db import validators

BOOK_EXTENSIONS = ['azw', 'azw1', 'azw4', 'epub', 'kf8', 'mobi', 'pdb', 'pdf', 'prc', 'tpz']


class BookModel(db.BlobModel):
	
	### Data:
	
	title = db.string(required = True)
	author = db.string(required = True)
	genre = db.string(required = True)
	submitted_at = db.date(auto_now_add = True)
	last_edit_at = db.date(auto_now = True)
	description = db.text()
	author_description = db.text()
	blob = db.string(required = True)
	
	
	### Form:
	
	form = {
		"title": [validators.required(message="title error")],
		"author": [validators.required(message="author error")],
		"genre": [validators.required(message="genre error")],
		"description": [validators.length(0, 500)],
		"author_description": [validators.length(0, 500)],
		
		# TO-DO: Add blob_extension validator
		"blob": [validators.required(message="blob error")],
	}
	
	
	### Functions used by templates:
	
	def small_description(self, max_len = 300):
		"""Return a reduced size of the description. Used in templates."""
		if len(self.description) <= max_len:
			return self.description
		return self.description[:max_len]
	
	def get_size(self):
		"""Size getter, but converts from bytes to human-readable size."""
		return utils.file_size(self.size())

