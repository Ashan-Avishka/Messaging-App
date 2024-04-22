import encryption
import decryption
import createKey
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import os

class App:
    @staticmethod
    def KeyGeneration():
        createKey.generate_ecc_key()
        
    @staticmethod
    def DataEncrypt(message, private_key):
        encryption.encrypt(message, private_key)
    
    @staticmethod
    def DataDecrypt(private_key):
        decryption.decrypt(private_key)
        
# create key
App.KeyGeneration()

private_key = ec.generate_private_key(ec.SECP256R1(), default_backend()) 

# Encryption
message = input("Please Enter The Message: ")
App.DataEncrypt(message, private_key)

# Decryption
App.DataDecrypt(private_key)

