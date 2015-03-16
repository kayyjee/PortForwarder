'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    MultiThreadedServer.py - A simple echo server using multiple threads to handle client connections
--
--  PROGRAM:        Multi threaded method server
--                  python MultiThreadedServer.py
--
--  FUNCTIONS:      run(hostIP, port), close()
--
--  DATE:           February 10, 2015
--
--  REVISIONS:      February 18, 2015
--
--  DESIGNERS:      Kyle Gilles
--
--  PROGRAMMERS:    Kyle Gilles, Justin Tom
--
--  NOTES:
--  The program will accept TCP connections from client machines.
--  The program will read data from the client socket and simply echo it back.
--  Design is a simple, multi-threaded server I/O to handle simultaneous inbound connections.
--  The program will also keep a log file of the number of connections and all data being echoed.
--  Test with accompanying client application: echoClient.py
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#!/usr/bin/env python
import socket
import threading
import thread
import time
import datetime
import sys


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
    ip = '192.168.0.22'

    AllConnections = [] #Full of connections
    bufferSize = 1024

    #Read Config
    #For each unique port,
    # AllConnections.append(8005)
    AllConnections.append(8006)
    #Read Config
    #For each unique port:
    print ("Server is listening for connections\n")


    for port in AllConnections:
        serverThread = threading.Thread(target = threadHandler, args=(port,ip))
        serverThread.start()
