from model.base import *
from model.subdomain import SubDomain

class Domain(BaseDocument):
	meta = {
	'collection': 'domain_collection'
	}
	name = db.StringField(required=True, unique=True)
	subdomains = db.ListField(db.ReferenceField("SubDomain"))

