from Crypto.Random import random
from Crypto.Cipher import AES
from Crypto.Hash import HMAC
import base64
import binascii
import random
import hashlib
import numpy as np
import re
import math
import sys
from ECDH1 import kab
import time


def hash1(str):
	result = hashlib.md5(str.encode())
	return result.digest()

def hash(str):
	"""
	Returns the digest of the SHA-256 hash function for use as the key in our AES-256 encryption.
	"""
	result = hashlib.sha256(str.encode())
	return result.digest()                  #二进制

def hmac(key, data):
	"""
	MD5
	"""
	result = HMAC.new(key.encode(), data.encode())
	return result.hexdigest()               #16进制

def encrypt(message, exchanged_value):
	"""
	Encrypts the message using the symmetric encryption scheme AES-256 with x-coordinate of the shared secret as a key.
	"""
	data = message.encode("utf8")
	# data = message
	key = hash(exchanged_value)
	cipher = AES.new(key,AES.MODE_EAX)
	nonce = cipher.nonce
	ciphertext,tag = cipher.encrypt_and_digest(data)
	#return (ciphertext)
	return(nonce,ciphertext,tag)
# encrypted = encrypt(message_in,str(abP[0]))

def decrypt(encrypted, exchanged_value):
	"""
	Decrypting the message. The variable "encrypted" is a tuple (nonce,ciphertext,tag).
	Since bob has the shared secret, he can make the appropriate key.
	For an attacker to (naively) obtain the correct key, they must solve the ECDLP.
	"""
	key = hash(exchanged_value)
	cipher = AES.new(key, AES.MODE_EAX, nonce = encrypted[0])
	plaintext = cipher.decrypt(encrypted[1])
	try:
		cipher.verify(encrypted[2])
	except ValueError:
		print("The message could not be verified!")
	return plaintext.decode("utf8")
# decrypted_message = decrypt(encrypted,str(abP[0]))

m = int(input("input m:"))
n = int(input("input n:"))
start_time = time.time()

K = random.getrandbits(128)
# A = re.findall(r'.{,30}''.',str(K))
for i in range(m):
    PRF_i = hash(str(i))
    sh = bytes()
    root = ''
    for j in range(n):
        Fj = encrypt(str(i), str(K))
        for k in range(len(Fj)):
            sh += Fj[k]
    EncRe_i = encrypt(str(PRF_i + sh), str(kab))
    HRE = hash1(str(PRF_i + sh))
    root += str(HRE)                                                    #end
end_time = time.time()
time1 = end_time-start_time
print('time1 = ',time1)
#print('Running time: %s Seconds'%(end_time-start_time))





