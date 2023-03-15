#!/usr/bin/env python3

#
#
#	This tools is made for educational purpose!
#	A bad usage of this tool is not allowed...
#
# _____  _______ _______ _____                __                
#|     \|    |  |     __|     |_.-----.-----.|  |--.--.--.-----.-----.----.
#|  --  |       |__     |       |  _  |  _  ||    <|  |  |  _  |  -__|   _|
#|_____/|__|____|_______|_______|_____|_____||__|__|_____|   __|_____|__|  
#                                                        |__|  
#
#


#Imports
import sys, os
try:
	import dns.resolver
except:
	print('[!] dnspython is not installed. Try "pip install dnspython"')
	sys.exit(0)
try:
	import argparse
except:
	print('[!] argparse is not installed. Try "pip install argparse"')
	sys.exit(0)
try:
	import json
except:
	print('[!] json is not installed. Try "pip install json"')
	sys.exit(0)
try:
	import csv
except:
	print('[!] cvs is not installed. Try "pip install csv"')

import requests


#COLOR CODES
BLACK = '\u001b[30m'
RED = '\u001b[31m'
GREEN = '\u001b[32m'
YELLOW = '\u001b[33m'
BLUE = '\u001b[34m'
MAGENTA = '\u001b[35m'
CYAN = '\u001b[36m'
WHITE = '\u001b[37m'
RESET = '\u001b[0m'


# Display DNSLookuper Banner
def banner():
	print('\n\n')
	print(' _____  _______ _______ _____                __                	')
	print('|     \|    |  |     __|     |_.-----.-----.|  |--.--.--.-----.-----.----.')
	print('|  --  |       |__     |       |  _  |  _  ||    <|  |  |  _  |  -__|   _|')
	print('|_____/|__|____|_______|_______|_____|_____||__|__|_____|   __|_____|__|  ')
	print('                                                        |__|  ')
	print("\t\t\t\t\t\t\t\tVersion 1.1")
	print("\t\t\t\t\t\t\t\tBy: @mvc1009")
	print('\n\n')

def readFile(file):
	try:
		with open(file, 'r') as f:
			return f.read().split()
	except:
		print("[!] File not found")
		sys.exit(0)

class DNSLookuper():

	domains = None
	input_file = None
	results = None
	compared_results = None
	server = None
	scope = None
	verbose = None
	color = None
	history_results = None
	viewdns_api_key = None

	
	def __init__(self, domains=None, input_file=None, server="8.8.8.8", verbose=False, color=False):
		self.domains = list()
		self.history_results = list()
		self.results = list()
		self.compared_results = list()
		self.scope = list()

		if domains:
			self.domains = domains

		self.verbose = verbose
		self.color = color
		self.server = server
		self.input_file = input_file
		if self.input_file:
			self.domains = self.domains + readFile(input_file)


	def __repr__(self):
		return "<%s %s at %#x>" % (self.__class__.__name__, self.server, id(self))

	def dns_query(self, query):
		# Return a list of DNS resolutions and the answer itself 
		my_resolver = dns.resolver.Resolver()
		my_resolver.nameservers = [self.server]
		datas = list()
		try:
			answer = my_resolver.query(query)
			if answer:
				for data in answer:
					datas.append(data)
				return datas, str(answer)
			return ['None'], 'None'
		except:
			return ['None'], 'None'
	
	def export(self, filename, fileformat):
		if self.verbose:
			if self.color:
				print(RED + '[+] Exporting results to: ' + RESET + filename)
			else:
				print('[+] Exporting results to: ' + filename)
		
		# CSV
		if fileformat == 'csv':
			with open(filename, mode="w+") as csv_file:
				fieldnames = ['DNS', 'IP']
				writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
				writer.writeheader()
				for i in self.results:
					writer.writerow(i)
			return None
		
		# JSON
		elif fileformat == 'json':
			with open(filename, mode="w+") as json_file:
				out = {
					'server' : self.server,
					'results' : self.results,
					'history_results' : self.history_results,
					'scope' : self.scope,
					'compared_results' : self.compared_results
				}
				json.dump(out, json_file)
			return out


	def resolve(self, domains=None):
		if self.verbose:
			if self.color:
				print(RED + '[!] Start resolving DNS queries' + RESET)
				print(BLUE + '[+] DNS Server' + RESET + ': %s' % self.server)
			else:
				print('[!] Start resolving DNS queries')
				print('[+] DNS Server: %s' % self.server)
		
		# Making DNS resolutions for all domains
		
		if domains:
			list_domains = domains
		else:
			list_domains = self.domains
		
		results = list()
		
		for query in list_domains:
			response_list, answers = self.dns_query(query)
			if response_list:
				for response in response_list:
					if response != None:
						if self.verbose:
							if self.color:
								print(BLUE + '[+] Query to resolve: ' + YELLOW + query + RESET)
								print('\t' + YELLOW + query + RESET + ' -> ' + GREEN + str(response) + RESET)
							else:
								print('[+] Query to resolve: ' + query)
								print('\t' + query + ' -> ' + str(response))
						else:
							if self.color:
								print(YELLOW + query + RESET + ' -> ' + GREEN + str(response) + RESET)		
							else:
								print(query + ' -> ' + str(response))
						results.append({'IP':str(response),'DNS':query})
			
					else:
						if self.verbose:
							if self.color:
								print(BLUE + '[+] Query to resolve: ' + YELLOW + query + RESET)
							else:
								print('[+] Query to resolve: ' + query)
							print('\t No response for this query')
						else:
							if self.color:
								print(YELLOW + query + RESET + ' -> ' + GREEN + str(response) + RESET)		
							else:
								print(query + ' -> ' + str(response))
		self.results += results
		return results

	def compare(self, scope):
		# Compare the results with a list of IPs
		if self.verbose:
			if self.color:
				print(RED + "[!] Comparing Results" + RESET)
			else:
				print("[!] Comparing Results")
		with open(scope, 'r') as f:
			data = f.read().split('\n')
			results = list()
			for row in data:
				if row:
					self.scope.append(row)
					if self.verbose:
						if self.color:
							print(BLUE + '[+] IP: ' + RESET + row )
						else:
							print('[+] IP: ' + row)
					r = {"IP" : row, "DNS" : []}
					for row2 in self.results:
						if row2['IP'] == row:
							if self.verbose:
								if self.color:
									print(YELLOW + row2['DNS'] + RESET)
								else:
									print(row2['DNS'])
								r["DNS"].append(row2['DNS'])
					results.append(r)
		self.compared_results = results
	
	
	def viewdns(self, domain, viewdns_api_key):
		if self.verbose:
			if self.color:
				print(YELLOW + "[+] Querying ViewDNS" + RESET)
			else:
				print("[+] Querying ViewDNS")
		r = requests.get("https://api.viewdns.info/iphistory/?domain=%s&apikey=%s&output=json" % (domain, viewdns_api_key), verify=False)
		if self.verbose:
			print(r.json())
		if "error" in r.json()['response'].keys():
			return list()
		return r.json()['response']['records']

	def history(self, viewdns_api_key):
		if self.verbose:
			if self.color:
				print(RED + "[!] Searching History of IPs" + RESET)
			else:
				print("[!] Searching History of IPs")
		for i in self.results:
			if self.verbose:
				if self.color:
					print(GREEN + i['DNS'] + RESET)
				else:
					print(i['DNS'])
			self.history_results.append({"domain" : i['DNS'], "history" : self.viewdns(i['DNS'], viewdns_api_key)})

try:
	if __name__ == "__main__":

		# Parsing arguments
		parser = argparse.ArgumentParser(description='DNSLookuper is used for resolve DNS Queries.\n\t\t\n Example: $ python3 dnslookuper.py -D example.txt -o example_output --format json -v -c ', epilog='Thanks for using me!')
		parser.add_argument('-v', '--verbose', action='store_true', help='Turn verbose output on')
		parser.add_argument('-c', '--color', action='store_true', help='Colorize DNSLookup output')
		parser.add_argument('-C', '--compare', action='store', dest='compare', help='Compare results to a list of IPs', type=str)
		parser.add_argument('-H', '--history', action='store_true', help='Search DNS History')
		parser.add_argument('-api', '--api-key-viewdns', action='store', dest='viewdns_api_key', help='ViewDNS api key (Needed if History is used!)', type=str)
		group1 = parser.add_mutually_exclusive_group()
		group1.add_argument('-d', '--domain', action='store', dest='domain', help='Target domain', type=str)
		group1.add_argument('-D', '--list-domains', action='store', dest='list', help='List of target domains', type=str)
		parser.add_argument('-s', '--server', action='store', dest='server', help='DNS server to query', default='8.8.8.8', type=str)
		group2 = parser.add_mutually_exclusive_group()	
		group2.add_argument('-o', '--output', action='store', dest='output', help='Export results to a file', type=str)
		parser.add_argument('-f', '--format', action='store', dest='format', help='Fileformat to export results', choices = ['csv' ,'json'], default = 'csv', type=str)
		group2.add_argument('-oA', '--output-all-formats', action='store', dest='outputallformats', help='Export results with all formats (csv and json)', type=str)
		global args
		args =  parser.parse_args()

		if len(sys.argv) < 2:
			parser.print_help()
			sys.exit(0)

		# Presentation
		banner()

		if args.domain or args.list:
			# Program
			if args.domain:
				dnslook = DNSLookuper([args.domain],server=args.server, verbose=args.verbose, color=args.color)
			elif args.list:
				dnslook = DNSLookuper(input_file=args.list,server=args.server, verbose=args.verbose, color=args.color)
			
			# Resolving Queries
			dnslook.resolve()

			# Comparing Results
			if args.compare:
				dnslook.compare(args.compare)

			if args.history:
				dnslook.history(str(args.viewdns_api_key))

			# Exporting Results
			if args.output:
				dnslook.export(args.output, args.format)
			elif args.outputallformats:
				dnslook.export(args.outputallformats + '.json', 'json')
				dnslook.export(args.outputallformats + '.csv', 'csv')
		else:
			parser.print_help()
			if args.color:
				print(RED + '[!] Introduce a domain (-d, --domain) or a list of domains (-D, --list-domains)' + RESET)
			else:
				print('[!] Introduce a domain (-d, --domain) or a list of domains (-D, --list-domains)')
	

except KeyboardInterrupt:
	print("[!] Keyboard Interrupt. Shutting down")
