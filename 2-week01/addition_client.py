import socket
import sys


def server_addition(host, port, arg1, arg2):
    size = 1024
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
        
    to_send = '%s+%s' % (arg1, arg2)
    
    print "Server at %s:%s" % (host, port,)
    print "Sending: %s" % ( to_send)    
    s.send(to_send)
    data = s.recv(size)
    s.close()
    print 'Received:', data

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "ERROR, addition_client.py takes two arguments, the numbers to be added together.  Example: python addition_client.py 10 24"
    else:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        host = 'block115401-q6x.blueboxgrid.com'
        port = 50000
        
        server_addition(host, port, arg1, arg2)