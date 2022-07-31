import RSA
import RSA_Attacks
import math
import random
import timeit
import matplotlib.pyplot as plt 
from Crypto.Util import number




#n = range(6, 900000000009000000000090000000000900000000009000000000090000000000900000000009000000000090000000000)
t = []
n = range(129, 1200)
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
        
    if(phi_n > 30):
        e = 29
    else:
        e = random.randint(2, phi_n - 1)
        while(math.gcd(e, phi_n) != 1):
            e = random.randint(2, phi_n - 1)

    start = timeit.default_timer()
    for i in range(20):
        encryptedmsg = RSA.Encrypt(msg, sample_n, e)
    stop = timeit.default_timer()
    time = (stop - start) / 20.0
    t.append(time)
    
    
plt.plot(n, t, marker = "o") 
plt.xlabel('n (decimal)') 
plt.ylabel('time to encrypt (seconds)') 
plt.title('efficiency graph') 
plt.show() 