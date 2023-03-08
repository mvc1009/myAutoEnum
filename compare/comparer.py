
from src.dnslookuper import DNSLookuper
from controller.db import *

def compare_scope(ips, subdomain_names):
	# Mark is_scope from SubDomain object to True if the DNS resolution is in scope.
	# Usage of DNSLookuper
	for subdomain_name in subdomain_names:
		dnslook = DNSLookuper(domains=[subdomain_name])
		out = dnslook.resolve()
		if out[0]['IP'] in ips:
			mark_as_scope(subdomain_name)
			