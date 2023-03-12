import json
from src.myCherryParser import myCherryParser
from controller.db import *

'''
# Cherry Tree output format
# Made with https://asciiflow.com/#/
#
# Scope
#   │
#   ├─► Host
#   │   │
#   │   └─► SubDomain
#   │
#   ├─► Domain
#   │
#   │
#   └─► Vulnerabilities
'''

def parse_scope(scope_name):
	
	scope_node = {
		"info_node" : {
			"node_name" : scope_name,
			"icon" : "redcherry",
			"bold" : True,
			"color" : "white"
		},
		"content_node" : [],
		"sub_node" : []
	}
	hosts_node = {
		"info_node" : {
			"node_name" : "Hosts",
			"icon" : "home",
			"bold" : True,
			"color" : "white"
		},
		"content_node" : [],
		"sub_node" : []
	}
	domains_node = {
		"info_node" : {
			"node_name" : "Domains",
			"icon" : "home",
			"bold" : True,
			"color" : "white"
		},
		"content_node" : [],
		"sub_node" : []
	}
	vulnerabilities_node = {
		"info_node" : {
			"node_name" : "Vulnerabilities",
			"icon" : "warning",
			"bold" : True,
			"color" : "red"
		},
		"content_node" : [],
		"sub_node" : []
	}

	rjson = scope_node
	rjson['sub_node'].append(hosts_node)
	rjson['sub_node'].append(domains_node)
	rjson['sub_node'].append(vulnerabilities_node)
	return rjson

def parse_host(ip):
	host = get_host(ip)
	rjson = {
		"info_node" : {
			"node_name" : ip,
			"icon" : "gray",
			"bold" : False,
			"color" : "white"
		},
		"content_node" : [],
		"sub_node" : []
	}

	title_host = {
		"type" : "text",
		"string" : "IP: %s" % ip,
		"style" : [
			"h1",
			"bold"
		]
	}
	if host.whois and host.whois != '' and host.whois != 'null':
		whois_title = {
			"type" : "text",
			"string" : "Whois",
			"style" : [
				"h2",
				"bold"
			]
		}

		rjson['content_node'].append(whois_title)

		whois_content = {

		}

	if host.shodan and host.shodan != '' and host.shodan != 'null':
		content = [
		{
			"type" : "text",
			"string" : "Shodan\n",
			"style" : [
				"h2",
				"bold"
			]
		},
		{
			"type" : "text",
			"string" : "Domains",
			"style" : [
				"bold"
			]
		},
		{
			"type" : "text",
			"string" : ", ".join(host.shodan['domains']) + "\n",
			"style" : []
		},
		{
			"type" : "text",
			"string" : "Hostnames",
			"style" : [
				"bold"
			]
		},
		{
			"type" : "text",
			"string" : ", ".join(host.shodan['hostnames']) + "\n",
			"style" : []
		},
		{
			"type" : "text",
			"string" : "ISP",
			"style" : [
				"bold"
			]
		},
		{
			"type" : "text",
			"string" : str(host.shodan['isp']) + "\n",
			"style" : []
		},
		{
			"type" : "text",
			"string" : "City/Region/Country",
			"style" : [
				"bold"
			]
		},
		{
			"type" : "text",
			"string" : str(host.shodan['city']) + " - " + str(host.shodan['region_code'])+ " - " + str(host.shodan['country_code']) +"\n",
			"style" : []
		},
		{
			"type" : "text",
			"string" : "Organization",
			"style" : [
				"bold"
			]
		},
		{
			"type" : "text",
			"string" : str(host.shodan['organization']) +"\n",
			"style" : []
		},
		{
			"type" : "text",
			"string" : "OS",
			"style" : [
				"bold"
			]
		},
		{
			"type" : "text",
			"string" : str(host.shodan['os']) +"\n",
			"style" : []
		},
		{
			"type" : "text",
			"string" : "Ports",
			"style" : [
				"bold"
			]
		},
		{
			"type" : "text",
			"string" : ', '.join([str(i) for i in sorted(host.shodan['ports'])])+"\n",
			"style" : []
		},
		{
			"type" : "text",
			"string" : "Tags",
			"style" : [
				"bold"
			]
		},
		{
			"type" : "text",
			"string" : ', '.join(host.shodan['tags'])+"\n",
			"style" : []
		},
		]
		rjson['content_node'] = rjson['content_node'] + content

	return rjson

def parse_domain(domain_name):
	rjson = {
		"info_node" : {
			"node_name" : domain_name,
			"icon" : "gray",
			"bold" : False,
			"color" : "white"
		},
		"content_node" : [],
		"sub_node" : []
	}
	return rjson

def parse_subdomain(subdomain_name):
	print()

def parse_webpage(url):
	print()

def export_json(results_json, filename):
	# save json to export with myCherryParser
	with open(filename, 'w') as outfile:
		json.dump(results_json, outfile)

def create_cherry(filename, outputfile):
	# Usage of myCherryParser
	print_status("Parsing: %s " % filename)
	parser = myCherryParser(filename, outputfile)
	parser.parse()
	print_good("Results saved in %s" % outputfile)