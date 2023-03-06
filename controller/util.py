
def str_domain_from_subdomain(subdomain):
	return '.'.join(subdomain.split('.')[-2:])


def str_is_domain(entry):
	le = entry.split('.')
	if len(le) == 2:
		return True
	return False

def str_is_subdomain(entry):
	le = entry.split('.')
	if len(le) == 3:
		return True
	return False

def str_get_domain_from_url(url):
	a = url.split('&')[0].split('?')[0].split('/')[2].split(':')[0].lower()
	if '@' not in a and len(a.split('.')) > 1 and a[-1] != '.':
		return a
	return None
