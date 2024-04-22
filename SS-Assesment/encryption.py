from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import os


def encrypt(message, private_key):
    try:
        # Load ECC public key
        with open('public_key_ecc.pem', 'rb') as public_key_file:
            public_key = serialization.load_pem_public_key(
                public_key_file.read(),
                backend=default_backend()
            )

        # Generate a random AES key
        aes_key = os.urandom(32)

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

        # Encrypt the message using AES
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()

        # Write IV and encrypted message to file
        with open('encrypted_message', 'wb') as encrypted_message_file:
            encrypted_message_file.write(iv + encrypted_message)

        print("Encryption successful.")
    except Exception as e:
        print("An error occurred:", e)
