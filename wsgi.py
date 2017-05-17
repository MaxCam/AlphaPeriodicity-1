from cgi import parse_qs, escape
from file import function

def application(environ, start_response):
	form = parse_qs(environ['QUERY_STRING'])
	start_response('200 OK', [('Content-Type', 'text/html')])
	return [form.get('a')[0]]
