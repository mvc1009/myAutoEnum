import requests
import os
import ssl
import OpenSSL
import socket
import sys
from concurrent import futures
from src.dnslookuper import DNSLookuper
from controller.util import *

#
# ------------------------
# Domain discovery modules
# ------------------------
#

def reverse_ip(ip):
	# Return a list of DNS names from a reverse DNS IP resolution.
	# Usage of viewdns.info API.
	# API KEY is needed!
	results = set()
	if os.environ.get('VIEWDNS_API_KEY'):
		r = requests.get('https://api.viewdns.info/reverseip/?host=%s&apikey=%s&output=json' % (ip, os.environ.get('VIEWDNS_API_KEY')))
		if r.status_code == 200:
			print(r_json)
			if int(r_json['response']['domain_count']) > 0:		
				for name in r_json['response']['domains']:
					results.add(name['name'])
	else:
		print_error("No ViewDNS API key was provided!")
	return results


def read_subject_from_certificate(domain_name, port):
	# Read Subject from server certificate and obtain a DNS name
	# Usage of OpenSSL
	# No API KEY.
	socket.setdefaulttimeout(2)
	dns_names = set()
	try:
		cert = ssl.get_server_certificate((domain_name, port))
		x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
		for i in x509.get_subject().get_components():
			if i[0] == b"CN":
				dns_names.add(i[1].decode())
		print_debug("	OpenSSL %s:%s" % (domain_name, str(port)))
		return dns_names
	except socket.timeout:
		print_error("	Timeout %s:%s" % (domain_name, str(port)))
		return None
	except :
		return None

def read_certificate(ip):
	# Check certificates from a lot of ports and get a list of domain names
	# Usage of OpenSSL
	# No API KEY.
	PORTS = [443,8443,4443,5000,5443,6443,7443,9443]
	dns_names = set()
	for port in PORTS:
		subject = read_subject_from_certificate(ip, port)
		if subject:
			if '*.' in subject:
				dns_names.update('.'.join(subject.split('.')[1:]))
			else:
				dns_names.update(subject)
	return dns_names

#
# ---------------------------
# SubDomain discovery modules
# ---------------------------
#


def similar_certificate(domain_name):
	# Return a set() of DNS names looking similar certificates from a domain.
	# Usage of crt.sh
	# No API KEY needed.
	r = requests.get('https://crt.sh/?q=%s&output=json' % domain_name)
	dns_names = set()
	if r.status_code == 200:
		r_json = r.json()
		# Parse Common Name
		for i in r_json:
			if '@' not in i['common_name'] and domain_name in i['common_name']:
				if '*.' in i['common_name']:
					dns_names.add('.'.join(i['common_name'].split('.')[1:]))
				else:
					dns_names.add(i['common_name'])
		# Parse Matching Identities
			data = i['name_value']
			for j in data.split():
				if '@' not in j and domain_name in j:
					if '*.' in j:
						dns_names.add('.'.join(j.split('.')[1:]))
					else:
						dns_names.add(j)
	return dns_names


def wayback_domains(domain_name):
	# Get a list of domain names from wayback machine.
	# Based on https://gist.github.com/mhmdiaa/adf6bff70142e5091792841d4b372050
	# No API KEY needed
	r = requests.get('http://web.archive.org/cdx/search/cdx?url=*.%s/*&output=json&fl=original&collapse=urlkey' % domain_name)
	dns_names = set()

	if r.status_code == 200:
		r_json = r.json()		
		if len(r_json) > 1:
			# Delete "original" from the list
			r_json.pop(0)

			for i in r_json:
				for url in i:
					domain = str_get_domain_from_url(url)
					if domain and domain_name in domain:
						dns_names.add(domain)
	return dns_names

def fuzz_dns(domain_name, dictfile='./src/dns-test.txt'):
	# Return a set() of subdomains doing bruteforcing A queries. 
	# Based on https://github.com/mvc1009/DNSLookuper
	# No API KEY needed.
	# dictfile='./src/subdomains-top1mil-5000.txt'
	results = set()
	fuzz = list()

	if os.path.isfile(dictfile):
		with open(dictfile) as fd:
			fuzz = [f"{sub.rstrip()}.{domain_name}" for sub in fd]
		dnslook = DNSLookuper(domains=fuzz)
		lookup = dnslook.resolve()
		for l in lookup:
			if l['IP'] != 'None':
				results.add(l['DNS'])

	return results