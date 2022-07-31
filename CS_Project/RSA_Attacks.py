import RSA
from Crypto.Util import number

#<----------------------------------------------------brute force attack---------------------------------->
def bruteForce_attack(c, n, e):
    msg = ''
    i = 2
    while(i != n):   
        if( n % i == 0 ):
            #print(i, n//i)
            msg = RSA.Decrypt(c, i, n//i, e)
            return msg
        i+=1
    return msg





def CCA (c,p,q, e):
    
    n= p*q

    #chosen r        (should be coprime with n )
    r = number.getPrime(10)

    #try to get Alice to encrypt r
    r_enc = RSA.Mod_exp(r, e, n)
  
    #multiply C with encrypted r
    c_dash = (c * r_enc) %n                                 
  
    #send c_dash to bob and ask him to decrypt it
    m_dash = RSA.Decrypt(c_dash, p,q,e)

    #convert to number
    m_dash_n = RSA.MsgToNumber(m_dash)

    #now calculate r_inverse
    r_inv = RSA.Mod_inverse(r, n)

    #then multiply r_inverse with m_dash (decrypted c_dash) and convert back to string, now we have the Message
    M = RSA.NumberToMsg((m_dash_n * r_inv)%n)
    return (M)


    

p = 988808879341
q = 988808879323
e = 313
n = p * q
c = RSA.Encrypt("attack", n, e)
#m = bruteForce_attack(c, n, e)
#print("\nMessage after brute force attack is :", m)

print("\n CCA attack message : \n")
print(CCA(c, p, q, e))