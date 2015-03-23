'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    client.py - A simple TCP client program.
--
--  PROGRAM:        Multi threaded client
--                  python client.py
--
--  FUNCTIONS:      run(), initializeParameters()
--
--  NOTES:
--  The program will create a TCP connection from the specified server and port.
--  The port forwarder IP address, port and number of connections will be specified at command execution.
--  The buffer size and data being sent are hardcoded into the code.
--  The program will then receive back the echo'd data from the server and print out the data
--  to ensure the data was kept intact on it's round trip.
--  Test with accompanying server applications: config.txt, PortForwarder.py, server.py
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
--      host
--          The IP address of the port forwarder
--      port
--          The port the client will use to connect with
--      clients
--          How many clients to simulate connecting to the port forwarder with.
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





'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       run
--  Parameters:
--      clientNumber
--  Return Values:
--      none
--  Description:
--      Function to infinitely send and receive data to the specified portforwarder.
--      It will also print the data it has received as well as from which host.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
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
