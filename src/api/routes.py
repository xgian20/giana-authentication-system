"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Invoice
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# token /POST
# this route is for when the user ALREADY exists and needs an ACCESS token 
# create user query with a conditional to see if user exists or return None

# this route is for a user that already exists and needs an access token 
# create a user query with a conditional where it checks to see if user exists or return none

@api.route('/token', methods=['POST'])
def generate_token():
    # receiving request and converting body of 
    # request into json format
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    # query the user table to check if user exists
    user = User.query.filter_by(email=email, password=password).first()

    if user is None:
        response = {
            "msg": "Email or password does not match."
        }
        return jsonify(response), 401
    
    access_token = create_access_token(identity=user.id)
    response = {
        "access_token": access_token,
        "user_id": user.id,
        "msg": f'Welcome {user.email}! This worked!'
    }
    
    return jsonify(response), 200

# create a route for signup that will add the user's email and password to the database
# POST 
# test that on postman

@api.route('/signup', methods=['POST'])
def register_user():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # query to check if email already exists
    email = email.lower()
    user = User.query.filter_by(email=email).first()

    if user is not None and user.email == email:
        response = {
            'msg': 'User already exists.'
        }
        return jsonify(response), 403
    
    # if email does not exist, make a record in the database
    # sign the user up

    user = User()
    user.email = email
    user.password = password
    user.is_active = True
    db.session.add(user)
    db.session.commit()

    response = {
        'msg': f'Congratulations {user.email}. You have signed up!'
    }
    return jsonify(response), 200

# create a route for /invoices that will retrieve and return the users invoices 
# in json format
# GET 

@api.route('/invoices' , methods=['GET'])
@jwt_required()
def get_invoices():
    # retrieve the user_id of the current user from the access_token
    # you do that with jwt_identity
    user_id = get_jwt_identity()
    # return jsonify(logged_in_as=user_id), 200

    user = User.query.filter_by(id=user_id).first()

    # query and retrieve any invoices that are in the database
    user_invoices = Invoice.query.filter_by(user_id=user_id).all()

    # use a list comprehension (for loop) that will : 1. get each invoice object and serialize() it 2. put them into a processed_invoices array
    processed_invoices = [each_invoices.serialize() for each_invoices in user_invoices]

    response = {
        'msg': f'Hello {user.email}, here are you invoices.',
        'invoices': processed_invoices
    }

    return jsonify(response), 200 