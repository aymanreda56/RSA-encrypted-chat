# server
import socket
import threading
import RSA
import math
from Crypto.Util import number

PORT = 5050
FORMAT = "utf-8"
D ="DISCONNECT"
HEADER = 64
hostname = socket.gethostname()
SERVER = socket.gethostbyname(hostname)
#192.168.56.1
ADDR = (SERVER,PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def send(msg, client):
    MSG = msg.encode(FORMAT)
    msg_len = len(MSG)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' '* (HEADER-len(send_len))
    client.send(send_len)
    client.send(MSG)

def client(conn, addr, p, q, e):
    print(f"{addr} is Connectedd!")
    connected = True
    #send public key to sender
    n = p * q
    en = str(e) + " " + str(n)
    send(en, conn)
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)                          #read exactly msg_len from buffer
            msg = conn.recv(msg_len).decode(FORMAT)#mmm
            if msg == D:
                connected = False
            print(f"{addr} {msg}")
            
            #naiive method to get message content as integers not strings (everything is sent/received as strings not lists)
            encryptedMSG = []
            temp = ""
            flag_to_append = False
            for i in range(msg_len):
                if (msg[i] != '[' and msg[i] != ',' and msg[i] != ' ' and msg[i] != ']'and msg[i] != '\''):
                    temp += str(msg[i])
                    flag_to_append = True

                elif(flag_to_append):
                    print("test")
                    print(temp)
                    temp = int(temp)
                    encryptedMSG.append(temp)
                    temp= ""
                    flag_to_append = False

            if(flag_to_append):
                encryptedMSG.append(temp)
                temp = ""


            print("\n")
            print(encryptedMSG)

            #Decrypting here 
            origmsg = RSA.Decrypt(encryptedMSG, p, q, e)
            print("\n" + origmsg + "\n")

            #if sender sent "DISCONNECT" or "DISCONNEC" (due to sender terminating before sending the last letter),
            #just get out of the loop and close the connection
            if(origmsg == 'DISCONNECT' or origmsg == 'DISCONNEC' or origmsg == 'DISCONNE'):
                connected = False
    conn.close()


def start(p, q, e):
    server.listen()
    print(" The server is listening to ",SERVER)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=client, args=(conn, addr, p, q, e))
        thread.start()
        

print("The Server is listening")
#print(SERVER)



# IO MODES here
mode = int(input("\n enter mode, 0 for manual entry of parameters, 1 for autogeneration"))

while (mode != 0 and mode != 1):
    mode = int(input("\n incorrect entry ! \n plz enter either 0 or e !"))

if(mode == 0):

    p = int(input("\n enter P\n"))
    while (not RSA.isPrime(p) or p < 2):
        p = int(input("\n wrong p, enter a prime number\n"))


    q = int(input("\n enter q or enter 0 to autogenerate\n"))
    while(q != 0 and not RSA.isPrime(q) or q == 1 or q < 0):
        q = int(input("\n wrong q, enter a prime number \n"))

    # generate a q same bit size as p, to keep n at bit size 2* bit size of p or q
    if(q == 0):
        q = number.getPrime(p.bit_length())
        while (q == p):
            q = number.getPrime(p.bit_length())

    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = int(input("\n enter e or enter 0 to autogenerate\n"))
    # check e constraints or generate randomly
    if(e):
        while ((math.gcd(e, phi_n) != 1) and (e > phi_n) and (e > 1)):
            e = int(input("\n incorrect e ! \n e must be coprime with phi_n and 1 < e < phi_n \n enter e again or enter 0 to autogenerate."))
            if(e == 0):
                break

    # generate prime e with bit size less than phi_n to ensure it is less than phi_n
    if(e == 0):
        e = number.getPrime(phi_n.bit_length() - 1)
        if(e < 10 or e < 1):
            e == 3



    



elif(mode):

    #generate everything
    p = number.getPrime(64)

    q = number.getPrime(64)
    while (p == q):
        q = number.getPrime(64)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = number.getPrime(phi_n.bit_length() - 1)
    while(math.gcd(e, phi_n) != 1 or (e >= phi_n)):
        e = number.getPrime(phi_n.bit_length() - 1)



#private key
d = RSA.Mod_inverse(e, phi_n)

print("\n p = ")
print(p)
print("\n q = ")
print(q)
print("\n n = ")
print(n)
print("\n phi_n = ")
print(phi_n)
print("\n e = ")
print(e)
print("\n d = ")
print(d)

start(p, q, e)