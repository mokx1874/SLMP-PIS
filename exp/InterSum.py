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
from __future__ import annotations
from typing import Union, Optional
import doctest
import base64

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


def key_base64() -> str:
    """
    Create a :obj:`~bcl.bcl.secret` key to be maintained by the service and return
    its Base64 UTF-8 string representation.
    >>> len(base64.standard_b64decode(key_base64()))
    32
    """
    return base64.standard_b64encode(key()).decode('utf-8')

def mask(
        k: bcl.secret,
        m: Optional[bcl.cipher] = None,
        d: Optional[oprf.data] = None
    ) -> Union[bcl.cipher, oprf.data]:
    """
    Function implementing a masking service. If only a :obj:`~bcl.bcl.secret`
    key is supplied, this function creates a :obj:`~oprf.oprf.mask` object,
    encrypts it using the supplied :obj:`~bcl.bcl.secret` key, and returns
    the resulting :obj:`~bcl.bcl.cipher` object. If an encrypted
    :obj:`~oprf.oprf.mask` object and a :obj:`~oprf.oprf.data` object are
    also supplied, it decrypts the supplied :obj:`~bcl.bcl.cipher` object into a
    :obj:`~oprf.oprf.mask` object, applies it to the :obj:`~oprf.oprf.data`
    object, and returns the result.
    >>> k = key()
    >>> m = mask(k)
    The two objects ``k`` and ``m`` can now be used to mask data.
    >>> d = oprf.data.hash('abc')
    >>> mask(k, m, d) == oprf.mask(bcl.symmetric.decrypt(k, m))(d)
    True
    If an encrypted :obj:`~oprf.oprf.mask` object is supplied, a
    :obj:`~oprf.oprf.data` object must also be supplied.
    >>> mask(k, m)
    Traceback (most recent call last):
      ...
    ValueError: data to be masked must be supplied
    """
    # If no mask is supplied, return a new encrypted mask.
    if m is None:
        return bcl.symmetric.encrypt(k, oprf.mask())

    if d is None:
        raise ValueError('data to be masked must be supplied')

    # Return the masked data.
    return oprf.mask(bcl.symmetric.decrypt(k, bcl.cipher(m)))(d)

def handler(k: bcl.secret, request: Union[str, dict]) -> dict:
    """
    Wrapper for service function that accepts inputs as a JSON
    string or a Python :obj:`dict` instance (*e.g.*, for use within a route
    defined using the `Flask <https://flask.palletsprojects.com>`__
    library).
    It is possible to request a new encrypted mask. Note that an empty request
    *must* be supplied to the handler.
    >>> k = key()
    >>> r = handler(k, {})
    >>> r['status']
    'success'
    >>> r = handler(k, '{}')
    >>> r['status']
    'success'
    The encrypted mask can be used to mask data. Note that it is the
    responsibility of the service implementation to maintain and supply
    the :obj:`~bcl.bcl.secret` key to the handler.
    >>> m = oprf.mask.from_base64(r['mask'][0])
    >>> d = oprf.data.hash('abc')
    >>> r = handler(k, {'mask': [m.to_base64()], 'data': [d.to_base64()]})
    >>> r['status']
    'success'
    The example below reproduces the example above, but submits the request
    to the handler as a string.
    >>> (m_str, d_str) = (str(m.to_base64()), str(d.to_base64()))
    >>> s = '{"mask": ["' + m_str + '"], "data": ["' + d_str + '"]}'
    >>> r = handler(k, s)
    >>> r['status']
    'success'
    The example below confirms that the response contains the masked data.
    >>> oprf.data.from_base64(r['data'][0]) == (
    ...     oprf.mask(bcl.symmetric.decrypt(k, bcl.cipher(m)))(d)
    ... )
    True
    If the supplied request is not valid (*e.g.*, if the data is missing),
    then the returned response indicates failure.
    >>> r = handler(k, {'mask': [m.to_base64()]})
    >>> r['status']
    'failure'
    """
    # Convert request to a dictionary if it is a JSON string.
    request = json.loads(request) if isinstance(request, str) else request

    # Convert the key from Base64 if it is a string.
    k = base64.standard_b64decode(k) if isinstance(k, str) else k

    # Extract arguments.
    m = oprf.mask.from_base64(request['mask'][0]) if 'mask' in request else None
    d = oprf.data.from_base64(request['data'][0]) if 'data' in request else None

    if m is None:
        return {
            'status': 'success',
            'mask': [base64.standard_b64encode(mask(k, m, d)).decode('utf-8')]
        }

    if m is not None and d is not None:
        return {
            'status': 'success',
            'data': [base64.standard_b64encode(mask(k, m, d)).decode('utf-8')]
        }

    return {'status': 'failure'}

m = int(input("input m:"))
n = int(input("input n:"))
start_time = time.time()

K = random.getrandbits(128)
# A = re.findall(r'.{,30}''.',str(K))
for i in range(m):
    sum = str(0)
    PRF_i = hash(str(i))
    sh = bytes()
    root = ''
    for j in range(n):
        Fj = hash(str(i))
        sh  += Fj
        # for k in range(len(Fj)):
        #     sh += Fj[k]
    EncRe_i = encrypt(str(PRF_i + sh), str(kab))
    sum  += str(EncRe_i)                                              #end
end_time = time.time()
time1 = end_time-start_time
print('time1 = ',time1)
#print('Running time: %s Seconds'%(end_time-start_time))
