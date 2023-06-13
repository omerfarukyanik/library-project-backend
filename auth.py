from flask import Blueprint, jsonify, make_response, request
from flask_wtf.csrf import generate_csrf
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from utils.sql import ADMIN_LOGIN_SQL, USER_LOGIN_SQL, ADMIN_SIGN_UP_SQL, ADMIN_USERNAME_SEARCH_SQL, \
    ADMIN_EMAIL_SEARCH_SQL, USER_USERNAME_SEARCH_SQL, USER_EMAIL_SEARCH_SQL, USER_SIGN_UP_SQL
from utils.util_funcs import log_to_db

auth = Blueprint('auth', __name__)

engine = create_engine("postgresql://postgres:2222@localhost:5432/library")


@auth.route("/api/get-session", methods=["GET"])
def get_session():
    custom_response = make_response()
    custom_response.headers.set("X-CSRFToken", generate_csrf())
    custom_response.headers.add('Access-Control-Expose-Headers', "X-CSRFToken")
    return custom_response, 200


@auth.route('/api/login', methods=["POST"])
def login():
    with engine.connect() as connection:
        connection.begin()
        if request.form.get("type") == "admin":
            result = connection.execute(
                text(ADMIN_LOGIN_SQL.format(request.form.get("username"))))
            if result.rowcount == 0:
                log_to_db(connection, request.form.get("username"), "cant.find.admin.account", "admin")
                return jsonify({"status": "not-found", "message": "cant.find.admin.account"}), 404

            log_to_db(connection, request.form.get("username"), "admin.found", "admin")
            return jsonify({"status": "success", "message": "admin.found", "password": result.first().password}), 200
        result = connection.execute(
            text(USER_LOGIN_SQL.format(request.form.get("username"))))
        if result.rowcount == 0:
            log_to_db(connection, request.form.get("username"), "cant.find.user.account", "user")
            return jsonify({"status": "not-found", "message": "cant.find.user.account"}), 404
        log_to_db(connection, request.form.get("username"), "user.found", "user")
        return jsonify({"status": "success", "message": "user.found", "password": result.first().password}), 200


@auth.route('/api/signup', methods=["POST"])
def signup():
    with engine.connect() as connection:
        connection.begin()
        result = connection.execute(text(USER_USERNAME_SEARCH_SQL.format(request.form.get("username"))))
        if result.rowcount != 0:
            log_to_db(connection, "system", "user.username.exists", "user")
            return jsonify({"status": "bad-request", "message": "user.username.exists"}), 400

        result = connection.execute(text(ADMIN_USERNAME_SEARCH_SQL.format(request.form.get("username"))))
        if result.rowcount != 0:
            log_to_db(connection, "system", "admin.username.exists", "admin")
            return jsonify({"status": "bad-request", "message": "admin.username.exists"}), 400

        result = connection.execute(text(ADMIN_EMAIL_SEARCH_SQL.format(request.form.get("email"))))
        if result.rowcount != 0:
            log_to_db(connection, "system", "admin.username.exists", "admin")
            return jsonify({"status": "bad-request", "message": "admin.email.exists"}), 400

        result = connection.execute(text(USER_EMAIL_SEARCH_SQL.format(request.form.get("email"))))
        if result.rowcount != 0:
            log_to_db(connection, "system", "user.email.exists", "user")
            return jsonify({"status": "bad-request", "message": "user.email.exists"}), 400

        if request.form.get("accountType") == "admin":
            result = connection.execute(
                text(ADMIN_SIGN_UP_SQL.format(request.form.get("username"), request.form.get("password"),
                                              request.form.get("email"), request.form.get("name"),
                                              request.form.get("surname"), "default")))
            if result.rowcount == 0:
                log_to_db(connection, "system", "cant.create.admin.account", "admin")
                return jsonify({"status": "bad-request", "message": "cant.create.admin.account"}), 400
            log_to_db(connection, "system", "admin.account.create.success", "admin")
            return jsonify({"status": "success", "message": "admin.account.create.success", "type": "admin"}), 200

        result = connection.execute(
            text(USER_SIGN_UP_SQL.format(request.form.get("username"), request.form.get("password"),
                                         request.form.get("email"), request.form.get("name"),
                                         request.form.get("surname"), "default")))
        if result.rowcount == 0:
            log_to_db(connection, "system", "cant.create.user.account", "user")
            return jsonify({"status": "bad-request", "message": "cant.create.user.account"}), 400
        log_to_db(connection, "system", "user.account.create.success", "user")
        return jsonify({"status": "success", "message": "user.account.create.success", "type": "user"}), 200


@auth.route('/logout')
def logout():
    return 'Logout'
