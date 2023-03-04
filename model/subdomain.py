from model.base import *

class SubDomain(BaseDocument):
	meta = {
	'collection': 'subdomain_collection'
	}
	name = db.StringField(required=True, unique=True)
	ip = db.StringField()
	ip_history = db.ListField(db.StringField())
	pages = db.ListField(db.ReferenceField("WebPage"))