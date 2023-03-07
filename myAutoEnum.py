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
from discover.discovery import *
from discover.modules import *

def init():
	try:
		# Connecting to the Database
		print_status("Connecting to the Database")
		db.connect(host='mongodb://localhost:27017/autoenum')
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


def discover():

	# Getting Domains/SubDomains from IPs
	ips = get_all_ips()
	for ip in ips:
		find_domains(ip)

	# Getting SubDomains from Domains
	domain_names = get_all_domain_names()
	for domain_name in domain_names:
		find_subdomains(args.name, domain_name)


def main():
	
	# Initialize
	init()

	# Defining the scope
	print("")
	print_status("Defining the Scope")
	print("----------------------")
	read_scope()
	
		
	# Discovery
	print("")
	print_status("Starting Discovery")
	print("----------------------")
	discover()

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
		global args
		args =  parser.parse_args()

		if len(sys.argv) < 2:
			parser.print_help()
			sys.exit(0)

		main()

except KeyboardInterrupt:
	print_error("Keyboard Interrupt. Shutting down")