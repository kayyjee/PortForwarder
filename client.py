'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    echoClient.py - A simple TCP client program.
--
--  PROGRAM:        Multi threaded client
--                  python echoClient.py
--
--  FUNCTIONS:      run()
--
--  DATE:           February 10, 2015
--
--  REVISIONS:      February 18, 2015
--
--  DESIGNERS:      Kyle Gilles, Justin Tom
--
--  PROGRAMMERS:    Kyle Gilles, Justin Tom
--
--  NOTES:
--  The program will accept TCP connections from a user specified server and port.
--  The server will be specified by the IP address.
--  The user will be prompted for the data to send, how many clients to simulate
--  and how many number of ports each client will send that data.
--  The application will also keep a log file of the data sent and received as well as
--  round trip ports for each sent data and the average RTT of all the data sent
--  Test with accompanying server applications: multithreadServer.py, epollSelectServer.py and epollEdgeLevelServer.py
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#!/usr/bin/env python

from socket import *
import threading
import argparse
import random
import sys
import logging
import datetime
import time



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       initializeParameters
--  Parameters:
--      None
--  Return Values:
--      numberOfAttempts
--          The total number of failed password attempts before clientsing the IP
--      portScan
--          The amount of port to use for slow scan password attempts
--      banport
--          The port that will be passed after being clientsed before the user is unclientsed.
--  Description:
--      Function to initialize all the parameters and user specified variables through arguments
--      passed when the python script is executed through the terminal.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def initializeParameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', nargs=1, help='The IP of the PortForwarding host.', required=True, dest='host')
    parser.add_argument('-p', '--port', nargs=1, help='The Port to Connect at.', required=True, dest='port')
    parser.add_argument('-c', '--clients', nargs=1, help='Number of Simultaneous Clients to Connect', required=True, dest='clients')
    
    args = parser.parse_args()

    host = str(args.host[0])
    port = int(args.port[0])
    clients = int(args.clients[0])
    
    
    return host, port, clients






def run (clientNumber):
     s = socket(AF_INET, SOCK_STREAM)
     addr = (host,port)
     s.connect(addr)
     while 1:
         
         s.send(data)
         receiveData = s.recv(buf)
         print "Received: " + (str(receiveData)) + " From: Client " + str(clientNumber)
         t = random.randint(3, 10)
         time.sleep(t)






if __name__ == '__main__':

    host, port, clients = initializeParameters()
    buf = 1024
    data = "Hello"

    for x in range (clients):
        thread = threading.Thread(target = run, args = [x])
        thread.start()
