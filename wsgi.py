from cgi import parse_qs, escape
from MySQLpersister import run

def application(environ, start_response):
    form = parse_qs(environ['QUERY_STRING'])
    start_response('200 OK', [('Content-Type', 'text/html')])

    defaultStart=form.get('start')[0]
    defaultEnd=form.get('stop')[0]
    defaultProbeId=form.get('probe')[0]
    defaultMeasurement=form.get('measurement')[0]
    return [run(defaultStart,defaultEnd,defaultMeasurement,defaultProbeId)]
