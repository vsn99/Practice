from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from database import Database
import json

db = Database()


with open("config.json") as config_file:
    jwt_config = json.load(config_file)["jwt"]

def roles_required(*required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            user_roles = get_user_roles(current_user)

            if 'admin' in user_roles:
                return f(*args, **kwargs)
            elif any(role in user_roles for role in required_roles):
                return f(*args, **kwargs)
            else:
                return jsonify({'error': 'Unauthorized: User does not have the necessary role'}), 403

        return decorated_function

    return decorator

def get_user_roles(username):
    try:
        query = "SELECT roles FROM USER WHERE username = %s"
        result = db.execute_query(query, (username,))
        return result[0][0].split(',') if result else []
    except Exception as e:
        print(f"Error fetching user roles: {e}")
        return []