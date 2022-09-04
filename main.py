from typing import Tuple, List, Dict
from info import mail_credentials, mysql_connection_info
from Scripts.spamCheck import check_ip
from Scripts.exporter import update_csv, save_csv, send_mail
from flask import Flask
from flask_restful import Api, Resource, reqparse
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
    # adds new query of the ip_check operation's results to the MySQL database.
    ip = info_list[0]
    time = info_list[3]
    timeout = info_list[2]
    blacklisted = info_list[1]
    try:
        cursor.execute(
            f"INSERT INTO ip_check (ip, time, blacklisted, timeout) VALUES ({ip},{time},{blacklisted},{timeout})")
        db.commit()
        return f'added MySQL query for {ip} successfully!'
    except Exception as error:
        return f'failed to add MySQL query for {ip} in ip_check table of nrst_project database. Error: {error}'


def search_for_query(keywords_dict: Dict) -> Dict:
    single_results = {}
    for entry in keywords_dict:
        if keywords_dict[entry] is None:
            keywords_dict.pop(entry)
        else:
            single_results[entry] = []
            for value in keywords_dict[entry]:
                cursor.execute(f"SELECT * FROM ip_check WHERE {entry} = '{value}' ORDER BY time DESC")
                for result in cursor:
                    single_results[entry].append(result)
    length = len(single_results)
    if length == 1:
        return {'results': single_results[list(single_results.keys())[0]]}
    else:
        final_results = []
        keys = list(single_results.keys())
        key_len = len(keys)
        for i in single_results[keys[0]]:
            check_flag = []
            for j in range(1,key_len):
                check_flag.append(i in single_results[keys[j]])
            if False not in check_flag:
                final_results.append(i)
        return {'results': final_results}



def check_and_export(ip) -> Tuple[List, Dict[str, str]]:
    # performs the ip_check and export operations. returns the ip_check operation's results
    # and logs of all the other functions it uses.
    logger = {}
    check_results = check_ip(ip)
    logger['ip'] = ip
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


app = Flask(__name__)
api = Api(app)

ip_check_put = reqparse.RequestParser()
ip_check_put.add_argument('ip', type=List, help='insert all the ips you want to be checked.', required=True)

database_query_get = reqparse.RequestParser()
database_query_get.add_argument('ip', type=List, help='insert list of ips you want to search for')
database_query_get.add_argument('blacklisted', type=List, help='insert list of listed providers you want to search for')
database_query_get.add_argument('timeout', type=List, help='insert list of timeout providers you want to search for')
database_query_get.add_argument('time', type=List, help='search for ip_check results by time')


class IpCheckReq(Resource):
    def get(self):
        search_keys = database_query_get.parse_args()
        database_search_results = search_for_query(search_keys)
        return database_search_results

    def put(self):
        req_ips = ip_check_put.parse_args()
        req_ips = req_ips['ip']
        results = []
        logs = []
        for ip in req_ips:
            cr, log = check_and_export(ip)
            results.append(cr)
            logs.append(log)
        return {'Results': results, 'Logs': logs}


api.add_resource(IpCheckReq, '/')

if __name__ == '__main__':
    app.run()
