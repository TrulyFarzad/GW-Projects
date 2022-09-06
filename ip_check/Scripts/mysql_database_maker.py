"""
this script makes the desired database in the MySQL app of the server it's running inside.
to be run only one, upon running the program on a server for the first time.
"""

from info import mysql_connection_info
import mysql.connector


if __name__ == '__main__':
    db = mysql.connector.connect(
        host=mysql_connection_info.HOST,
        user=mysql_connection_info.USER,
        password=mysql_connection_info.PASSWORD,
        port=mysql_connection_info.PORT
    )

    cursor = db.cursor()

    cursor.execute('CREATE DATABASE nrst_project')
    print('database created')
