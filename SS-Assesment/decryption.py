from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import os

def decrypt(private_key):
    try:
        # Load ECC public key
        with open('public_key_ecc.pem', 'rb') as public_key_file:
            public_key = serialization.load_pem_public_key(
                public_key_file.read(),
                backend=default_backend()
            )

        # Read IV and encrypted message from file
        with open('encrypted_message', 'rb') as encrypted_message_file:
            iv = encrypted_message_file.read(16)
            encrypted_message = encrypted_message_file.read()

        # Perform ECDH key exchange to derive shared key
        shared_key = private_key.exchange(ec.ECDH(), public_key)

        # Derive key using HKDF
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
            backend=default_backend()
        ).derive(shared_key)

        # Decrypt the message using AES
        cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()

        print("Decryption successful:")
        print(decrypted_message.decode())
    except Exception as e:
        print("An error occurred:", e)




