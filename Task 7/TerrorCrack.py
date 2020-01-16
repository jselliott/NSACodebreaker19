from __future__ import print_function
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Cipher import blockalgo
from Crypto.Hash import HMAC
from Crypto.Hash import SHA256
import base64
import hashlib
import sqlite3

"""

HOW TO USE THIS SCRIPT

In the keygen program, there are three values that are loaded in memory 
based on the size of key that is requested (512,1024,or 2048), two base-64
strings and a public key. They will automatically be extracted.

This program works as a chain where it uses the cracked 256-bit key to crack the 512,
then the 1024, and finally the 2048-bit key for a TerrorTime user.

Setup:

- Download keygen executable for Task 7 and place it in same folder
- Copy target public key into file called target.key in same folder
- Download clientDB.db from Task 3 into same folder
- Enter target username in XNAME variable in script
- Enter app pin from Task 4 in PIN variable in script
- Run once and script will prompt you to run Yafu factoring program
- After factoring, enter factors for P and Q in variables below
- Run again to complete cracking/patching process
- Upload modified clientDB.db to emulator
- Log in using username and pin from Task 4
- Read messages and destroy terrorist plans!

"""

try:
    long
except NameError:
    long = int

#256-bit factors (ENTER FACTORS FROM YAFU HERE)
P = 0
Q = 0

#Enter username and pin from task 4 here
XNAME = ""
PIN = ""

class KeyRecover:

    def __init__(self,key1,key2,pub,priv,keysize=512):

        self.R1 = key1
        self.R2 = key2
        self.pub = pub
        self.priv = priv
        self.e = 65537
        self.keysize = keysize

    def permute_key(self,R):

        if self.keysize == 512:

            return int(hashlib.sha256(long_to_bytes(R)).hexdigest(), 16)

        elif self.keysize == 1024:

            return int(hashlib.sha512(long_to_bytes(R)).hexdigest(), 16)

        else:

            R1_1 = hashlib.sha512(long_to_bytes(R)).hexdigest()
            R1_2 = hashlib.sha512(long_to_bytes(int(R1_1, 16))).hexdigest()

            return int(R1_1 + R1_2,16)

    def recover(self,target):

        print("\nRecovering Modulus: \t"+target)

        #Target public key
        T = int(target,16)

        #Cut off the first half
        mid = len(target) // 2
        part1 = target[:mid]

        print("First Half: \t\t\t"+str(part1))

        part1 = int(part1,16)

        print("R1: \t\t\t\t\t"+str(self.R1))
        print("R2: \t\t\t\t\t"+str(self.R2))

        for x in range(2):

            for i in range(1000):

                #Get the encrypted part
                encrypted = (part1+x) ^ (self.R2+i)

                #Decrypt it with the private key
                decrypted = pow(encrypted,self.priv,self.pub)

                R1 = self.R1

                #Limit so we don't sit here all day
                for limit in range(100):

                    for j in range(10):

                        #Try to get back the original prime P
                        prime = decrypted ^ R1

                        #If it is evenly divisible from T then we found it
                        if T%prime == 0:

                            print("Recovered P: \t\t\t"+str(prime))
                            print("Recovered Q: \t\t\t"+str(T//prime))
                            return prime,T//prime,self.get_private_key_from_p_q_e(prime,T//prime,self.e)

                        #Else increment key1
                        R1+=1

                    #After 10 tries, hash key1 and keep trying
                    R1 = self.permute_key(R1)

        return None,None,None


    def get_private_key_from_p_q_e(self, p, q, e):

        d = 0

        #Calculate phi_n
        phi_n = (p-1) * (q-1)

        #d is the modular inverse of e and phi_n
        d = self.modinv(e,phi_n)

        return d

    def modinv(self,a,n):

        t = 0
        r = n
        nt = 1
        nr = a

        while nr != 0:
            q = r//nr
            t,nt = nt,t-q*nt
            r,nr = nr,r-q*nr

        if r > 1:
            return 0
        if t < 0:
            t += n

        return t

def b64i(s):
    #print base64.b64decode(s).encode("hex")
    return int(base64.b64decode(s).encode("hex"),16)

def wrapkey(s):
    return "-----BEGIN PUBLIC KEY-----\n"+s.strip()+"\n-----END PUBLIC KEY-----\n"

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

def encryptClientBytes(pin,message):

    prf = lambda p, s: HMAC.new(p, s, SHA256).digest()
    key = PBKDF2(pin,hashlib.sha256(pin).digest(),32,10000,prf)
    cipher = AES.new(key,mode=blockalgo.MODE_ECB)

    return cipher.encrypt(pad(message))

try:
    f = open("keygen","rb")

except IOError:
    print("Error: You must put keygen in the same folder as script.")
    exit()

# Extract key values from keygen executable
keys = f.read().strip().split("-----")

PK_256 = wrapkey(keys[2])
PK_512 = wrapkey(keys[6])
PK_1024 = wrapkey(keys[10])

PK_256 = RSA.importKey(PK_256)
PK_512 = RSA.importKey(PK_512)
PK_1024 = RSA.importKey(PK_1024)

r_keys = keys[12].split("=")

R1_256 = r_keys[0]+"="
R2_256 = r_keys[1]+"="
R1_512 = r_keys[2]+"=="
R2_512 = r_keys[4]+"=="
R1_1024 = r_keys[6]+"="
R2_1024 = r_keys[7]+"="

R1_256 = b64i(R1_256)
R2_256 = b64i(R2_256)
R1_512 = b64i(R1_512)
R2_512 = b64i(R2_512)
R1_1024 = b64i(R1_1024)
R2_1024 = b64i(R2_1024)


if P == 0 or Q == 0:
    print("You must manually factor the 256-bit public key for this task.")
    print("Please download Yafu and factor the number below with the command:\n")
    print("yafu-x64 factor(" + str(PK_256.n)+")")
    print("\n\nOnce you have the factors, enter them for P and Q in this script and rerun it.")
    exit()

if XNAME=="" or PIN == "":
    print("Please enter the target username and the pin from task 4 at the top of the script and rerun it.")
    exit()

#Get the initial private key for the 256-bit key
rec = KeyRecover(0,0,0,0)
D = rec.get_private_key_from_p_q_e(P,Q,65537)

print("First Private Key: "+str(D))

print("\n--- Recovering 512 Bit RSA Key ---")

rec = KeyRecover(R1_256,R2_256,PK_256.n,D,512)
P,Q,D = rec.recover('{:x}'.format(int(PK_512.n)))
print("Private Key: \t\t\t"+str(D))

print("\n--- Recovering 1024 Bit RSA Key ---")

rec = KeyRecover(R1_512,R2_512,PK_512.n,D,1024)
P,Q,D = rec.recover('{:x}'.format(int(PK_1024.n)))
print("Private Key: \t\t\t"+str(D))


try:
    f = open("target.key","rb")

except IOError:
    print("Error: You must put target.key (containing target public key) in the same folder as script.")
    exit()

PK_2048_PEM = f.read()
PK_2048 = RSA.importKey(PK_2048_PEM)

print("\n--- Recovering Leader Key ---")

T = '{:x}'.format(int(PK_2048.n))

rec = KeyRecover(R1_1024,R2_1024,PK_1024.n,D,2048)
P,Q,D = rec.recover(T)
print("Private Key: \t\t\t"+str(D))
print("\n\n")

if D is None:
    print("Sorry, the program failed to crack this key. :(")
    exit()

RSAKey = RSA.construct((int(T,16),long(65537),D,P,Q))

FinalKey = RSAKey.exportKey()
#print FinalKey.encode("hex")

print("\nCracked user key!")

print("Patching clientDB.db....")

try:
    conn = sqlite3.connect('clientDB.db')

except sqlite3.DatabaseError:
    print("Error: You must put clientDB.db in the same folder as script.")
    exit()

encodedKey = encryptClientBytes(PIN,FinalKey)

query = "UPDATE Clients SET xname=?, pubkey=?, privkey=?"

try:
    conn.text_factory = str
    cursor = conn.cursor()
    cursor.execute(query, (XNAME, PK_2048_PEM+"\n",sqlite3.Binary(encodedKey)))
    conn.commit()
    cursor.close()
    conn.close()

except sqlite3.DatabaseError:
    print("Error: Something went wrong while patching the DB. You may have to put in the encoded private key bytes yourself (below):")
    print("\n\n"+encodedKey.encode("hex"))
    exit()

print("\n** All done! Upload the patched database to your emulator and log in to view this user's messages. **")