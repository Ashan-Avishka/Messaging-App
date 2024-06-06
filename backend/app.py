from flask import Flask, render_template, request, session, jsonify
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

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)  # To allow cross-origin requests from your React frontend

# Dummy user data
# users = {
#     'user1@example.com': 'password1',
#     'user2@example.com': 'password2',
#     'user3@example.com': 'password3'
# }

user_data = {
    'user1@example.com': {'name': 'User One', 'email': 'user1@example.com'},
    'user2@example.com': {'name': 'User Two', 'email': 'user2@example.com'},
    'user3@example.com': {'name': 'User Three', 'email': 'user3@example.com'}
}

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
        return jsonify({"message": "Login successful", "user": user}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401









db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="cryptography"
)
cursor = db.cursor()

# @app.route('/')
# def login():
#     return render_template('Signup.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    try:
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, role))
        db.commit()

        cursor.execute('SELECT UID FROM users ORDER BY UID DESC LIMIT 1')
        UID = cursor.fetchone()
        global global_uid 
        global_uid = int(UID[0])

        return render_template('dashboard.html')
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        message = request.form['original-message']
        role = request.form['role']

        # Generate RSA key pair for this session
        private_key = session.get('private_key')
        if not private_key:
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
        
        # Deserialize the private key from PEM format
        private_key = serialization.load_pem_private_key(private_key, password=None, backend=default_backend())
        
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

        cursor.execute('SELECT * FROM users WHERE role= %s AND UID= %s', (role, global_uid))
        valid = cursor.fetchone()

        if valid:
            cursor.execute('INSERT INTO message (sendMessage, UID, public_key, encrypted_des3_key, nonce, tag) VALUES (%s, %s, %s, %s, %s, %s)',
                           (base64.b64encode(ciphertext).decode('utf-8'), 
                            global_uid, 
                            public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8'), 
                            base64.b64encode(encrypted_des3_key).decode('utf-8'),
                            base64.b64encode(cipher_des3.nonce).decode('utf-8'),
                            base64.b64encode(tag).decode('utf-8')))
            db.commit()
            return render_template('dashboard.html', encrypted_message="Message encrypted successfully")
        else:
            return render_template('dashboard.html', encrypted_message="No data sent")
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        dusername = request.form['decryption-username']
        dpassword = request.form['decryption-password'].encode('utf-8')

        cursor.execute("SELECT password FROM users WHERE username=%s AND UID = %s", (dusername, global_uid))
        valid = cursor.fetchone()

        if valid and valid[0] == hashlib.sha512(dpassword).hexdigest():
            cursor.execute('SELECT sendMessage, public_key, encrypted_des3_key, nonce, tag FROM message WHERE UID=%s', (global_uid,))
            result = cursor.fetchone()
            encrypted_message, public_key_data, encrypted_des3_key, nonce, tag = result

            encrypted_message = base64.b64decode(encrypted_message)
            encrypted_des3_key = base64.b64decode(encrypted_des3_key)
            nonce = base64.b64decode(nonce)
            tag = base64.b64decode(tag)

            # Load the sender's public key
            sender_public_key = serialization.load_pem_public_key(public_key_data.encode('utf-8'), backend=default_backend())

            # Retrieve the private key for decryption
            private_key_pem = session.get('private_key')
            if not private_key_pem:
                return jsonify({'message': "Private key not found"})

            # Deserialize the private key from PEM format
            private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())

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

            return jsonify({'message': decrypted_message.decode('utf-8')})
        else:
            return jsonify({'message': "Wrong user"})
    except Exception as e:
        return jsonify({'message': f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
