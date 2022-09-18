from typing import Tuple, List, Dict
from Scripts.info import HOST, USER, MYSQL_PASSWORD, PORT, DATABASE, SENDER, SENDER_PASSWORD, RECIPIENT
from Scripts.spamCheck import check_ip
from Scripts.exporter import to_dataframe, save_csv, send_mail
from flask import Flask
from flask_restful import Api, Resource, reqparse
import mysql.connector
import pandas as pd


def add_query(info_list: List) -> str:
    # adds new query of the ip_check operation's results to the MySQL database.

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
        return f'failed to connect to MySQL server to add ip-check query. Error: {error}'
    cursor = db.cursor()
    ip = info_list[0]
    time = info_list[3]
    timeout = info_list[2]
    blacklisted = info_list[1]
    try:
        cursor.execute(
            f"INSERT INTO ip_check (ip, time, blacklisted, timeout) VALUES ({ip},{time},{blacklisted},{timeout})")
        db.commit()
        db.close()
        return f'added MySQL query for {ip} successfully!'
    except Exception as error:
        return f'failed to add MySQL query for {ip} in ip_check table of nrst_project database. Error: {error}'


def search_for_query(keywords_dict: Dict) -> Dict:
    # search in the MySQL database for the given values from the get request.

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
        return {'results': f'failed to connect to MySQL server to search for requested ip-check query. Error: {error}'}
    cursor = db.cursor()
    for entry in keywords_dict:
        if keywords_dict[entry] is None:
            keywords_dict.pop(entry)
    get_req_len = len(keywords_dict)
    if get_req_len == 1:
        cursor.execute(f"SELECT * FROM directadmin_update_check WHERE {list(keywords_dict.keys())[0]} IN {keywords_dict[list(keywords_dict.keys())[0]]} ORDER BY time DESC")
    elif get_req_len == 2:
        cursor.execute(f"SELECT * FROM directadmin_update_check WHERE {list(keywords_dict.keys())[0]} IN {keywords_dict[list(keywords_dict.keys())[0]]} AND {list(keywords_dict.keys())[1]} IN {keywords_dict[list(keywords_dict.keys())[1]]} ORDER BY time DESC")
    elif get_req_len == 3:
        cursor.execute(f"SELECT * FROM directadmin_update_check WHERE {list(keywords_dict.keys())[0]} IN {keywords_dict[list(keywords_dict.keys())[0]]} AND {list(keywords_dict.keys())[1]} IN {keywords_dict[list(keywords_dict.keys())[1]]} AND {list(keywords_dict.keys())[2]} IN {keywords_dict[list(keywords_dict.keys())[2]]} ORDER BY time DESC")
    elif get_req_len == 4:
        cursor.execute(f"SELECT * FROM directadmin_update_check WHERE {list(keywords_dict.keys())[0]} IN {keywords_dict[list(keywords_dict.keys())[0]]} AND {list(keywords_dict.keys())[1]} IN {keywords_dict[list(keywords_dict.keys())[1]]} AND {list(keywords_dict.keys())[2]} IN {keywords_dict[list(keywords_dict.keys())[2]]} AND {list(keywords_dict.keys())[3]} IN {keywords_dict[list(keywords_dict.keys())[3]]} ORDER BY time DESC")
    else:
        db.close()
        return {'results': ['no search keys given']}
    results = list(cursor)
    db.close()
    return {'results': results}


def check_and_export(ip) -> Tuple[List, Dict[str, str]]:
    # performs the ip_check and export operations. returns the ip_check operation's results
    # and logs of all the other functions it uses.
    logger = {}
    check_results = check_ip(ip)
    logger['ip'] = ip
    # df, log = update_csv(check_results)
    # logger['update_csv'] = log
    df = to_dataframe(check_results)
    logger['save_csv'] = save_csv(df)
    logger['add_query'] = add_query(check_results)
    logger['send_mail'] = send_mail(df,
                                    sender=SENDER,
                                    recipient=RECIPIENT,
                                    password=SENDER_PASSWORD,
                                    subject='new ip check query')

    # send the logger via email too.
    logs_df = pd.DataFrame(logger, index=[0])
    logs_df.to_csv(r'path to save ip_check results')
    send_mail(logs_df,
              sender=SENDER,
              recipient=RECIPIENT,
              password=SENDER_PASSWORD,
              subject='operation logs')

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
    # ip_list = \
    #     [
    #         '157.90.205.145',
    #         '151.80.93.33',
    #         '138.201.79.233',
    #         '148.251.200.145',
    #         '147.135.173.17',
    #         '5.9.220.53'
    #     ]
    #
    # rslts = []
    # check_logs = []
    # for ip_to_check in ip_list:
    #     cr, lgs = check_and_export(ip_to_check)
    #     rslts.append(cr)
    #     check_logs.append(lgs)
    # print(rslts)
    # print(check_logs)

    app.run()
