from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from auth import roles_required
from database import Database

db = Database()


calc_bp = Blueprint('calc', __name__)


@calc_bp.route('/add', methods=['POST'])
@jwt_required()
@roles_required('user')
def get_add():
    try:
        current_user_id = get_jwt_identity()
        response = request.get_json()
        num1 = response.get('a')
        num2 = response.get('b')

        if num1 is None or num2 is None:
            return jsonify({'error': 'invalid no format'}), 400

        try:
            result = float(num1) + float(num2)
            return jsonify({'result': result})
        except ValueError:
            return jsonify({'error': 'invalid number format'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ calc_bp.route('/subtract', methods=['POST'])
@jwt_required()
@roles_required('user')
def get_subtract():
    try:
        current_user_id = get_jwt_identity()
        response = request.get_json()
        num1 = response.get('a')
        num2 = response.get('b')

        if num1 is None or num2 is None:
            return jsonify({'error': 'invalid no format'}), 400

        try:
            result = float(num1) - float(num2)
            return jsonify({'result': result})
        except ValueError:
            return jsonify({'error': 'invalid number format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@calc_bp.route('/multiply', methods=['POST'])
@jwt_required()
@roles_required('user')
def multiply():
    try:
        current_user_id = get_jwt_identity()
        response = request.get_json()
        
        num1 = response.get('a')
        num2 = response.get('b')

        if num1 is None or num2 is None:
            return jsonify({'error': 'invalid no format'}), 400

        try:
            result = float(num1) * float(num2)
            return jsonify({'result': result})
        except ValueError:
            return jsonify({'error': 'invalid number format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    




@calc_bp.route('/division', methods=['POST'])
@jwt_required()
@roles_required('user')
def division():
    try:
        current_user_id = get_jwt_identity()
        response = request.get_json()
       
        num1 = response.get('a')
        num2 = response.get('b')

        if num1 is None or num2 is None:
            return jsonify({'error': 'invalid no format'}), 400

        try:
            result = float(num1) / float(num2)
            return jsonify({'result': result})
        except ValueError:
            return jsonify({'error': 'invalid number format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

