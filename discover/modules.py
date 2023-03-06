import requests
from controller.util import *

def reverse_ip(ip):
	# Return a list of DNS names from a reverse DNS IP resolution.
	# Usage of viewdns.info API.
	# API KEY is needed!
	return list()

def similar_certificate(domain_name):
	# Return a set() of DNS names looking similar certificates from a domain.
	# Usage of crt.sh
	# No API KEY.
	r = requests.get('https://crt.sh/?q=%s&output=json' % domain_name)
	r_json = r.json()
	dns_names = set()
	# Parse Common Name
	for i in r_json:
		if '@' not in i['common_name'] and domain_name in i['common_name']:
			if '*' in i['common_name']:
				dns_names.add('.'.join(i['common_name'].split('.')[-2:]))
			else:
				dns_names.add(i['common_name'])
	# Parse Matching Identities
		data = i['name_value']
		for j in data.split():
			if '@' not in j and domain_name in j:
				if '*' in j:
					dns_names.add('.'.join(j.split('.')[-2:]))
				else:
					dns_names.add(j)
	print(dns_names)
	return dns_names

def get_subdomains_with_wayback(domain_name):
	r = requests.get('http://web.archive.org/cdx/search/cdx?url=*.%s/*&output=json&fl=original&collapse=urlkey' % domain_name)
	r_json = r.json()
	dns_names = set()

	# Delete "original" from the list
	r_json.pop(0)

	for i in r_json:
		for url in i:
			domain = str_get_domain_from_url(url)
			if domain and domain_name in domain:
				dns_names.add(domain)
	return dns_names