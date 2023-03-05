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
		add_host(args.name, ip.rstrip())

	# Domains
	for domain in open(args.domain_file):
		add_domain(domain.rstrip())

	# Subdomains
	for subdomain in open(args.subdomain_file):
		if not check_domain_from_subdomain(subdomain.rstrip()):
			add_domain(str_domain_from_subdomain(subdomain.rstrip()))
		add_subdomain(subdomain.rstrip())

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