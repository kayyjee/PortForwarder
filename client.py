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
--  and how many number of times each client will send that data.
--  The application will also keep a log file of the data sent and received as well as
--  round trip times for each sent data and the average RTT of all the data sent
--  Test with accompanying server applications: multithreadServer.py, epollSelectServer.py and epollEdgeLevelServer.py
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#!/usr/bin/env python

from socket import *
import threading
import time
import random
import sys
import logging
import datetime




def run (clientNumber):
     while 1:
         s = socket(AF_INET, SOCK_STREAM)
         addr = (host,port)
         s.connect(addr)
         s.send(data)
         receiveData = s.recv(buf)
         print "Received: " + (str(receiveData)) + " From: Client " + str(clientNumber)
         t = random.randint(3, 10)
         time.sleep(t)






if __name__ == '__main__':

    host = '192.168.0.24'
    port = 345
    buf = 1024
    clients = 10
    data = "Hello"

    for x in range (clients):
        thread = threading.Thread(target = run, args = [x])
        thread.start()
