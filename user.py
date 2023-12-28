from flask import Blueprint, request, jsonify, make_response
from functools import wraps
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from auth import roles_required
from database import Database
import json

db = Database()
with open("config.json") as config_file:
    jwt_config = json.load(config_file)["jwt"]

user_bp = Blueprint('user', __name__)
#======================================================
with open("config.json") as config_file:
    email_config = json.load(config_file)["email"]

server = smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"])
server.starttls()
senderEmail = email_config["sender_email"]
server.login(senderEmail, email_config["sender_password"])

msg = MIMEMultipart()
msg['From'] = senderEmail
msg['To'] = '   '
msg['Subject'] = 'Subject: Your Authentication Status to the application'
#======================================================



@user_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        roles = data['roles']
        email = username

        existing_user = db.execute_query("SELECT username FROM USER")
        if username in existing_user:
            body = "username already exists" 
            msg.attach(MIMEText(body, 'plain'))
            server.sendmail(senderEmail, email, msg.as_string())
            return jsonify({'error': 'username already exists'}), 400

        query = "INSERT INTO USER (username, password, roles) VALUES (%s, %s, %s)"
        db.execute_query(query, (username, password, roles))
        body = "User registered successfully" 
        msg.attach(MIMEText(body, 'plain'))
        server.sendmail(senderEmail, email, msg.as_string())
        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#=========================================================================================


@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = db.execute_query("SELECT * FROM USER WHERE username = %s AND password = %s", (username, password))
        email = username
        if user:
            access_token = create_access_token(identity=username)
            response = make_response(jsonify({'message': 'Login successful'}))

            body = "Login successful"
            msg.attach(MIMEText(body, 'plain'))
            server.sendmail(senderEmail, email, msg.as_string())

            response.set_cookie('token', access_token)
            return response, 200
        else:
            body = "Invalid username or password"
            msg.attach(MIMEText(body, 'plain'))
            server.sendmail(senderEmail, email, msg.as_string())
            return jsonify({'error': 'Invalid username or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500




@user_bp.route('/masterData', methods=['GET'])
@jwt_required()
@roles_required('admin')
def master_data():
    try:
        user_data = db.execute_query("SELECT username, password, roles FROM USER;")
        user_list = []
        for username, password, role in user_data:
            user_dict = {
                'username': username,
                'password': password,
                'role': role
            }
            user_list.append(user_dict)

        return jsonify({'users': user_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@user_bp.route('/loggedinUser', methods=['GET'])
@jwt_required()
@roles_required('admin')
def loggedin_user():
    try:
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@user_bp.route('/', methods=["GET"])
def home():
    return "This is a home page:"
