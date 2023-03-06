
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
