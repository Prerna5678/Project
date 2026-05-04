import pymysql
import os

def get_db_connection():
    connection = pymysql.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),   # Use env variable — never hardcode passwords
        database=os.environ.get("DB_NAME", "House_db"),
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
