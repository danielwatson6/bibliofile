from lib import db, utils

import logging

BOOK_EXTENSIONS = ['azw', 'azw1', 'azw4', 'epub', 'kf8', 'mobi', 'pdb', 'pdf', 'prc', 'tpz']
IMG_EXTENSIONS = ['jpg', 'jpeg', 'gif', 'png']

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
	
	# Validate form
	@classmethod
	def invalid_form(cls, fields, blob):
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
				extension = filename.split('.')[-1]
				if not extension in BOOK_EXTENSIONS:
					blob_error = "Please select a file with a valid extension."
				else:
					blob_error = None
			except IndexError:
				blob_error = "The server has rejected this file."
		
		if not (errors == [] and not blob_error):
			error_str = str(errors)[1:-1].replace(' ','')
			return (error_str, blob_error)
	
	# For rendering purposes
	def small_description(self, max_len = 300):
		try:
			return self.description[:max_len]
		except:
			return self.description
	
	# Size getter, but converts from bytes to human-readable size
	def get_size(self):
		return utils.file_size(self.size())
