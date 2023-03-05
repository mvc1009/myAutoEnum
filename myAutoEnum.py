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
	try:	
		scope = Scope(name=args.name)
		scope.save()
		print("	[+] %s added to scope" % args.name)
	except:
		print("	[-] Err while adding %s to scope. Tried to save duplicate unique keys." % args.name)
		sys.exit(0)

	# IPs
	for ip in open(args.ip_file)
		try:	
			host = Host(ip=ip)
			host.save()
			print("	[+] %s added to hosts" % ip)
		except:
			print("	[-] Err while adding %s to Hosts. Tried to save duplicate unique keys." % ip)
			sys.exit(0)

	# Domains
	for domain in open(args.domain_file)
		try:	
			dom = Host(name=domain)
			dom.save()
			print("	[+] %s added to domains" % domain)
		except:
			print("	[-] Err while adding %s to Domains. Tried to save duplicate unique keys." % ip)
			sys.exit(0)

	# Subdomains

def main():
	
	# Initialize
	init()

	# Defining the scope
	print("[!] Defining the Scope")
	
		
	# Discovery
	print("[!] Starting Discovery")

	# Enum
	print("[!] Starting Enumeration")

	# Export
	print("[!] Starting Exports")
	
	# Exit
	print("[!] Finished")

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