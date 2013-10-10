from lib import db

# Book model
class BookModel(db.BlobModel):
	
	# Issue: add more data here
	title = db.string(required = True)
