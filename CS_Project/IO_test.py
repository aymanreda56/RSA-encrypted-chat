from pickle import FALSE
import RSA
import math
from Crypto.Util import number




mode = int(input("\n enter the mode, 0 for manual entry, 1 for autogeneration\n"))

while (mode != 0 and mode != 1):
    mode = int(input("\n incorrect entry ! \n plz enter 1 or 0 !\n"))

if(mode == 0):
    x = input("\n enter sample text \n")

    p = int(input("\n enter P"))
    while (not RSA.isPrime(p) or p < 2):
        p = int(input("\n wrong p, enter a prime number plz \n"))


    q = int(input("\n enter q or enter 0 to autogenerate"))
    while(q != 0 and not RSA.isPrime(q) or q == 1 or q < 0):
        q = int(input("\n wrong q, enter a prime number plz \n"))

    # generate a q just larger than p, to keep n very large and increase confusion
    if(q == 0):
        q = number.getPrime(p.bit_length())
        while (q == p):
            q = number.getPrime(p.bit_length())

    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = int(input("\n enter e or enter 0 to autogenerate\n"))
    # check e constraints or generate randomly
    if(e):
        while ((math.gcd(e, phi_n) != 1) and (e < phi_n) and (e > 1)):
            e = int(input("\n incorrect e ! \n e must be coprime with phi_n and 1 < e < phi_n \n enter e again or enter 0 to autogenerate plz.\n"))
            if(e == 0):
                break

    # generate random e and pick only the prime one
    if(e == 0):
        e = number.getPrime(phi_n.bit_length() - 1)
        if(e < 10 or e < 1):
            e == 3



    



elif(mode):
    x = input("\n enter sample text \n")
    p = number.getPrime(64)

    q = number.getPrime(64)
    while (p == q):
        q = number.getPrime(64)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = number.getPrime(phi_n.bit_length() - 1)
    while(math.gcd(e, phi_n) != 1 or (e >= phi_n)):
        e = number.getPrime(phi_n.bit_length() - 1)




d = RSA.Mod_inverse(e, phi_n)
MSG = RSA.Encrypt(x, n, e)
    
#in case of array of messages after splitting
#if(isinstance(MSG, list)):
#    MSG = ''.join(str(MSG))         #joining the split message again to only one string

decrypted = RSA.Decrypt(MSG, p, q, e)



print("\n p = \n")
print(p)
print("\n q = \n")
print(q)
print("\n n = \n")
print(n)
print("\n phi_n = \n")
print(phi_n)
print("\n e = \n")
print(e)
print("\n d = \n")
print(d)
print("\n text = \n")
print(x)
print("\n cypherText = \n")
print(MSG)
print("\n decrypted text = \n")
print(decrypted)


# now we have p, q, n, phi_n, e and d
