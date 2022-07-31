# import sys
import math
from re import M

#<----------------------------------------------INVERSION------------------------------------>
def MsgToNumber(msg):
    result = 0
    for i in range(len(msg)):
        result = result * 256 + ord(msg[i])       
    return result

def NumberToMsg(number):
    result = ""
    while number > 0:
        result += chr(number % 256)
        number //= 256
    return result[::-1]

# print(NumberToMsg(MsgToNumber('Send me 5000000')))
# print(NumberToMsg(MsgToNumber("try to atttttack")))

#<----------------------------------------------SPLITTING------------------------------------>
#<-----M < n ----->
def Split_Msg(msgs, n):
    temp = MsgToNumber(msgs)
    temp2 = str(temp)
    # Mi_LEN = math.floor( len(temp2) /( len(str(n)) - 1) ) 
    #print(temp2, "mmm")
    Mi = []
    i = 0
    while(True):
        #if(i != Mi_LEN - 1):
        if(len(temp2) - (len(str(n))-1) * (i) >  len(str(n-1)) ):
            # print(i,"jj")
            Mi.append( (temp2[ (len(str(n))-1) * i : (len(str(n))-1) * (i+1) ]) )
            # print((temp2[ (len(str(n))-1) * i : (len(str(n))-1) * (i+1) ]))
            Mi[i] = int(Mi[i])
            Mi[i] = NumberToMsg(Mi[i])
        else:
            # print(i, "ss")
            Mi.append( (temp2[ (len(str(n))-1)* i : len(temp2) ]) )
            # print((temp2[ (len(str(n))-1)* i : len(temp2) ]))
            Mi[i] = int(Mi[i])
            Mi[i] = NumberToMsg(Mi[i])
            break
        i += 1
    return Mi

#<----------------------------------------------HELPER FUNCTIONS------------------------------------>
def isPrime(n):
    if n == 2 or n == 3: return True
    if n < 2 or n%2 == 0: return False
    if n < 9: return True
    if n%3 == 0: return False
    r = int(n**0.5)
    f = 5
    while f <= r:
        if n % f == 0: return False
        if n % (f+2) == 0: return False
        f += 6
    return True


def Mod_exp(m, e, n):
    if e == 0:
        return 1 % n
    elif e == 1:
        return m % n
    else:
        result = Mod_exp(m, e // 2, n)
        result = result * result % n
        if e % 2 == 0:
            return result
        else:
            return result * m % n

def Ext_ecludean(a, b):
    if a == 0:
        return  (b, 0, 1)
    d, y, x = Ext_ecludean(b % a, a)
    return (d, x-(b //a) * y, y)

def Mod_inverse(e, totient_func):
    d, x, y = Ext_ecludean(e, totient_func)
    if d != 1:
        print(" no inverse for e ")               ############# to be handeled
    else:  
        return (x % totient_func) 

        #<----------------------------------------------ENCRYPTION------------------------------------>
# C  = M ^ e (mod n )
def Encrypt(m, n, e):
    #if( len( str(MsgToNumber(m)) ) >  len(str(n-1))):
    if( MsgToNumber(m) >  (n-1)):
        M = Split_Msg(m, n)
        #print("Messages arr",M)
        c = []
        for i in range (len(M)):
            # print(len(str(MsgToNumber(M[i]))))
            c.append(Mod_exp(MsgToNumber(M[i]), e, n))
    else:
        #print(MsgToNumber(m))
        c = Mod_exp(MsgToNumber(m), e, n)
 #       print(c, "okkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")

    return c
#<----------------------------------------------DECRYPTION------------------------------------>
#  M = C ^ d (mod n)
def Decrypt(c, p, q, e):
    if(isinstance(c, int)):
  #      print("heeey okkk3 ", c)
        d = Mod_inverse(e, (p-1) * (q-1))
        print(d ,Mod_exp(c, d, p * q))
        return NumberToMsg(Mod_exp(c, d, p * q))
    else:
        msg = ''
        temp = ''
        d = (Mod_inverse(e, (p-1) * (q-1))) 
        for i in range(len(c)):
            temp += str(Mod_exp(c[i], d, p * q))
        msg = NumberToMsg(int(temp))

        return msg

#<--------------------------------------------------------------------------------------------->

'''
p = 7
q = 11
e = 13
n = p * q
m = "hello"
print("before RSA MESSAGE is ", m)
# print( len( str( MsgToNumber(m) ) ))
# print(len(str(n)))
c = Encrypt(m, n, e)
msg = Decrypt(c, p, q, e)
print("Message After RSA is  ", msg)


#print(Mod_inverse(35, 12*16))
 
# n = int(sys.argv[1])
# print(n+1)

'''




