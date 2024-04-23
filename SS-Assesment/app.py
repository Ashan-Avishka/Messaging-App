import encryption
import decryption
import createKey
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

from flask import Flask, render_template, request
from flask_socketio import SocketIO, send 

# server = Flask(__name__)

app = Flask(__name__)
app.config['SECRET'] = "secret!123"
socketio = SocketIO(app, cors_allowed_origin="*")

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

# @server.route("/sendMsg", methods=["GET", "POST"])
# def send_message():

#     form_data = request.form

#     # print(form_data.get("message"))
    
#     # # Encryption
#     App.DataEncrypt(form_data.get("message"), private_key)

#     # # Decryption
#     App.DataDecrypt(private_key)

#     return render_template("client.html")

# server.run(debug=True)

@socketio.on('message')
def handle_message(message):
    
    if message != "User connected!":

        # # Encryption
        App.DataEncrypt(message, private_key)

        # # Decryption
        App.DataDecrypt(private_key)

        # # sned the message to frontend
        send(message, broadcast=True)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host="localhost")