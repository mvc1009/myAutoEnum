import os,sys
from model.scope import Scope
from model.host import Host
from model.domain import Domain
from model.subdomain import SubDomain
from model.webpage import WebPage
from controller.util import *

#
# ----------------------
# Scope class interaction
# ----------------------
#

def add_scope(scope_name):
	# Add a new scope to the collection
	try:	
		scope = Scope(name=scope_name)
		scope.save()
		print("	[+] Scope added: %s" % scope_name)
		return scope_name
	except:
		print("	[-] Err while adding %s to scope. Tried to save duplicate unique keys." % scope_name)
		sys.exit(0)

def add_host_to_scope(scope_name, host):
	# Append the given Host object to the given scope
	scope = Scope.objects(name=scope_name).first()
	if scope:
		scope.hosts.append(host)
		scope.save()

def add_domain_to_scope(scope_name, domain):
	# Append the given Doamin object to the given scope
	scope = Scope.objects(name=scope_name).first()
	if scope:
		scope.domains.append(domain)
		scope.save()

def get_scope(scope_name):
	# Get a Scope of the collection
	return Scope.objects(name=scope_name).first()
	
#
# ----------------------
# Host class interaction
# ----------------------
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

def get_host(ip):
	# Get a Host of the collection
	return Host.objects(ip=ip).first()

#
# ----------------------
#  Domain class interaction
# ----------------------
#

def add_domain(domain_name):
	# Add a new domain to the collection
	try:	
		dom = Domain(name=domain_name)
		dom.save()
		print("	[+] Domain added: %s" % domain_name)
		return dom
	except:
		print("	[-] Err while adding %s to domains. Tried to save duplicate unique keys." % domain_name)
		sys.exit(0)

def add_subdomain_to_domain(domain_name, subdomain):
	# Add the object SubDomain() to a given domain name.
	dom = Domain.objects(name=domain_name).first()
	if dom:
		dom.subdomains.append(subdomain)
		dom.save()
	
def check_domain(domain_name):
	# Check if a domain exists with a given domain name
	results = Domain.objects(name=domain_name)
	return bool(results)

def check_domain_from_subdomain(subdomain):
	# Check if a domain exists with a given subdomain name
	domain = str_domain_from_subdomain(subdomain)
	results = Domain.objects(name=domain)
	return bool(results)

def get_domain(domain_name):
	# Get a Domain from the collection
	return Domain.objects(name=domain_name).first()


#
# ----------------------
# SubDomain class interaction
# ----------------------
#

def add_subdomain(subdomain_name):
	# Add a new subdomain to the collection
	try:	
		subdomain = SubDomain(name=subdomain_name)
		subdomain.save()
		print("	[+] Subdomain added: %s" % subdomain_name)
		return subdomain

	except:
		print("	[-] Err while adding %s to Subdomains. Tried to save duplicate unique keys." % subdomain_name)
		sys.exit(0)

def check_subdomain(subdomain_name):
	# Check if a subdomain exists with a given subdomain name
	results = SubDomain.objects(name=subdomain_name)
	return bool(results)

def get_subdomain(subdomain_name):
	# Get a SubDomain from the collection
	return SubDomain.objects(name=subdomain_name).first()