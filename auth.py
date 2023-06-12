from flask import Blueprint, jsonify, make_response, request
from flask_cors import cross_origin
from flask_wtf.csrf import generate_csrf

auth = Blueprint('auth', __name__)


@auth.route("/api/get-session", methods=["GET"])
def get_session():
    response = make_response()
    response.headers.set("X-CSRFToken", generate_csrf())
    response.headers.add('Access-Control-Expose-Headers', "X-CSRFToken")
    return response, 200


@auth.route('/api/login', methods=["POST"])
def login():
    form = request
    response = {"status": "success", "message": "Login", "type": "admin"}
    return jsonify(response), 200


@auth.route('/signup')
def signup():
    return 'Signup'


@auth.route('/logout')
def logout():
    return 'Logout'
