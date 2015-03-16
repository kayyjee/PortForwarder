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

sourceIP = []
sourcePort = []
destinationIP = []
destinationPort = []
ConnectionList = []

def addressDelimeter(line):
    forwarderList = line.split(",")
    source = forwarderList[0]
    destination = forwarderList[1]
    sourceTemp = source.split(":")
    source_IP = sourceTemp[0]
    source_Port = sourceTemp[1]
    destinationTemp = destination.split(":")
    destination_IP = destinationTemp[0]
    destination_Port = destinationTemp[1]
    #Since this is the last delimited value from the line, it will contain a newline character, thus we will need to remove it evey time
    destination_Port = destination_Port.strip(' \t\n\r')
    return source_IP, source_Port, destination_IP, destination_Port

def readConfig():
    global sourceIP
    global sourcePort
    global destinationIP
    global destinationPort

    filename = "config.txt"
    file = open(filename, "r")
    for line in file:

        sIP, sPort, dIP, dPort = addressDelimeter(line)
        sourceIP.append(sIP)
        sourcePort.append(sPort)
        destinationIP.append(dIP)
        destinationPort.append(dPort)

        Connection = mk_Connection(sIP, sPort, dIP, dPort)
        ConnectionList.append(Connection)






class Connection(object):
    sourceIp = ""
    sourcePort = ""
    destinationIp = ""
    destinationPort = ""



    def __init__(self, sourceIP, sourcePort, destinationIP, destinationPort):
        self.sourceIP = sourceIP
        self.sourcePort = sourcePort
        self.destinationIP = destinationIP
        self.destinationPort = destinationPort


def mk_Connection(sourceIP, sourcePort, destinationIP, destinationPort):
    connection = Connection(sourceIP, sourcePort, destinationIP, destinationPort)
    return connection




def FindWhereToSend(clientIP, port):

    for connection in ConnectionList:
        if connection.sourceIP == clientIP:

            if connection.sourcePort == str(port):

                return connection.destinationIP, connection.destinationPort




def receiveHandler(sendsocket, clientsocket, port):

        returnData = sendsocket.recv(bufferSize)
        print "Received: " + (str(returnData))
        clientsocket.send(returnData)


def clientHandler(clientsocket, clientaddr, port):
    global bufferSize
    sendsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientIP, ClientSocket = clientsocket.getpeername()
    destinationIP, destinationPort = FindWhereToSend(clientIP, port)
    addr2 = (destinationIP, int(destinationPort))

    sendsocket.connect(addr2)

    while 1:
        print "HERE"
        data = clientsocket.recv(bufferSize)
        print "Got it"
        sendsocket.send(data)

        ReceiveThread = threading.Thread(target = receiveHandler, args=(sendsocket, clientsocket, port))
        ReceiveThread.start()








def threadHandler(port, hostIP):


    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    addr = (hostIP, port)
    serversocket.bind(addr)
    serversocket.listen(50)

    while 1:
        clientsocket, clientaddr = serversocket.accept()
        clientThread = threading.Thread(target = clientHandler, args=(clientsocket, clientaddr, port))
        clientThread.start()












if __name__ == '__main__':
    readConfig()


    Hostip = '192.168.0.24'

    bufferSize = 1024



    for item in ConnectionList:
        serverThread = threading.Thread(target = threadHandler, args=(int(item.sourcePort),Hostip))
        serverThread.start()
