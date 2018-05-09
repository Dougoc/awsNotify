#!/Users/douglas.costa/.envs/aws-handler/bin/python
"""

"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from collections import namedtuple
import json
from elasticsearch import Elasticsearch
import time
import datetime

es = Elasticsearch([dict(host='localhost', port=9200, http_auth=('elastic', 'changeme'))])

ts = time.time()

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.end_headers()

        data = json.loads(self.data_string, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        time = data.Timestamp
        message = data.Message
        detail = json.loads(message)
        instanceid = detail['detail']['instance-id']
        state = detail['detail']['state']
        analyzed = {'state': state, 'instanceid': instanceid, 'ocurred-time': time}
        es.index(index='aws', doc_type='instances', body=analyzed)
        print analyzed


def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
