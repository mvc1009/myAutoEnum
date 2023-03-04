# myAutoEnum

Enumeration software that automatize tasks that I usually do while enumerating in a new pentest.

MongoDb

pip:

```
mongoengine
pymongo
jinja2
```

# Debug with iPython

Useful commands:

* Connect to the database and load the models
```
import os,sys
import mongoengine as db
from model.scope import *

db.connect(host='mongodb://localhost:27017/autoenum')
```
