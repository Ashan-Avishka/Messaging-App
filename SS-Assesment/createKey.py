from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import os

def generate_ecc_key():
    # Create private and public ECC keys
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()

    # Serialize and write the keys
    private_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM, 
                                             format=serialization.PrivateFormat.PKCS8,
                                             encryption_algorithm=serialization.NoEncryption())
    public_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                         format=serialization.PublicFormat.SubjectPublicKeyInfo)

    with open('private_key_ecc.pem', 'wb') as private_key_file:
        private_key_file.write(private_pem)
        
    with open('public_key_ecc.pem', 'wb') as public_key_file:
        public_key_file.write(public_pem)

if __name__ == "__main__":
    generate_ecc_key()
