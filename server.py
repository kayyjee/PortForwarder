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
import argparse
import datetime
import sys

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       initializeParameters
--  Parameters:
--      None
--  Return Values:
--      numberOfAttempts
--          The total number of failed password attempts before blocking the IP
--      timeScan
--          The amount of time to use for slow scan password attempts
--      banTime
--          The time that will be passed after being blocked before the user is unblocked.
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
