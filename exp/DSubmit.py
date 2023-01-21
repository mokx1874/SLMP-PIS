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
from typing import Optional, Union
import doctest
import PISexp.oblivious

class data(PISexp.oblivious.ristretto.point):
    """
    Wrapper class for a bytes-like object that corresponds to a piece of data
    that can be masked.
    """
    @classmethod
    def hash(cls, argument: Union[str, bytes]) -> data: # pylint: disable=arguments-renamed
        if not isinstance(argument, (bytes, bytearray, str)):
            raise TypeError(
                'can only hash a string or bytes-like object to a data object'
            )

        argument = argument.encode() if isinstance(argument, str) else argument
        return bytes.__new__(cls, PISexp.oblivious.ristretto.point.hash(argument))

    @classmethod
    def from_base64(cls, s: str) -> data:
        return bytes.__new__(cls, PISexp.oblivious.ristretto.point.from_base64(s))

    def __new__(cls, bs: Optional[bytes] = None) -> data:
        return bytes.__new__(cls, PISexp.oblivious.ristretto.point(bs))

    def __truediv__(self: data, argument: mask) -> data:
        return data((~argument) * self)

    def to_base64(self: data) -> str:
        return PISexp.oblivious.ristretto.point(self).to_base64()

class mask(PISexp.oblivious.ristretto.scalar):
    """
    Wrapper class for a bytes-like object that corresponds to a mask.
    """
    @classmethod
    def random(cls) -> mask:
        return bytes.__new__(cls, PISexp.oblivious.ristretto.scalar())

    @classmethod
    def hash(cls, argument: Union[str, bytes]) -> mask: # pylint: disable=arguments-renamed
        if not isinstance(argument, (bytes, bytearray, str)):
            raise TypeError(
                'can only hash a string or bytes-like object to a mask object'
            )

        argument = argument.encode() if isinstance(argument, str) else argument
        return bytes.__new__(cls, PISexp.oblivious.ristretto.scalar.hash(argument))

    @classmethod
    def from_base64(cls, s: str) -> mask:
        return bytes.__new__(cls, PISexp.oblivious.ristretto.scalar.from_base64(s))

    def __new__(cls, bs: Optional[bytes] = None) -> mask:

        return bytes.__new__(cls, PISexp.oblivious.ristretto.scalar(bs))

    def __invert__(self: mask) -> mask:
        return mask(~PISexp.oblivious.ristretto.scalar(self))

    def mask(self: mask, argument: data) -> data:
        return data(PISexp.oblivious.ristretto.scalar(self) * argument)

    def __call__(self: mask, argument: data) -> data:
        return data(PISexp.oblivious.ristretto.scalar(self) * argument)

    def __mul__(self: mask, argument: data) -> data:
        return data(PISexp.oblivious.ristretto.scalar(self) * argument)

    def unmask(self: mask, argument: data) -> data:
        return data(PISexp.oblivious.ristretto.scalar(~self) * argument)

    def to_base64(self: mask) -> str:
        return PISexp.oblivious.ristretto.scalar(self).to_base64()

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

    def bit_arr_to_bytes(arr: np.ndarray) -> bytes:
        """
        :param arr: 1-d uint8 numpy array
        :return: bytes, one element in arr maps to one bit in output bytes, padding in the left
        """
        n = arr.size
        pad_width = (8 - n % 8) % 8
        arr = np.pad(arr, pad_width=((pad_width, 0),), constant_values=0)
        bs = bytes(np.packbits(arr).tolist())

        return int_to_bytes(n) + bs

    def bytes_to_bit_arr(data: bytes) -> np.ndarray:
        """
        :param data: bytes, first 4 bytes is array length, and the remaining is array data
        :return:
        """
        prefix_length = 4
        n = bytes_to_int(data[:prefix_length])
        while (n + 7) // 8 != len(data) - prefix_length:
            prefix_length += 4
        arr = np.array(list(data[prefix_length:]), dtype=np.uint8)
        res = np.unpackbits(arr)[-n:]
        return res

    K = random.getrandbits(128)
# A = re.findall(r'.{,30}''.',str(K))
    def send(self, m0: bytes, m1: bytes):
        if not self.is_available():
            raise ValueError(
                "The sender is not available now. "
                "The sender may be not prepared or have used all ot keys"
            )

        key0 = int_to_bytes(self._index) + bit_arr_to_bytes(self._q[self._index, :])
        key1 = int_to_bytes(self._index) + bit_arr_to_bytes(
            self._q[self._index, :] ^ self._s
        )

        cipher_m0 = shake.encrypt(key0, m0)
        cipher_m1 = shake.encrypt(key1, m1)

        self._index += 1

	for i in range(m):
		PRF_i = hash(str(i))
		ES_i = encrypt(str(i), str(PRF_i))
		ER_i = encrypt(str(PRF_i), str(kab))
		sh = bytes()
		root = ''
		for j in range(n):
			Fj = encrypt(str(i), str(K))
			for k in range(len(Fj)):
				sh += Fj[k]
		# EncRe_i = encrypt(str(PRF_i + sh), str(kab))
		# HRE = hash1(str(PRF_i + sh))
		# root += str(HRE)                                                    #end
	end_time = time.time()
	time1 = end_time-start_time
	print('time = ',time1)
	#print('Running time: %s Seconds'%(end_time-start_time))
