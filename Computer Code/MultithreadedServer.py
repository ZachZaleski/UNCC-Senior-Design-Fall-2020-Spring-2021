import socket
from _thread import *
import threading
import sys
import csv
import time
import random
import datetime

HOST = '192.168.0.167' # IP address of server
PORT = 8000
threadCount = 0
i = 0
messagePackage = []
serverSocket = socket.socket()
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
serverSocket.settimeout(1)
serverSocket.bind((HOST,PORT))

                
def threadedSendMessage(arrayOfCones , messagePackage,sentMessage):
    for cons in arrayOfCones:
        message = sentMessage
        for i in messagePackage:
            message = message + i

        messageSplit = message.split(",")
        for characters in messageSplit:
            if '('  in characters or ')' in characters:
                message = sentMessage
        try:
            cons.sendall(message.encode())
        except socket.error:
            cons.close()
    print("Final Message:" +  message)       
        
    messagePackage.clear()   
    
def threadedClientIndi(conn , messagePackage,e):
    e.clear()
    try:
        data = conn.recv(1024)
        recvMessage = data.decode('utf-8' , 'replace')
        recvMessage = recvMessage[2:]
        print(recvMessage)
        messagePackage.append(recvMessage)
        e.set()          
    except socket.error:
        e.set()
        
def threadedClient(arrayOfCones , messagePackage , e):

    for conn in arrayOfCones:
        start_new_thread(threadedClientIndi, ((conn,messagePackage,e)))
    print('Done with this iteration')



print('Server started')
print('Socket Listening...')
serverSocket.listen(5) # Queue of connections

allClient = [] 

iteration = 0 

e = threading.Event()
messages = ["Intrusion - 2 Seconds - Run," , "Barrier Removed - Fix It - Now,"]                        

while True:
    try:
        client , address = serverSocket.accept()
        allClient.append(client)
        
    except socket.timeout:
        e.set()
        sentMessage = ""
        
        if iteration < 30:
            sentMessage = "{:.2f}".format(random.random()*6.99) 
        elif 30 <= iteration and iteration < 35:    
            sentMessage = "{:.2f}".format(7.0 + random.random()) 
        elif iteration >= 35 and iteration < 40:     
            sentMessage = "{:.2f}".format(random.random()*6.99) 
        elif iteration >= 40 and iteration < 45:
            sentMessage = "{:.2f}".format(9.99) 
        
        else:
            sentMessage = "{:.2f}".format(random.random()*6.99) 
    

        if(float(sentMessage) > 9):
            sentMessage = sentMessage +","+ messages[0]
        elif (float(sentMessage) <=9 and float(sentMessage) > 7 ):
            sentMessage = sentMessage +","+ messages[1]
        else :
            sentMessage = sentMessage +","  
            
        if(len(allClient) != 0 and e.isSet()):            
            start_new_thread(threadedSendMessage, ((allClient,messagePackage,sentMessage)))
            start_new_thread(threadedClient, ((allClient,messagePackage,e)))
            time.sleep(1)
            iteration = iteration + 1

serverSocket.close()
serverSocket.shutdown(socket.SHUT_RDWR)

