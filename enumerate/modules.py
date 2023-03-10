import os
from src.dnslookuper import DNSLookuper
from controller.util import *
import requests

#
# ---------------------------
# Domain enum modules
# ---------------------------
#

def resolve(domain_name):
	# Resolve actual IP of domain_name
	# Usage of DNSLookuper
	dnslook = DNSLookuper(domains=[domain_name])
	out = dnslook.resolve()
	return out[0]['IP']

def ip_history(domain_name):
	# Return a list() of records {"IP" : ip, "location" : location, "owner": owner, "lastseen" : lastseen}
	# Usage of viewdns.info API.
	# API KEY is needed!
	results = list()
	if os.environ.get('VIEWDNS_API_KEY'):
		r = requests.get("https://api.viewdns.info/iphistory/?domain=%s&apikey=%s&output=json" % (domain_name, os.environ.get('VIEWDNS_API_KEY')), proxies=get_proxy())
		print(r.text)
		if (r.status_code == 200) and ('limit reached' not in r.text):
			r_json = r.json()
			if "error" in r_json['response'].keys():
				return list()
			return r.json()['response']['records']
		else:
			print_error("Problems with ViewDNS API key")
	else:
		print_error("No ViewDNS API key was provided!")
	return list()

#
# ---------------------------
# WebPage enum modules
# ---------------------------
#

def wayback_urls(subdomain_name):
	# Get a list of domain names from wayback machine.
	# Based on https://gist.github.com/mhmdiaa/adf6bff70142e5091792841d4b372050
	# No API KEY needed
	r = requests.get('http://web.archive.org/cdx/search/cdx?url=%s/*&output=json&fl=original&collapse=urlkey' % subdomain_name, proxies=get_proxy())
	urls = set()

	if r.status_code == 200:
		r_json = r.json()		
		if len(r_json) > 1:
			# Delete "original" from the list
			r_json.pop(0)
			for i in r_json:
				for url in i:
					# Filtering css,woff,jpeg,jpg,png and gif files.
					if ('.css' not in url) and ('.woff' not in url) and ('.jpeg' not in url) and ('.jpg' not in url) and ('.png' not in url) and ('.gif' not in url):
						print(url)
						urls.add(url)
	return urls


'''
https://shodan.readthedocs.io/en/latest/examples/query-summary.html

import shodan
sh = shodan.Shodan('APIKEY')
rjson  = sh.host('172.67.1.227')
rjson2 = sh.info()
'''