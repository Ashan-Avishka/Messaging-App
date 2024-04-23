import encryption
import decryption
import createKey
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import os

from flask import Flask, render_template, request
server = Flask(__name__)

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

@server.route("/sendMsg", methods=["GET", "POST"])
def send_message():

    form_data = request.form
    
    # # Encryption
    App.DataEncrypt(form_data["message"], private_key)

    # # Decryption
    App.DataDecrypt(private_key)

    return render_template("sendMsg.html")

server.run(debug=True)
