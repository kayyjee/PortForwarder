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
    source_Port = forwarderList[0]
    destination = forwarderList[1]
    destinationTemp = destination.split(":")
    destination_IP = destinationTemp[0]
    destination_Port = destinationTemp[1]
    #Since this is the last delimited value from the line, it will contain a newline character, thus we will need to remove it evey time
    destination_Port = destination_Port.strip(' \t\n\r')
    return source_Port, destination_IP, destination_Port

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
    global sourcePort
    global destinationIP
    global destinationPort

    filename = "config.txt"
    file = open(filename, "r")
    for line in file:
    print line
        sPort, dIP, dPort = addressDelimeter(line)
        sourcePort.append(sPort)
        destinationIP.append(dIP)
        destinationPort.append(dPort)

        Connection = mk_Connection(sPort, dIP, dPort)
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
    sourcePort = ""
    destinationIp = ""
    destinationPort = ""

    def __init__(self, sourcePort, destinationIP, destinationPort):
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
def mk_Connection(sourcePort, destinationIP, destinationPort):
    connection = Connection(sourcePort, destinationIP, destinationPort)
    return connection


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       dataHandler
--  Parameters:
--      source
--          source of incoming packets
--      destination
--          destination address of incoming packets
--  Return Values:
--      None
--  Description:
--      Thread function that sits at receive, upon receiving a packet will 
--      forward it to the destination.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def dataHandler(source, destination):
   while 1:
        data = source.recv(bufferSize)
        if data ==' ':
            source.shutdown(socket.SHUT_RD)
            destination.shutdown(socket.SHUT_WR)    
        destination.sendall(data)
    
    


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
--      connection, will create start 2 threads, one to handle packets coming 
--      from the client and one coming from the server.  
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
def threadHandler(connection, hostIP):

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    addr = (hostIP, int(connection.sourcePort))
    serversocket.bind(addr)
    serversocket.listen(50)

     while 1:
        clientsocket, clientaddr = serversocket.accept()
        sendsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sendAddr = (Connection.destinationIP, int(Connection.destinationPort))
        sendsocket.connect(sendAddr)
        clientThread = threading.Thread(target = sendData, args=(sendsocket, clientsocket))
        receiveThread = threading.Thread(target = sendData, args=(clientsocket, sendsocket))
        clientThread.start()
        receiveThread.start()




if __name__ == '__main__':
    readConfig()
    Hostip = initializeParameters()
    bufferSize = 1024

    for connection in ConnectionList:
        serverThread = threading.Thread(target = threadHandler, args=(connection,Hostip))
        serverThread.start()

