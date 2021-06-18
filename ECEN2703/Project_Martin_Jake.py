#Jake Martin
#Final Project

import secrets
import sympy
import time

#Code from the slides for extended Euclid GCD
def gcd(a: int, b: int):
    """Returns the gcd of a and b and the Bezout coefficients"""
    if b == 0:
        return (a, 1, 0)
    q, r = divmod(a, b)
    d, s, t = gcd(b, r)
    return d, t, s - q * t

#Translates a string into an integer encoding
def str_to_int(string: str) -> int:
    return int.from_bytes(str.encode(string), byteorder='big')

#Translates an integer encoding back into a string
def int_to_str(num: int) -> str:
    return num.to_bytes(num.bit_length()//8+1, byteorder='big').decode()

#Generate a new key of given length using python's most secure number generation
def new_key(length: int) -> int:
    return secrets.randbits(length);

#Encrypts a message using a OTP with a randomly generated key
def OTP_encrypt(message: str) -> (int, int):
    M = str_to_int(message)
    K = new_key(M.bit_length())
    return (M^K, K)

#Decrypts a message encrypted using OTP with a ciphertext and key
def OTP_decrypt(C: int, K: int) -> int:
    message = int_to_str(C^K)
    return message

#Simulates a message receiver for RSA
class Receiver:
    def __init__(self, P: int, Q: int):
        self.p = P
        self.q = Q
        self.e = 65537 #Since this number is usually used for RSA
        
        self.d = gcd(self.e, (self.p-1)*(self.q-1))[1]
    
    def get_public_key(self) -> (int, int):
        n = self.p * self.q
        return (n, self.e)
    
    def decrypt(self, C: int) -> str:
        M = pow(C, self.d, self.p * self.q)
        return int_to_str(M)

#Simulates a message sender for RSA
class Sender:
    def __init__(self, rec: Receiver):
        rec_public = rec.get_public_key()
        self.n = rec_public[0]
        self.e = rec_public[1]
    
    def encrypt(self, message: str) -> int:
        M = str_to_int(message)
        C = pow(M, self.e, self.n)
        return C

#Brute-force find the prime factors of semiprime n
def n_factor(n: int) -> (int, int):
    num_tries = 0
    for prime1 in range(2, n):
        if not sympy.isprime(prime1):
            prime1 = sympy.nextprime(prime1)
        
        num_tries += 1
        prime2 = n//prime1
        if sympy.isprime(prime2) and (prime1 * prime2 == n):
            print("Got it after", num_tries, "guesses")
            return (prime1, prime2)
        else:
            print("Failed guess #", num_tries)
            time.sleep(0.001)
        
    return (-1, -1)

    
print("\n" + 100*"-")
mode = input("Enter encryption mode (RSA/OTP): ")
if mode == "OTP":
    text = input("Enter your text to encrypt: ")
    print("\nMessage:  ", text)

    #Encryption scheme using OTP
    print("\nUsing OTP...")
    encr1 = OTP_encrypt(text)
    print("Encoded:  ", hex(str_to_int(text)))
    print("\nEncrypted:", hex(encr1[0]))
    print("Key:      ", hex(encr1[1]))
    print("\nDecrypted:", OTP_decrypt(encr1[0], encr1[1]))
    print("\n" + 100*"-")
    
    #Attempt attack
    attack = input("\nPerform attack(Y/N): ")
    if(attack[0] == 'Y'):
        print("OK, starting brute-force key-guessing calculation...")
        print("\nGuessing the key by counting from zero would take", encr1[1], "tries.")
        print("On a 2GHz processor that could run decrypt in 10 cycles (very fast), it")
        print("would take", (encr1[1]*10) / (2000000000*60*60*24), "days to test enough keys")
        print("to find the correct decryption.\n")
        print("Additionally, it would generate vast quantities of false decryptions in")
        print("the process, making brute-force practically useless on OTP")
                
    else:
        print("OK, exiting now!")

elif mode == "RSA":
    text = input("Enter your text to encrypt (Currently 8char max for this mode): ")
    print("\nMessage:  ", text)
    
    #Encryption scheme using RSA
    print("\nUsing RSA...")

    Bob = Receiver(0x10000000f, 0x10000003d) #Small, but easily testable keys
    Alice = Sender(Bob)
    pub_key = Bob.get_public_key()

    encr2 = Alice.encrypt(text)
    print("Encoded:  ", hex(str_to_int(text)))
    print("\nEncrypted:", hex(encr2))
    print("Key n:    ", hex(pub_key[0]))
    print("\nDecrypted:", Bob.decrypt(encr2))
    print("\n" + 100*"-")
    
    #Attempt attack
    attack = input("\nPerform attack(Y/N): ")
    if(attack[0] == 'Y'):
        print("OK, starting n-factoring key-finding...")
        priv_keys = n_factor(pub_key[0])
        print("Found! The private key values are", priv_keys)
        d = gcd(pub_key[1], (priv_key[0] - 1)*(priv_key[1] - 1))[1]
        M = pow(encr2, d, pub_key[0])
        print("Now, using the keys and public info, the message can be ")
        print("decryped as ", int_to_str(M))
        a = 0
        while True:
            a += 1
            print(a, end="")
            time.sleep(10)
    
else:
    print("Error, unsupported mode, please run again!")

time.sleep(3)