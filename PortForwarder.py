'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    PortForwarder.py - Forwards packets to a different address.
--
--  PROGRAM:        Multi threaded method server
--                  python MultiThreadedServer.py
--
--  FUNCTIONS:      initializeParameters(), addressDelimeter(line), readConfig(), mk_Connection(sourceIP, sourcePort, destinationIP, destinationPort),
--                  FindWhereToSend(clientIP, port), receiveHandler(sendsocket, clientsocket, port), clientHandler(clientsocket, clientaddr, port),
--                  threadHandler(port, hostIP).    
--
--  DATE:           March 15, 2015
--
--  REVISIONS:      March 23, 2015
--
--  DESIGNERS:      Kyle Gilles, Justin Tom
--
--  PROGRAMMERS:    Kyle Gilles, Justin Tom
--
--  NOTES:
--  This program reads from a config file source and destination addresses.
--  The program will accept TCP connections from client machines.
--  The program will read data from the client socket and forward it to config file determined adderesses. 
--  Design is a simple, multi-threaded server I/O to handle simultaneous inbound connections.
--  Test with accompanying client application: client.py & server.py
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#!/usr/bin/env python
import socket
import threading
import thread
import time
import argparse
import datetime
import sys

sourceIP = []
sourcePort = []
destinationIP = []
destinationPort = []
ConnectionList = []


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       initializeParameters
--  Parameters:
--      None
--  Return Values:
--      hostip
--          IP of the port forwarder.
--  Description:
--      Function to initialize all the parameters and user specified variables through arguments
--      passed when the python script is executed through the terminal.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def initializeParameters():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', nargs=1, help='The IP PortForwarder is running on.', required=True, dest='host')
    args = parser.parse_args()
    hostip = str(args.host[0])

    return hostip

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       addressDelimeter
--  Parameters:
--      line
--          individual line read from config file.
--  Return Values:
--      source_IP
--          source IP (of packet to be forwarded)
--      source_Port
--          source port (of packet to be forwarded)
--      destination_IP
--          destination IP (where packet will be forwarded)
--      destination_Port
--          destination port (where packet will be forwarded)
--  Description:
--      Parses the config file lines and stores the results as variables 
--      that will be used to forward appropriate packets. 
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
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

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       readConfig
--  Parameters:
--      None
--  Return Values:
--      None
--  Description:
--      Opens the config file and makes a connection object from 
--      the data in each line. 
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def readConfig():
    global sourceIP
    global sourcePort
    global destinationIP
    global destinationPort

    filename = "config.txt"
    file = open(filename, "r")
    for line in file:
	print line
        sIP, sPort, dIP, dPort = addressDelimeter(line)
        sourceIP.append(sIP)
        sourcePort.append(sPort)
        destinationIP.append(dIP)
        destinationPort.append(dPort)

        Connection = mk_Connection(sIP, sPort, dIP, dPort)
        ConnectionList.append(Connection)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  CLASS
--  Name:       Connection
--  Parameters:
--      None
--  Return Values:
--      None
--  Description:
--      An object that will store the source and destination IP & Port Values
--      so that each received packet corresponds with a destination.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       mk_Connection
--  Parameters:
--      sourceIP
--          source IP (of packet to be forwarded)
--      sourcePort
--          source port (of packet to be forwarded)
--      destinationIP
--          destination IP (where packet will be forwarded)
--      destinationPort
--          destination port (where packet will be forwarded)
--  Return Values:
--      connection
--  Description:
--      Passes variables to the Connection object constructor.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def mk_Connection(sourceIP, sourcePort, destinationIP, destinationPort):
    connection = Connection(sourceIP, sourcePort, destinationIP, destinationPort)
    return connection


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       FindWhereToSend
--  Parameters:
--      clientIP
--          IP packet was received from 
--      port
--          port packet was received from
--  Return Values:
--      connection.destinationIP
--          IP where packet is to be forwarded
--      connectin.destinationPort
--          The port to forward the packet to
--  Description:
--      This function acts as a getter method, returning the connection
--      object variables.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def FindWhereToSend(clientIP, port):

    for connection in ConnectionList:
        if connection.sourceIP == clientIP:

            if connection.sourcePort == str(port):

                return connection.destinationIP, connection.destinationPort


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       receiveHandler
--  Parameters:
--      sendSocket
--          Socket connecting port forwarder and server
--      clientSocket
--          Socket connecting port forwarder and client
--  Return Values:
--      None
--  Description:
--      Thread function listening for data from the server, upon receiving data 
--      will send it across the client socket.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def receiveHandler(sendsocket, clientsocket):

    returnData = sendsocket.recv(bufferSize)
    clientsocket.send(returnData)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       clientHandler
--  Parameters:
--      clientSocket
--          Socket connecting port forwarder and client
--      port
--          port where packet was received
--  Return Values:
--      None
--  Description:
--      Thread function that finds where to forward the packet too (from config file)
--      connects to that address, sends the data then starts a thread that 
--      waits for return data. 
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def clientHandler(clientsocket, port):
    global bufferSize
    sendsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientIP, ClientSocket = clientsocket.getpeername()
    destinationIP, destinationPort = FindWhereToSend(clientIP, port)
    addr2 = (destinationIP, int(destinationPort))

    sendsocket.connect(addr2)

    while 1:
        data = clientsocket.recv(bufferSize)
        sendsocket.send(data)

        ReceiveThread = threading.Thread(target = receiveHandler, args=(sendsocket, clientsocket))
        ReceiveThread.start()


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       threadHandler
--  Parameters:
--      port
--          port to bind too
--      hostIP
--          IP of the port forwarder (machine running this program)
--  Return Values:
--      None
--  Description:
--      Thread function that binds to ports determined in the config
--      file, then listens for a connection at those ports. Upon receiving a
--      connection, will create a socket and start a thread to receive data. 
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
def threadHandler(port, hostIP):

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    addr = (hostIP, port)
    serversocket.bind(addr)
    serversocket.listen(50)

    while 1:
        clientsocket, clientaddr = serversocket.accept()
        clientThread = threading.Thread(target = clientHandler, args=(clientsocket, port))
        clientThread.start()




if __name__ == '__main__':
    readConfig()
    Hostip = initializeParameters()
    bufferSize = 1024

    for item in ConnectionList:
	    serverThread = threading.Thread(target = threadHandler, args=(int(item.sourcePort),Hostip))
        serverThread.start()
