from src.dnslookuper import DNSLookuper
from controller.db import *
from enumerate.modules import *


def enum_domains(enum_modules, domain_name):
	print("")
	print_debug("Enumerating domain %s" % domain_name)
	
	# Modules
	print_status('	Resolving DNS address')
	ip = resolve(domain_name)
	set_ip(domain_name, ip)

	if 'ip_history' in enum_modules:
		print_status('	IP History module')
		ip_history_results = ip_history(domain_name)
		print(ip_history_results)
		set_ip_history(domain_name, ip_history_results)

def enum_subdomains(enum_modules, subdomain_name):
	print("")
	print_debug("Enumerating subdomain %s" % subdomain_name)

	# Modules
	if 'wayback_urls' in enum_modules:
		print_status('	Wayback URLS module')
		urls = wayback_urls(subdomain_name)

