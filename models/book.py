from lib import db

# Book model
class BookModel(db.BlobModel):
	
	# Issue: add more data here
	title = db.string(required = True)
	description = db.text(default = '')
	
	def small_description(self, max_len = 30):
		try:
			return self.description[:max_len]
		except:
			return self.description
