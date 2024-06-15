"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
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

# create a route for /invoices that will retrieve and return the users invoices 
# in json format
# GET 
