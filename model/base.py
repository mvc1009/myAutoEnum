import mongoengine as db
from datetime import datetime

CURRENT_SCHEMA = 0

class BaseDocument(db.Document):
	meta = {
		'abstract': True,
	}

	created_at = db.DateTimeField(default=datetime.utcnow)
	schema_version = {0,}
	_schema_version = db.IntField(default=CURRENT_SCHEMA, choices=schema_version)