from flask import Flask, request, jsonify, redirect, url_for

app = Flask(__name__)


users = {
    "test@example.com": "password123"
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Authentication logic (replace with real authentication)
    if email in users and users[email] == password:
        # Generate a token (this is a dummy example, implement proper JWT token)
        token = "dummy_token"
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Login failed"}), 401

@app.route('/home')
def home():
    return "Welcome to the home page!"

if __name__ == '__main__':
    app.run(debug=True)
