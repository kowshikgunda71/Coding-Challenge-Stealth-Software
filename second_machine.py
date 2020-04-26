import socket
import threading
import os
import time

ENCODING = 'utf-8'

#dictionary where address of the computers store along with there messages
messages = {
    "xxx.xxx.xx.x" : None,  ### 1st address should be of local computer
    "xxx.xxx.xx.xx" : None,
    "xxx.xxx.xx.x" : None
}

 
#this class is for listening to other computers
class Receiver(threading.Thread):
 
    #set address and host of local computer
    def __init__(self, my_host, my_port):
        threading.Thread.__init__(self, name="messenger_receiver")
        self.host = my_host
        self.port = my_port
 
    #recieve messages from other computers
    def listen(self):
        # open a socket to listen other computers requests
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(10)

        #in this loop our computer continously listen to requests for connection from other computers
        while True:
            #connection variable stores the connection connection and client_address has the address and port# of other computer
            connection, client_address = sock.accept()
            try:
                full_message = ""
                while True:
                    #here data recieves the message from other computer
                    data = connection.recv(16)
                    #we have to encode it to utf-8
                    full_message = full_message + data.decode(ENCODING)
                    if not data:
                        #stores message in dictionary where key is address of other computer and break the loop
                        messages[client_address[0]] = full_message
                        break
            finally:
                #shutting down the connection
                connection.shutdown(2)
                connection.close()
 
    def run(self):
        self.listen()
 
#this class is for sending messages to other computers
class Sender(threading.Thread):
    
    #set address and host of other computers
    def __init__(self, my_friends_host1, my_friends_port1, my_friends_host2, my_friends_port2):
        threading.Thread.__init__(self, name="messenger_sender")
        self.host1 = my_friends_host1
        self.port1 = my_friends_port1
        self.host2 = my_friends_host2
        self.port2 = my_friends_port2
 
    #send messages to other computers
    def run(self):
        while True:
            #here we check weather our message has any value or not
            if list(messages.values())[0] is not None:
                #get message from dictionary
                message = list(messages.values())[0]

                #make a socket object and connect with 1st computer
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.host1, self.port1))
                #send message to that computer
                s.sendall(message.encode(ENCODING))
                #shutting down the connection
                s.shutdown(2)
                s.close()

                #make a socket object and connect with 2nd computer
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.host2, self.port2))
                #send message to that computer
                s.sendall(message.encode(ENCODING))
                #shutting down the connection
                s.shutdown(2)
                s.close()
 
 
def main():
    #get and set the address and ports of local computer
    my_host = list(messages)[0] 
    my_port = 44444 

    #make object of reciever class and pass address and port of local computer
    receiver = Receiver(my_host, my_port)
    
    #get and set the address and ports of other computer
    my_friends_host1 = list(messages)[1] 
    my_friends_port1 = 44444 

    my_friends_host2 = list(messages)[2] 
    my_friends_port2 = 44444 
    
    #make object of sender class and pass address and port of other computers
    sender = Sender(my_friends_host1, my_friends_port1, my_friends_host2, my_friends_port2)
    
    #run the functions in threads bcz we need them to work as async
    treads = [receiver.start(), sender.start()]
    
    #get message from user 
    messages[list(messages)[0]] = input("Enter message: ")

    while True:
        #here we call an infinite loop which runs until we have messages from other 2 computers
        #once we have messages print it on screen and exit the program
        if list(messages.values())[1] is not None and list(messages.values())[2] is not None:
            print(list(messages.values())[0])
            print(list(messages.values())[1])
            print(list(messages.values())[2])
            
            time.sleep(3)
            os._exit(1)
        
 
if __name__ == '__main__':
    main()
