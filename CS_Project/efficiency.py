import RSA
import RSA_Attacks
import math
import random
import timeit
import matplotlib.pyplot as plt 
from Crypto.Util import number






#n = range(6, 900000000009000000000090000000000900000000009000000000090000000000900000000009000000000090000000000)
t = []
n = range(129, 40000000)
msg = "Hello I am Ayman"
for i in n:
    size_bits = i.bit_length()
    size_p = int(size_bits / 2)
    p = number.getPrime(size_p)

    q = number.getPrime(size_p)
    while (p == q):
        q = number.getPrime(size_p)
    
    sample_n = p * q
    phi_n = (p-1) * (q - 1)
        

    e = number.getPrime(phi_n.bit_length() - 1)
    
    c = RSA.Encrypt("attack", sample_n, e)
    start = timeit.default_timer()
    m = RSA_Attacks.bruteForce_attack(c, sample_n, e)
    stop = timeit.default_timer()
    time = stop - start
    t.append(time)
    
    
plt.plot(n, t) 
plt.xlabel('n (decimal)') 
plt.ylabel('time to encrypt (seconds)') 
plt.title('Brute Force graph') 
plt.show() 