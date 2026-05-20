import pymysql

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="username@2811",
        database="house_db",
        cursorclass=pymysql.cursors.DictCursor   
    )
