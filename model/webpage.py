from model.base import *

class WebPage(BaseDocument):
	meta = {
		'collection': 'webpage_collection'
	}
	url = db.StringField(required=True, unique=True)
	title = db.StringField()
	screenshot = db.StringField() # ImagePath
	status = db.StringField()
	headers = db.ListField(db.DictField())
	tags = db.ListField(db.DictField())
	wayback = db.ListField(db.StringField())
	#addrs = db.ListField(db.StringField())