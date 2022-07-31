from collections import namedtuple
import socket
import threading
from tkinter.font import names
import RSA
import math
import queue

# CLIENT
PORT = 5050
FORMAT = "utf-8"
HEADER = 64
SERVER = "172.26.48.1"
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)



my_queue = queue.Queue()



def send(msg):
    MSG = msg.encode(FORMAT)
    msg_len = len(MSG)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' '* (HEADER-len(send_len))
    client.send(send_len)
    client.send(MSG)

def read():
    msg_len = client.recv(HEADER).decode(FORMAT)
    if msg_len:

        #we must receive the public key before doing any communication
            msg_len = int(msg_len)
            msg = client.recv(msg_len).decode(FORMAT)
            print("\n RECIEVED e & n \n")

            e = ""
            n = ""
            temp = ""
            flag_to_append = False
            for i in range(msg_len):
                if (msg[i] != '[' and msg[i] != ',' and msg[i] != ' ' and msg[i] != ']'):
                    temp += str(msg[i])
                    flag_to_append = True

                elif(flag_to_append):
                    if(not e):
                        e += temp
                    else:
                        n += temp
                    temp= ""
                    flag_to_append = False
            n += temp
            e = int(e)
            n = int(n)
            print(f" {msg}")
#            print("func e = " + str(e))
#            print("func n = " + str(n))

            # I used a queue because threads dont return anything, instead, they can access some sort of shared resource
            my_queue.put(e)
            my_queue.put(n)




while (1):


#messages to be encrypted
    x = input("\n enter a sample message ")
    while(x == ""):
        x = input("\n plz enter a sample text again \n")
    

    thread = threading.Thread(target=read)
 
    thread.start()
    

    e = my_queue.get()
    n = my_queue.get()
    my_queue.put(e)
    my_queue.put(n)
    print("\n e = " + str(e) + "\n")
    print("\n n = " + str(n) + "\n")
    MSG = RSA.Encrypt(x, n, e)
    print(MSG)

    #if you entered "DISCONNECT" it will send the same message to the receiver then terminate both
    if(x != "DISCONNECT"):
        send(str(MSG))

    if(x == "DISCONNECT"):
        send(str(RSA.Encrypt("DISCONNECT", n, e)))
        break
    

