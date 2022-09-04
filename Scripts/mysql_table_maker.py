"""
this script creates desired tables in the database. to be run after the mysql_database_maker.py script.
and only once, upon running the program on a server for the first time.
"""

import mysql.connector


if __name__ == '__main__':
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='d5ug9XF45KMwHe71Gk',
        port='3031',
        database='nrst_project'
    )

    cursor = db.cursor()

    cursor.execute(
        "CREATE TABLE ip_check (ip VARCHAR(20) NOT NULL, time VARCHAR(30) NOT NULL, blacklisted VARCHAR(1600), timeout VARCHAR(1600), index int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
    print('successfully created ip_Check table.')

    cursor.execute(
        "CREATE TABLE directadmin_update_check (name VARCHAR(50) NOT NULL, current_Version VARCHAR(20) NOT NULL, new_Version VARCHAR(20), update ENUM('Y', 'N'), index int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
    print('successfully created Directadmin table.')
