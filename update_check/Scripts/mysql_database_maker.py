"""
this script makes the desired database in the MySQL app of the server it's running inside.
to be run only one, upon running the program on a server for the first time.
"""

from info import USER, HOST, MYSQL_PASSWORD, PORT
import mysql.connector


if __name__ == '__main__':
    db = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=MYSQL_PASSWORD,
        port=PORT
    )

    cursor = db.cursor()

    cursor.execute('CREATE DATABASE nrst_project')
    print('database created')
