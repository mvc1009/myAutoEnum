import os


def print_status(message=""):
	print(f"\033[1;34m[*]\033[1;m {message}")


def print_good(message=""):
	print(f"\033[1;32m[+]\033[1;m {message}")


def print_error(message=""):
	print(f"\033[1;31m[-]\033[1;m {message}")


def print_debug(message=""):
	print(f"\033[1;31m[!]\033[1;m {message}")


def str_domain_from_subdomain(subdomain):
	return '.'.join(subdomain.split('.')[-2:])


def str_is_domain(entry):
	le = entry.split('.')
	if len(le) == 2:
		return True
	return False

def str_is_subdomain(entry):
	le = entry.split('.')
	if len(le) > 2:
		return True
	return False

def str_get_domain_from_url(url):
	if 'http' in url:
		a = url.split('&')[0].split('?')[0].split('/')[2].split(':')[0].lower()
		if '@' not in a and len(a.split('.')) > 1 and a[-1] != '.':
			return a
	return None


def get_proxy():
	if os.environ.get("PROXY") != '':
		return {"http" : os.environ.get("PROXY"), "https" : os.environ.get("PROXY")}
	else:
		return None