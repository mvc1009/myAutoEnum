import requests

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
	return dns_names

