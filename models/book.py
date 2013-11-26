from lib import db, utils

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
	last_edited_at = db.date(auto_now_add = True) #TODO: fix this
	
	# Descriptions
	description = db.text(required = True)
	author_description = db.text(required = True)
	
	# Other data
	book_img = db.string(default = 'javascript:void(0)')
	author_img = db.string(default = 'javascript:void(0)')
	
	
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
