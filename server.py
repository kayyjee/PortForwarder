'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    server.py - A simple echo server using multiple threads to handle client connections
--
--  PROGRAM:        Multi threaded echo server
--                  python server.py
--
--  FUNCTIONS:      initializeParameters(), threadHandler(port, ip)
--
--  NOTES:
--  The program will accept TCP connections from client machines.
--  The program will read data from the client socket and simply echo it back.
--  Design is a simple, multi-threaded server I/O to handle simultaneous inbound connections.
--  Test with accompanying server applications: config.txt, PortForwarder.py, client.py
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#!/usr/bin/env python
import socket
import threading
import thread
import time
import argparse
import datetime
import sys

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       initializeParameters
--  Parameters:
--      None
--  Return Values:
--      host
--          The IP of the current host the server is running on.
--  Description:
--      Function to initialize all the parameters and user specified variables through arguments
--      passed when the python script is executed through the terminal.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def initializeParameters():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', nargs=1, help='The IP Server is running on.', required=True, dest='host')
   
    args = parser.parse_args()
    host = str(args.host[0])
    return host

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       threadHandler
--  Parameters:
--      port
--          Port(s) to listen on for any connections
--      ip
--          IP address of the client/port forwarder that will be connecting to the server.
--  Return Values:
--      host
--          The IP of the current host the server is running on.
--  Description:
--      Function to infinitely receive and send back data to the connected portforwarder/client.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def threadHandler(port, ip):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    addr = (ip, port)
    serversocket.bind(addr)
    serversocket.listen(50)
    clientsocket, clientaddr = serversocket.accept()

    while 1:

        data = clientsocket.recv(1024)
        print str(data)
        clientsocket.send(data)





if __name__ == '__main__':
    ip = initializeParameters()
    AllConnections = [] #Full of connections
    bufferSize = 1024


    #For each unique port,
    AllConnections.append(8005)
    AllConnections.append(8006)
    
    print ("Server is listening for connections\n")


    for port in AllConnections:
        serverThread = threading.Thread(target = threadHandler, args=(port,ip))
        serverThread.start()
