import os,sys

from model.scope import Scope
from model.host import Host
from model.domain import Domain
from model.subdomain import SubDomain
from model.webpage import WebPage
from controller.db import *
from controller.util import *
from discovery.discovery import *
from discovery.modules import *

try:
	import argparse
except:
	print_error('argparse is not installed. Try "pip install argparse"')
	sys.exit(0)

try:
	import mongoengine as db
except:
	print_error('mongoengine is not installed. Try "pip install mongoengine"')
	sys.exit(0)
try:
	from dotenv import load_dotenv
except:
	print_error('python-dotenv is not installed. Try "pip install python-dotenv"')



def init():
	try:
		# Loading .env variables
		load_dotenv()
		# Connecting to the Database
		print_status("Connecting to the Database")
		db.connect(host=os.environ.get("DB_URL"))
	except:
		print_error("Err while connecting to mongodb")
		sys.exit(0)


def read_scope():

	# Scope
	new_scope(args.name)

	# IPs
	for ip in open(args.ip_file):
		new_host(args.name, ip.rstrip())

	# Domains
	for domain_name in open(args.domain_file):
		new_domain(args.name, domain_name.rstrip())

	# Subdomains
	for subdomain_name in open(args.subdomain_file):
		new_subdomain(args.name, subdomain_name.rstrip())


def discover(discovery_modules):

	# Getting Domains/SubDomains from IPs
	ips = get_all_ips()
	for ip in ips:
		find_domains(discovery_modules, args.name, ip)

	# Getting SubDomains from Domains
	domain_names = get_all_domain_names()
	for domain_name in domain_names:
		find_subdomains(discovery_modules, args.name, domain_name)


def main():
	
	# Initialize
	init()

	
	discovery_modules = [
		'reverse_ip',
		#'similar_certificate',
		#'read_certificate',
		#'wayback_domains',
		#'fuzz_dns'
	]
	
	#discovery_modules = ['fuzz_dns']

	enum_modules = [
		'ip_history',
		'wayback_urls',
		'gowitness',
		'dnslookup',
		'get_emails',
		'subdomain_takeover'
	]

	# Defining the scope
	print("")
	print_status("Defining the Scope")
	print("----------------------")
	read_scope()
	
		
	# Discovery
	print("")
	print_status("Starting Discovery")
	print("----------------------")
	discover(discovery_modules)

	# Enum
	#print("")
	#print("[!] Starting Enumeration")
	#print("----------------------")
	
	# Export
	#print("")
	#print("[!] Starting Exports")
	#print("----------------------")

	# Exit
	#print("")
	print("----------------------")
	print_status("Finished")

try:
	if __name__ == "__main__":
		parser = argparse.ArgumentParser(description='myAutoEnum is a tool that automate some task when a new pentest is started.')
		parser.add_argument('-n', '--name', action='store', dest='name', help='Name of the pentest', type=str, required=True)
		parser.add_argument('-i', '--ips', action='store', dest='ip_file', help='File with IPs list', type=str)
		parser.add_argument('-d', '--domains', action='store', dest='domain_file', help='File with Domains list', type=str)
		parser.add_argument('-s', '--subdomains', action='store', dest='subdomain_file', help='File with SubDomains list', type=str)
		parser.add_argument('-m', '--modules', action='store', dest='modules', help='Modules to use: reverse_ip,similar_certificate,read_certificate,wayback_domains,fuzz_dns,ip_history,wayback_urls', type=str)
		parser.add_argument('-p', '--proxy', action='store', dest='proxy', help='Proxy to use. ej: socks5://localhost:9080', type=str)
		global args
		args =  parser.parse_args()

		if len(sys.argv) < 2:
			parser.print_help()
			sys.exit(0)

		main()

except KeyboardInterrupt:
	print_error("Keyboard Interrupt. Shutting down")