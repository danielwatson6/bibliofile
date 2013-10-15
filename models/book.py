from lib import db

# Book model
class BookModel(db.BlobModel):
	
	### Data
	
	# Main data
	title = db.string(required = True)
	author = db.string(default = "Unknown")
	submitter = db.string(default = "Anonymus")
	
	# Dates
	submitted = db.date(auto_now_add = True)
	last_edit = db.date(auto_now_add = True) #TODO: fix this
	
	# Descriptions
	description = db.text(default = '')
	info_description = db.text(default = '')
	author_description = db.text(default = '')
	
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
