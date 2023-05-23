from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.sql import text

app = Flask(__name__)
engine = create_engine("postgresql://postgres:2222@localhost:5432/library")

with engine.connect() as connection:
    result = connection.execute(text("""SELECT * FROM public.author"""))
    for row in result:
        print(row)
response = {"status": "success", "message": "SQL query executed successfully"}
print(response)


@app.route("/execute-sql", methods=["POST"])
def execute_sql():
    sql_query = request.json["sql_query"]
    with engine.connect() as connection:
        result = connection.execute("SELECT * FROM library.public.author")
        for row in result:
            print(row)
    response = {"status": "success", "message": "SQL query executed successfully"}
    return jsonify(response)


if __name__ == '__main__':
    app.run()
