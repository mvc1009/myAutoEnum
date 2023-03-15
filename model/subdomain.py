from model.base import *

class SubDomain(BaseDocument):
	meta = {
	'collection': 'subdomain_collection'
	}
	name = db.StringField(required=True, unique=True)
	ip = db.StringField()
	pages = db.ListField(db.ReferenceField("WebPage"))
	ip_history = db.ListField(db.DictField())
	is_scope = db.BooleanField(default=False)
	#wayback = db.ListField(db.StringField())