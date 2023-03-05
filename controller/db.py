import os,sys
from model.scope import Scope
from model.host import Host
from model.domain import Domain
from model.subdomain import SubDomain
from model.webpage import WebPage

#
# Scope class interaction
#

def add_scope(scope):
	try:	
		scope = Scope(name=scope)
		scope.save()
		print("	[+] Scope added: %s" % scope)
		return scope

	except:
		print("	[-] Err while adding %s to scope. Tried to save duplicate unique keys." % scope)
		sys.exit(0)

def add_host_to_scope(scope, host):
	# Append the given Host object to the given scope
	try:
		scope = Scope.objects(name=scope)[0]
		scope.hosts.append(host)
		scope.save()
	except:
		print("	[-] Scope not found")

#
# Host class interaction
#
def add_host(ip):
	# Add a new Host to the collection
	try:	
		host = Host(ip=ip)
		host.save()
		print("	[+] Host added: %s" % ip)
		return host
	except:
		print("	[-] Err while adding %s to hosts. Tried to save duplicate unique keys." % ip)
		sys.exit(0)




def check_host(ip):
	# Check if the IP exists on the collection
	results = Host.objects(ip=ip)
	return bool(results)

#
# Domain class interaction
#

def add_domain(domain):
	# Add a new domain to the collection
	try:	
		dom = Domain(name=domain)
		dom.save()
		print("	[+] Domain added: %s" % domain)
		return dom
	except:
		print("	[-] Err while adding %s to domains. Tried to save duplicate unique keys." % domain)
		sys.exit(0)

def add_subdomain_to_domain(domain, subdomain):
	# Add the object SubDomain() to a given domain name.
	try:	
		dom = Domain.objects(name=domain)[0]
		dom.subdomains.append(subdomain)
	except:
		print("	[-] Domain %s not found" % domain)
		sys.exit(0)

def check_domain(domain):
	# Check if a domain exists with a given domain name
	results = Domain.objects(name=domain)
	return bool(results)

def check_domain_from_subdomain(subdomain):
	# Check if a domain exists with a given subdomain name
	domain = '.'.join(subdomain.split('.')[-2:])
	results = Domain.objects(name=domain)
	return bool(results)


#
# SubDomain class interaction
#

def add_subdomain(subdomain):
	try:	
		sub = SubDomain(name=subdomain)
		sub.save()
		print("	[+] Subdomain added: %s" % subdomain)
		return sub

	except:
		print("	[-] Err while adding %s to Subdomains. Tried to save duplicate unique keys." % subdomain)
		sys.exit(0)

def check_subdomain(subdomain):
	results = SubDomain.objects(name=subdomain)
	return bool(results)