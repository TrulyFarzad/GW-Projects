from typing import Tuple, List, Dict
from Scripts.info import mail_credentials, mysql_connection_info
from Scripts.updateCheck import check_update, concat_text, crucial_updates
from Scripts.exporter import update_csv, save_csv, send_mail
import mysql.connector
import pandas as pd

# connect to the MySQL server
db = mysql.connector.connect(
    host=mysql_connection_info.HOST,
    user=mysql_connection_info.USER,
    password=mysql_connection_info.PASSWORD,
    port=mysql_connection_info.PORT,
    database=mysql_connection_info.DATABASE
)
cursor = db.cursor()


def add_query(info_list: List) -> str:
    # adds new query of the update_check operation's results to the MySQL database.
    package = info_list[0]
    time = info_list[1]
    try:
        for num in range(len(package)):
            cursor.execute(
                f"INSERT INTO directadmin_update_check (package, time) VALUES ({package[num]},{time[num]})")
        db.commit()
        return f'added MySQL query for {package} successfully!'
    except Exception as error:
        return f'failed to add MySQL query for {package} in ip_check table of nrst_project database. Error: {error}'


def check_and_export() -> Tuple[List, Dict[str, str]]:
    # performs the update_check and export operations. returns the ip_check operation's results
    # and logs of all the other functions it uses.
    logger = {}
    check_results = check_update()
    check_results[0] = crucial_updates(check_results[0])
    logger['packages'] = concat_text(check_results[0])
    df, log = update_csv(check_results)
    logger['update_csv'] = log
    logger['save_csv'] = save_csv(df)
    logger['add_query'] = add_query(check_results)
    logger['send_mail'] = send_mail(df,
                                    sender=mail_credentials.SENDER,
                                    recipient=mail_credentials.RECIPIENT,
                                    password=mail_credentials.PASSWORD)

    # send the logger via email too.
    logs_df = pd.DataFrame(logger, index=[0])
    send_mail(logs_df,
              sender=mail_credentials.SENDER,
              recipient=mail_credentials.RECIPIENT,
              password=mail_credentials.PASSWORD)

    return check_results, logger


if __name__ == '__main__':
    results, logs = check_and_export()
    print(f'the results of the update check operation are:\n{results}')
    print(f'\n\nthe logs of the update check operation are:\n{logs}')
