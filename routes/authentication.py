from flask import Blueprint, request, jsonify
from flask_jwt_extended import  jwt_required, get_jwt_identity, create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from models.user import User

auth = Blueprint('auth', __name__)

# Log in user with Tokens in Cookies 
@auth.route('/login', methods=['POST'])
def login_user():
    """Login user and return JWT tokens."""
    data = request.get_json()

    if not data or 'email' not in data or not data['email'] or 'password' not in data or not data['password']:
        return jsonify({'message': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Create access and refresh tokens
    access_token = create_access_token(identity=str(user.id))  
    refresh_token = create_refresh_token(identity=str(user.id))  

    response = jsonify({'message': 'Login successful', 'user': user.serialize()})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response

# Refresh Token EndPoint
@auth.route('/token/refresh', method=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity() 
    access_token = create_access_token(identity=identity)
    response = jsonify({'message' : 'Token refreshed'})
    set_access_cookies(response=access_token)
    return response


#  Logout (Clearing Cookies)
@auth.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'message': 'Logged out'})
    unset_jwt_cookies(response)
    return response
