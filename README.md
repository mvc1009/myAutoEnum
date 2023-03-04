# myAutoEnum

Enumeration software that automatize tasks that I usually do while enumerating in a new pentest.

MongoDb is used

pip:

```
mongoengine
```

# Debug with iPython

Useful commands:

##  Connect to the database and load the models
```
import os,sys
import mongoengine as db
from model.scope import Scope
from model.host import Host
from model.domain import Domain
from model.subdomain import SubDomain
from model.webpage import WebPage

db.connect(host='mongodb://localhost:27017/autoenum')
```

## Add Scope

```
s1 = Scope(name="pentest")
s1.save()
```

## Add Domain

```
s1 = Domain(name="example.com")
s1.save()
```