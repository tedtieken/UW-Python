#Based on echo server from class
# Takes two numbers separated by either " " or "+" and adds them together
import socket 

host = '' 
port = 50000 
backlog = 5 
size = 1024

s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM) 
s.bind((host,port)) 
s.listen(backlog) 

ERROR_MSG = "An Error occurred, addition server accepts two integers separated by either ' ' or '+'.  Example '1+1'' or '2 2' You sent '%s'"

print "Addition server running on port %s ..." % port

try:
    while True: 
        client, address = s.accept()
        data = client.recv(size) 
        
        print "Client at %s said %s" % (address[0], data)
    
        # Try to split on " "
        data_list = data.split()
        
        # If that didn't work, try to split on "+"
        if len(data_list) != 2:
            data_list = data.split("+")                     
        
        if len(data_list)!= 2:
            to_return = ERROR_MSG % data
        else:
            try:
                val1 = int(data_list[0])
                val2 = int(data_list[1])
            except:
                to_return = ERROR_MSG % data
            else:
                to_return = str(val1 + val2)

        client.send(to_return)        
        print "Server returned %s " % to_return

        client.close()
except:
    s.close()    