"""
this script creates desired tables in the database. to be run after the mysql_database_maker.py script.
and only once, upon running the program on a server for the first time.
"""

from info import mysql_connection_info
import mysql.connector


if __name__ == '__main__':
    db = mysql.connector.connect(
        host=mysql_connection_info.HOST,
        user=mysql_connection_info.USER,
        password=mysql_connection_info.PASSWORD,
        port=mysql_connection_info.PORT,
        database=mysql_connection_info.DATABASE
    )

    cursor = db.cursor()

    cursor.execute(
        "CREATE TABLE ip_check (ip VARCHAR(20) NOT NULL, time VARCHAR(30) NOT NULL, blacklisted VARCHAR(1600), timeout VARCHAR(1600), index int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
    print('successfully created ip_Check table.')

    cursor.execute(
        "CREATE TABLE directadmin_update_check (package VARCHAR(20) NOT NULL, time VARCHAR(30) NOT NULL, index int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
    print('successfully created Directadmin table.')
