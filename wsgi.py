from cgi import parse_qs, escape
from MySQLpersister import run
from pathlib2 import Path

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

def application(environ, start_response):
    form = parse_qs(environ['QUERY_STRING'])
    start_response('200 OK', [('Content-Type', 'text/html')])

    try:
        defaultStart=int(form.get('start')[0])
        defaultEnd=int(form.get('stop')[0])
        defaultProbeId=int(form.get('probe')[0])
        defaultMeasurement=int(form.get('measurement')[0])
    except:
        return [str(file_get_contents("index.html"))]
    return [run(defaultStart,defaultEnd,defaultMeasurement,defaultProbeId)]
