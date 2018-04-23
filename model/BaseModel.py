from app import mysql

def getDbCursor():
    return mysql.get_db().cursor()