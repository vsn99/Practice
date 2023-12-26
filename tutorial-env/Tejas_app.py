from flask import Flask, request, jsonify
import mysql.connector
from jwt.exceptions import DecodeError
from functools import wraps
import os,requests,jwt,json,logging
from flask import make_response
logging.basicConfig(filename='app.log', level=logging.INFO)


app = Flask(__name__)

#=====================   Establish a connection to the database =================
def create_connection():
    connection = mysql.connector.connect(
        host="database.clau0466sb6g.us-east-1.rds.amazonaws.com",
        user="admin",
        password="12345678",
        database="database1"
        
    )
    print("connection is created successfully")
    return connection

connection = create_connection()
print(connection)

#========================================================================================
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE users (id INT PRIMARY KEY,username VARCHAR(50),password VARCHAR(50),role VARCHAR(50))")
    print("Table created successfully")

def insert_multiple_users(connection, user_records):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO users (id, username, password, role) VALUES (%s, %s, %s, %s)"
        cursor.executemany(query, user_records)
        connection.commit()
        cursor.close()
        print("Records inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Example data
user_records = [
    (1, 'tajesavhad999@gmail.com', '12345678', 'admin'),
    (2, 'user2', '123245678', 'user'),
    (3, 'user3', '12345678', 'user')
]

def select_records(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


#==========================  End point to add the user  =============================================================
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        # Get data from the request
        data = request.json
        id = data['id']
        username = data['username']
        password = data['password']
        role = data['role']

        # Create a database connection
        connection = create_connection()
        if connection is None:
            return jsonify({'message': 'Failed to connect to the database'}), 500

        # Insert data into the 'users' table
        cursor = connection.cursor()
        query = "INSERT INTO users (id,username,password,role) VALUES(%s ,%s, %s, %s)"
        cursor.execute(query, (id,username, password, role))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'User added successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#===========================================================================
@app.route('/get_users', methods=['GET'])
def get_users():
    try:
        # Create a database connection
        connection = create_connection()
        if connection is None:
            return jsonify({'message': 'Failed to connect to the database'}), 500

        # Retrieve all data from the 'users' table
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users"
        cursor.execute(query)
        users = cursor.fetchall()

        cursor.close()
        connection.close()

        # Return user data in the response
        return jsonify({'users': users}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

#==============================================================
select_records(connection)
#print(create_table(connection))  
#print(insert_multiple_users(connection ,user_records ))


#=========================== Authentication ===============================================
#==========================  Authentication ===============================================

    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/auth', methods=['POST'])
def authenticate_user():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415
    
    # Get credentials from the request
    username = request.json.get('username')
    password = request.json.get('password')

    # Create a database connection
    connection = create_connection()
    if connection is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    try:
        # Retrieve user data from the 'users' table
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            # Generate a token if the user is found
            token = jwt.encode({'user_id': user['id']}, app.config['SECRET_KEY'], algorithm="HS256")
            logging.info(f"Authentication successful! Token: {token}")

            # Set the token as a cookie in the response
            response = make_response(jsonify({'message': 'Authentication successful', 'Token': token}))
            response.set_cookie('token', token)
            return response, 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)