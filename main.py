import logging
import os

from flask import Flask, request, jsonify, flash, redirect, url_for, send_file, make_response, Response
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
# from sqlalchemy.sql import text
from utils.const import UPLOAD_FOLDER, MAX_CONTENT_LENGTH, SECRET_KEY, PORT_NUMBER
from utils.util_funcs import allowed_file
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect, generate_csrf

app = Flask(__name__)
CORS(app)
engine = create_engine("postgresql://postgres:2222@localhost:5432/library")
csrf = CSRFProtect(app)
logging.getLogger("flask_cors").level = logging.DEBUG


# with engine.connect() as connection:
#    result = connection.execute(text("""SELECT * FROM public.author"""))
#    for row in result:
#        print(row)
# response = {"status": "success", "message": "SQL query executed successfully"}
# print(response)

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":  # CORS preflight
        response = make_response()
        response.headers.add('Access-Control-Allow-Headers', request.headers.get("Access-Control-Request-Headers"))
        response.headers.add('Access-Control-Allow-Methods', request.headers.get("Access-Control-Request-Method"))
        response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin"))
        return response


@app.after_request
def handle_response(response):
    response.headers.add('Access-Control-Allow-Credentials', "true")
    return response


@app.route("/execute-sql", methods=["POST", "OPTIONS"])
def execute_sql():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = 'POST'
        return res
    sql_query = request.json["sql_query"]
    with engine.connect() as connection:
        result = connection.execute("SELECT * FROM library.public.author")
        for row in result:
            print(row)
    response = {"status": "success", "message": "SQL query executed successfully"}
    return jsonify(response)


@app.route("/api/upload-profile-picture", methods=["POST", "GET"])
@cross_origin(origins='*')
def upload_profile_picture():
    if request.method == "GET":
        if os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(request.args["filename"]))):
            return make_response(jsonify())
    if "profile_picture" not in request.files:
        flash("No file part!")
        return redirect(request.url)
    file = request.files["profile_picture"]
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename), file.content_length)
        return redirect(url_for("upload_profile_picture", filename=filename))


if __name__ == '__main__':
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["CORS_ORIGINS"] = "http://localhost:3000"
    app.config["CORS_HEADERS"] = "Content-Type"
    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    # from main import main as main_blueprint
    # app.register_blueprint(main_blueprint)

    app.run(debug=True, use_debugger=False, use_reloader=False, port=PORT_NUMBER)
