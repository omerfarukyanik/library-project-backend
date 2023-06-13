from utils.const import ALLOWED_EXTENSIONS
from sqlalchemy.sql import text
from utils.sql import LOGS_SQL
import datetime


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def log_to_db(connection, done_by, message, account_type):
    connection.execute(
        text(LOGS_SQL.format(datetime.datetime.now(), done_by, message, account_type)))
    connection.commit()
    connection.close()
