from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from auth import roles_required
from database import Database
import requests,json,logging

db = Database()


currency_bp = Blueprint('currency', __name__)

# ... Other configurations


def euro_to_inr(euros):
    rate = 84
    try:
        euros = float(euros)
    except ValueError:
        raise ValueError(": Euros quantity should be a number")

    if euros < 0:
        raise ValueError("Invalid input: Euro should be non negative")

    inr = euros * rate
    return inr



@currency_bp.route('/euro_to_inr', methods=["POST"])
@jwt_required()
@roles_required('admin')
def handle_euros():

    headers = {'Authorization': f'Bearer {request.cookies.get("token")}'}
    response = requests.post('http://127.0.0.1:5000/euro_to_inr', headers=headers)

    data = request.get_json()
    euros = data.get("euros")
    try:
        if euros is None:
            raise ValueError("Invalid input: Euros value is missing")

        result = euro_to_inr(euros)
        return jsonify({'result': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


def pounds_to_inr(pounds):
    rate = 104
    try:
        pounds = float(pounds)
    except ValueError:
        raise ValueError("Value of quantity of Pounds should be in number:")

    if pounds < 0:
        raise ValueError("Value of the quantity of the pounds cannot be less than 0")

    inr = pounds * rate
    return inr


@currency_bp.route("/Pounds_to_inr", methods=["POST"])
@jwt_required()
@roles_required('admin')
def handle_Pounds():
    data = request.get_json()
    pounds = data.get("pounds")

    try:
        if pounds is None:
            raise ValueError("Invalid input: Pounds value is missing")

        result = pounds_to_inr(pounds)
        return jsonify({'result': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


def francs_to_inr(francs):
    rate = 96.6
    try:
        francs = float(francs)
    except ValueError:
        raise ValueError("Invalid value. Please enter amount in numbers")

    if francs < 0:
        raise ValueError("Francs cannot be in negative:")

    inr = francs * rate
    return inr



@currency_bp.route('/francs_to_inr', methods=["POST"])
@jwt_required()
@roles_required('admin')
def handle_francs():
    data = request.get_json()
    francs = data.get("francs")

    try:
        if francs is None:
            raise ValueError("Invalid input: Francs value is missing")

        result = francs_to_inr(francs)
        return jsonify({'result': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400