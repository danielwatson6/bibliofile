from lib import db

class BookModel(db.BlobModel):
	title = db.string(required = True)
