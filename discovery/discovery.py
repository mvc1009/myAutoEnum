import requests
from controller.db import *
from discovery.modules import *

def find_domains(discovery_modules, scope_name, ip):
	print("")
	print_debug("Finding Domains of %s" % ip)
	results = set()

	# Modules
	if 'reverse_ip' in discovery_modules:
		print_status(' 	Reverse IP module (viewdns)')
		results.update(reverse_ip(ip))
	if 'read_certificate' in discovery_modules:
		print_status('	OpenSSL module')
		results.update(read_certificate(ip))
	parse_results(discovery_modules, scope_name, results)
	return results


def find_subdomains(discovery_modules, scope_name, domain_name):
	# Return Domain / Subdomain
	print("")
	print_debug("Finding Subdomains of %s" % domain_name)
	
	results = set()
	results.update("www.%s" % domain_name)
	
	# Modules
	if 'similar_certificate' in discovery_modules:
		print_status('	Similar Certificates module')
		results.update(similar_certificate(domain_name))
	if 'wayback_domains' in discovery_modules:
		print_status('	Wayback module')
		results.update(wayback_domains(domain_name))
	if 'fuzz_dns' in discovery_modules:
		print_status('	Fuzz DNS module')
		results.update(fuzz_dns(domain_name))
	if 'shodan_domain' in discovery_modules:
		print_status('	Shodan domain module')
		results.update(shodan_domain(domain_name))

	parse_results(discovery_modules, scope_name, results)
	return results

def parse_results(discovery_modules, scope_name, results):
	# Save Results 
	if results:
		print_status('	Parsing results')

		for r in results:
			if str_is_domain(r):
				new = new_domain(scope_name, r)
				if new:
					find_subdomains(discovery_modules, scope_name, r)

			elif str_is_subdomain(r):
				(dom, subdom) = new_subdomain(scope_name ,r)
				if dom:
					find_subdomains(discovery_modules, scope_name, dom.name)

def find_websites(subdomain_name):
	# Detecting Webpages in common ports
	print_debug("Finding websites in %s" % subdomain_name)
	proto_port = [
		("http", 80),
		("https", 443),
		("https", 4443),
		("http", 8000),
		("http", 8080),
		("https", 8443),
	]

	for pr in proto_port:
		try:
			url = "%s://%s:%s" % (pr[0], subdomain_name, str(pr[1]))
			r = requests.get(url, timeout=2)
			new_webpage(subdomain_name, url)
		except requests.exceptions.Timeout:
			print_error("	Timeout %s" % url)
		except:
			print_error("	Unable to connect to %s" % url)