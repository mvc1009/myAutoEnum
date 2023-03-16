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

## Add SubDomain

```
s1 = SubDomain(name="www.example.com")
s1.save()
```


## Add WebPage

```
s1 = WebPage(url="http://www.example.com")
s1.save()
```

# Environ

dotenv is used, so create a `.env` file and add your api keys and your mongodb route.

Example of `.env`:

```
DB_URL="mongodb://localhost:27017/myautoenum"
PROXY = "socks5://localhost:xxxx"
GOWITNESS_BIN = "./src/gowitness-2.4.2-linux-amd64"
VIEWDNS_API_KEY_1 = "xxxxxxxxxxxxxxxxxxxx"
VIEWDNS_API_KEY_2 = "xxxxxxxxxxxxxxxxxxxx"
VIEWDNS_API_KEY_3 = "xxxxxxxxxxxxxxxxxxxx"
VIEWDNS_API_KEY_4 = "xxxxxxxxxxxxxxxxxxxx"
VIEWDNS_API_KEY_5 = "xxxxxxxxxxxxxxxxxxxx"
SHODAN_API_KEY_1 = "xxxxxxxxxxxxxxxxxxxx"
```

## API Key rotator

To avoid paying for some API keys I have implemented an API key rotator, which will detect if the provided free api key has reached its limit and will rotate to the next API key.

You can provide as many keys as possible, no limit is established. You only need to use the following name convention. Same for other API keys like shodan and more...

```
VIEWDNS_API_KEY_1 = "xxxxxxxxxxxxxxxxxxxx"
...
VIEWDNS_API_KEY_99999 = "xxxxxxxxxxxxxxxxxxxx"
```
# Gowitness integration

To use `gowitness` enumeration module we need to download the binary and set the following env variable.

```
GOWITNESS_BIN = "./src/gowitness-2.4.2-linux-amd64"
```
Gowitness have more dependencies such as google chrome and more. Check his page.

* [https://github.com/sensepost/gowitness/wiki/Installation](https://github.com/sensepost/gowitness/wiki/Installation)

It is recommended to download the last precomiled build from releases page.

Google chrome can ge downloaded and installed with the following commands:

```
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo apt-get update
sudo apt-get install google-chrome-stable
```

# To improve

* API Key rotator.
* Module Fuzzer
* Module find emails
* Implment some low hanging fruits