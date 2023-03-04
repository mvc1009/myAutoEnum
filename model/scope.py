from model.base import *

class Scope(BaseDocument):
	meta = {
	'collection': 'scope_collection'
	}
	name = db.StringField(required=True, unique=True)
	hosts = db.ListField(db.ReferenceField("Host"))