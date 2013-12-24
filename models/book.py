from lib import db, utils


BOOK_EXTENSIONS = ['azw', 'azw1', 'azw4', 'epub', 'kf8', 'mobi', 'pdb', 'pdf', 'prc', 'tpz']


# Book model
class BookModel(db.BlobModel):
	
	### Data
	
	# Main data
	title = db.string(required = True)
	
	author = db.string(required = True)
	submitter = db.string(default = "Unknown")
	genre = db.string(required = True)
	
	# Dates
	submitted_at = db.date(auto_now_add = True)
	last_edit_at = db.date(auto_now = True)
	
	# Descriptions
	description = db.text(required = True)
	author_description = db.text(required = True)
	
	# Other data
	book_img = db.string(default = 'javascript:void(0)')
	author_img = db.string(default = 'javascript:void(0)')
	
	blob_key = db.string(required = True, validator=lambda s: db.valid_blob_extension(s, BOOK_EXTENSIONS))
	
	
	### Functions
	
	# For rendering purposes
	def small_description(self, max_len = 300):
		try:
			return self.description[:max_len]
		except:
			return self.description
	
	# Size getter, but converts from bytes to human-readable size
	def get_size(self):
		return utils.file_size(self.size())
