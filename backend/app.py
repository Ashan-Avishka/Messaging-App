from flask import Flask, render_template, request, session, jsonify, g
from flask_session import Session
from flask_cors import CORS
import mysql.connector
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import base64
from db_config import get_db_connection
from auth_decorator import login_required
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
cors = CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:3000"}})  
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'session:'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True 
Session(app)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="cryptography"
)
cursor = db.cursor()

# fetch all users data from database
def get_all_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT * FROM users"  
    cursor.execute(query)
    
    users = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return users


# check that email is already exists or not
def email_exists(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    
    user = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return user is not None


# creating a new user
def create_user(username, email, password):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    connection.commit()


@app.route('/api/signup', methods=['POST'])
def signup():

    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if email_exists(email):
        return jsonify({"error": "User already exists"}), 400
    else:
        create_user(username, email, password)
        return jsonify({"message": "User created successfully"}), 201
    

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    users = get_all_users()
    user = next((u for u in users if u['email'] == email), None)
    
    if user and user['password'] == password:
        session['user_id'] = user['uid']
        response = jsonify({"message": "Login successful", "user": user})
        return response
    else:
        return jsonify({"error": "Invalid credentials"}), 401
  

@app.route('/api/users', methods=['GET'])
def user_list(): 
    current_user_id = session.get('user_id')
    try:
        users = get_all_users()
        filtered_users = [user for user in users if user['uid'] != current_user_id]
        return jsonify(filtered_users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/messages', methods=['POST'])
def encrypt():
    try:
        data = request.json
        message = data.get('text')
        sender_uid = session.get('user_id')
        reciever_uid = data.get('reciever')
        timestamp = data.get('timestamp')

        # Hash the sender and receiver UIDs
        hashed_sender_uid = hashlib.sha256(str(sender_uid).encode('utf-8')).hexdigest()
        hashed_reciever_uid = hashlib.sha256(str(reciever_uid).encode('utf-8')).hexdigest()

        # Generate RSA key pair for this session
        private_key_pem = session.get('private_key')
        if not private_key_pem:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            private_key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
            session['private_key'] = private_key_pem
        else:
            private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())
        
        public_key = private_key.public_key()

        # Generate a 3DES key
        des3_key = get_random_bytes(24)  # 3DES key size is 24 bytes
        cipher_des3 = DES3.new(des3_key, DES3.MODE_EAX)
        ciphertext, tag = cipher_des3.encrypt_and_digest(message.encode('utf-8'))

        # Encrypt the 3DES key with RSA
        encrypted_des3_key = public_key.encrypt(
            des3_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Insert encrypted message and keys into the database
        cursor.execute('INSERT INTO message (sendMessage, SUID, RUID, public_key, encrypted_des3_key, nonce, tag, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                       (base64.b64encode(ciphertext).decode('utf-8'), 
                        hashed_sender_uid,  
                        hashed_reciever_uid,
                        public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8'), 
                        base64.b64encode(encrypted_des3_key).decode('utf-8'),
                        base64.b64encode(cipher_des3.nonce).decode('utf-8'),
                        base64.b64encode(tag).decode('utf-8'),
                        timestamp)),
        
        db.commit()

        return jsonify({"message": "Message encrypted and stored successfully"})

    except Exception as e:
        return f"An error occurred: {str(e)}"
    



@app.route('/api/messages/decrypt', methods=['POST'])
def decrypt_messages():
    try:
        data = request.json
        sender_uid = session.get('user_id')
        receiver_uid = data.get('receiver')
        msg_type = ''

        # Hash the receiver UID to match the stored value
        hashed_receiver_uid = hashlib.sha256(str(receiver_uid).encode('utf-8')).hexdigest()
        hashed_sender_uid = hashlib.sha256(str(sender_uid).encode('utf-8')).hexdigest()

        # Retrieve the encrypted message and keys from the database for the specific user
        cursor.execute('SELECT sendMessage, SUID, RUID, public_key, encrypted_des3_key, nonce, tag, timestamp FROM message WHERE (RUID=%s AND SUID=%s) OR (RUID=%s AND SUID=%s)', 
                       (hashed_receiver_uid, hashed_sender_uid, hashed_sender_uid, hashed_receiver_uid))
        results = cursor.fetchall()
        
        if not results:
            print("No message found for this user")
            return jsonify({'message': "No message found for this user"})

        private_key_pem = session.get('private_key')
        if not private_key_pem:
            print("Private key not found")
            return jsonify({'message': "Private key not found"})

        # Ensure private_key_pem is in bytes format
        if isinstance(private_key_pem, str):
            private_key_pem = private_key_pem.encode('utf-8')

        # Deserialize the private key from PEM format
        private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())

        decrypted_messages = []
        timestamps = []
        msg_types = []

        for row in results:
            sendMessage, SUID, RUID, public_key_data, encrypted_des3_key, nonce, tag, timestamp = row

            # Determine the message type
            if RUID == hashed_receiver_uid and SUID == hashed_sender_uid:
                msg_type = 'sent'
            elif SUID == hashed_receiver_uid and RUID == hashed_sender_uid:
                msg_type = 'received'

            encrypted_message = base64.b64decode(sendMessage)
            encrypted_des3_key = base64.b64decode(encrypted_des3_key)
            nonce = base64.b64decode(nonce)
            tag = base64.b64decode(tag)

            # Decrypt the 3DES key using RSA
            des3_key = private_key.decrypt(
                encrypted_des3_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Decrypt the message using 3DES
            cipher_des3 = DES3.new(des3_key, DES3.MODE_EAX, nonce=nonce)
            decrypted_message = cipher_des3.decrypt_and_verify(encrypted_message, tag)

            decrypted_messages.append(decrypted_message.decode('utf-8'))
            timestamps.append(timestamp)
            msg_types.append(msg_type)

        return jsonify({
            'messages': decrypted_messages, 
            'timestamps': timestamps, 
            'msg_types': msg_types
        })
    except Exception as e:
        return jsonify({'message': f"An error occurred: {str(e)}"})
    



if __name__ == '__main__':
    app.run(debug=True)



















