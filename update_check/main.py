from typing import Tuple, List, Dict
from Libraries.info import USER, HOST, MYSQL_PASSWORD, PORT, DATABASE, SENDER, SENDER_PASSWORD, RECIPIENT
from Libraries.updateCheck import check_updates
from Libraries.exporter import to_dataframe, save_csv, send_mail
import mysql.connector
import pandas as pd


def add_query(info_list: List) -> str:
    # adds new query of the update_check operation's results to the MySQL database.

    # connect to the MySQL server
    try:
        db = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=MYSQL_PASSWORD,
            port=PORT,
            database=DATABASE
        )
    except Exception as error:
        return f'failed to connect to MySQL server to add update-check query. Error: {error}'
    cursor = db.cursor()
    package = info_list[0]
    time = info_list[1]
    try:
        for num in range(len(package)):
            cursor.execute(
                f"INSERT INTO directadmin_update_check (package, time) VALUES ({package[num]},{time[num]})")
        db.commit()
        db.close()
        return f'added MySQL query for {package} successfully!'
    except Exception as error:
        return f'failed to add MySQL query for {package} in ip_check table of nrst_project database. Error: {error}'


def check_and_export() -> Tuple[List, Dict[str, str]]:
    # performs the update_check and export operations. returns the ip_check operation's results
    # and logs of all the other functions it uses.
    logger = {}
    logger['packages'] = check_results = check_updates()
    # df, log = update_csv(check_results)
    # logger['update_csv'] = log
    df = to_dataframe(check_results)
    logger['save_csv'] = save_csv(df)
    logger['add_query'] = add_query(check_results)
    logger['send_mail'] = send_mail(df,
                                    sender=SENDER,
                                    recipient=RECIPIENT,
                                    password=SENDER_PASSWORD)

    # send the logger via email too.
    logs_df = pd.DataFrame(logger, index=[0])
    logs_df.to_csv(r'path to save update_check results')
    send_mail(logs_df,
              sender=SENDER,
              recipient=RECIPIENT,
              password=SENDER_PASSWORD)

    return check_results, logger


if __name__ == '__main__':
    print('this is the main.py file of the project.\n to run the program itself you should run the update_software.sh '
          'script')
    results, logs = check_and_export()
    print(f'the results of the update check operation are:\n{results}')
    print(f'\n\nthe logs of the update check operation are:\n{logs}')
