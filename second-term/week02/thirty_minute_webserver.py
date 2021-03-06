#
# ws30 -- the thirty minute web server
# author: Wilhelm Fitzpatrick (rafial@well.com)
# date: August 3rd, 2002
# version: 1.0
#
# Written after attending a Dave Thomas talk at PNSS and hearing about
# his "write a web server in Ruby in one hour" challenge.
#
# Actual time spent:
#  30 minutes reading socket man page
#  30 minutes coding to first page fetched
#   3 hours making it prettier & more pythonic
#
# updated for UW Internet Programming in Python, by Brian Dorsey
#

import os, socket, sys, subprocess

local_defaults = ['127.0.0.1', '8080']
defaults = ['', '8080']
mime_types = {'.jpg' : 'image/jpg', 
             '.gif' : 'image/gif', 
             '.png' : 'image/png',
             '.html' : 'text/html', 
             '.pdf' : 'application/pdf'}
response = {}

response[200] =\
"""HTTP/1.0 200 Okay
Server: ws30
Content-type: %s

%s
"""

response[301] =\
"""HTTP/1.0 301 Moved
Server: ws30
Content-type: text/plain
Location: %s

moved
"""

response[404] =\
"""HTTP/1.0 404 Not Found
Server: ws30
Content-type: text/plain

%s not found
"""

DIRECTORY_LISTING =\
"""<html>
<head><title>%s</title></head>
<body>
<a href="%s..">..</a><br>
%s
</body>
</html>
"""


TIME_HTML = \
"""<html>
<head><title>%s</title></head>
<body>
The unix time is %s
</body>
</html>

"""


DIRECTORY_LINE = '<a href="%s">%s</a><br>'

def server_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    return s

def listen(s):
    connection, client = s.accept()
    return connection.makefile('r+')

def get_request(stream):
    method = None
    while True:
        line = stream.readline()
        #print line
        if not line.strip(): 
            break
        elif not method: 
            method, uri, protocol = line.split()
    #print uri
    return uri

def list_directory(uri):
    entries = os.listdir('.' + uri)
    entries.sort()
    return DIRECTORY_LISTING % (uri, uri, '\n'.join(
        [DIRECTORY_LINE % (e, e) for e in entries]))

def get_file(path):
    f = open(path)
    try: 
        return f.read()
    finally: 
        f.close()

def get_time():
    import time
    return TIME_HTML % (time.time(), time.time())


def start_response(status, headers):
    # This is so bad.  Nasty Nasty Hack.
    pass
    

def get_content(uri):
    print 'fetching:', uri
    try:
        path = '.' + uri
        if os.path.isfile(path):
            #if path.split(".")[-1] == "py":
            #    return(200, 'text/html', subprocess.Popen(['python', path], stdout=subprocess.PIPE).stdout.read())
            return (200, get_mime(uri), get_file(path))
        if os.path.isdir(path):
            if(uri.endswith('/')):
                return (200, 'text/html', list_directory(uri))
            else:
                return (301, uri + '/')
        # Only gathers the root, proof of concept.
        if uri == '/django/':
            # WSGI Stuff goes here
            # This is a very incomplete implementation
            from django.core.handlers.wsgi import WSGIHandler
            application = WSGIHandler()
            dsm = 'hello.settings'
            os.environ['DJANGO_SETTINGS_MODULE'] = dsm
            if os.path.realpath(os.path.dirname(__file__)) not in sys.path:
                sys.path.append(os.path.realpath(os.path.dirname(__file__)))
            iterable = application({'DJANGO_SETTINGS_MODULE': dsm, 'REQUEST_METHOD':'GET', 'SERVER_NAME':'NOT_IMPLEMENTED', 'SERVER_PORT':'NOT_IMPLEMENTED'}, start_response)
            body = ""
            for data in iterable:
              body += str(data)
            return (200, 'text/html', body)          
        elif uri == '/time/':
            return (200, 'text/html', get_time())
        elif uri == '/kill/':
            raise KeyboardInterrupt      
        else: return (404, uri)
    except IOError, e:
        return (404, e)

def get_mime(uri):
    return mime_types.get(os.path.splitext(uri)[1], 'text/plain')

def send_response(stream, content):
    stream.write(response[content[0]] % content[1:])

if __name__ == '__main__':
    args, nargs = sys.argv[1:], len(sys.argv) - 1
    host, port = (args + defaults[-2 + nargs:])[0:2]
    server = server_socket(host, int(port))
    print 'starting %s on %s...' % (host, port)
    try:
        while True:
            stream = listen (server)
            send_response(stream, get_content(get_request(stream)))
            stream.close()
    except KeyboardInterrupt:
        print 'shutting down...'
    server.close()

