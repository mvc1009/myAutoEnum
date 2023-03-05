import os,sys

try:
	import argparse
except:
	print('[!] argparse is not installed. Try "pip install argparse"')
	sys.exit(0)

try:
	import mongoengine as db
except:
	print('[!] mongoengine is not installed. Try "pip install mongoengine"')
	sys.exit(0)

from model.scope import Scope
from model.host import Host
from model.domain import Domain
from model.subdomain import SubDomain
from model.webpage import WebPage
from controller.db import *
from controller.util import *

def init():
	try:
		# Connecting to the Database
		print("[!] Connecting to the Database")
		db.connect(host='mongodb://localhost:27017/autoenum')
	except:
		print("[-] Err while connecting to mongodb")
		sys.exit(0)

def read_scope():

	# Scope
	add_scope(args.name)

	# IPs
	for ip in open(args.ip_file):
		host = add_host(ip.rstrip())
		add_host_to_scope(args.name, host)

	# Domains
	for domain_name in open(args.domain_file):
		domain = add_domain(domain_name.rstrip())
		add_domain_to_scope(args.name, domain)

	# Subdomains
	for subdomain_name in open(args.subdomain_file):
		subdomain = add_subdomain(subdomain_name.rstrip())
		domain_name = str_domain_from_subdomain(subdomain_name.rstrip())
		domain = get_domain(domain_name)
		if domain:
			add_subdomain_to_domain(domain_name, subdomain)
		else:
			new_domain = add_domain(domain_name)
			add_subdomain_to_domain(domain_name, subdomain)

def main():
	
	# Initialize
	init()

	# Defining the scope
	print("[!] Defining the Scope")
	read_scope()
	
		
	# Discovery
	#print("[!] Starting Discovery")

	# Enum
	#print("[!] Starting Enumeration")

	# Export
	#print("[!] Starting Exports")
	
	# Exit
	print("[+] Finished")

try:
	if __name__ == "__main__":
		parser = argparse.ArgumentParser(description='myAutoEnum is a tool that automate some task when a new pentest is started.')
		parser.add_argument('-n', '--name', action='store', dest='name', help='Name of the pentest', type=str, required=True)
		parser.add_argument('-i', '--ips', action='store', dest='ip_file', help='File with IPs list', type=str)
		parser.add_argument('-d', '--domains', action='store', dest='domain_file', help='File with Domains list', type=str)
		parser.add_argument('-s', '--subdomains', action='store', dest='subdomain_file', help='File with SubDomains list', type=str)
		global args
		args =  parser.parse_args()

		if len(sys.argv) < 2:
			parser.print_help()
			sys.exit(0)

		main()

except KeyboardInterrupt:
	print("[!] Keyboard Interrupt. Shutting down")