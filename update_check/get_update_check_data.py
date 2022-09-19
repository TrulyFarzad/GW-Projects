from flask import Flask
from flask_restful import Api, Resource, reqparse
from typing import Dict
from Libraries.info import USER, HOST, MYSQL_PASSWORD, PORT, DATABASE
import mysql.connector


def concat_text(list_input: list) -> str:
    # concat all the provider names resulted from check_ip operation into a ';' separated string.
    if len(list_input) == 0:
        return ''
    result = ''
    for text in list_input:
        result += f'{text};'
    result = result[0:-1]
    return result


def search_for_query(keywords_dict: Dict) -> Dict:
    # search in the MySQL database for the given values from the get request.
    results_dict = {'package': [], 'new': [], 'old': [], 'time': [], 'update': []}
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
        return {'results': f'failed to connect to MySQL server to search for requested update-check query. Error: {error}'}
    cursor = db.cursor()
    get_req_len = len(keywords_dict)
    if get_req_len == 1:
        cursor.execute(f"SELECT * FROM directadmin_update_check WHERE {list(keywords_dict.keys())[0]} IN {keywords_dict[list(keywords_dict.keys())[0]]} ORDER BY time DESC")
    elif get_req_len == 2:
        cursor.execute(f"SELECT * FROM directadmin_update_check WHERE {list(keywords_dict.keys())[0]} IN {keywords_dict[list(keywords_dict.keys())[0]]} AND {list(keywords_dict.keys())[1]} IN {keywords_dict[list(keywords_dict.keys())[1]]} ORDER BY time DESC")
    else:
        db.close()
        return {'results': ['no search keys given']}
    results = list(cursor)
    db.close()
    for r in results:
        results_dict['package'].append(r[0])
        results_dict['new'].append(r[1])
        results_dict['old'].append(r[2])
        results_dict['time'].append(r[3])
        results_dict['update'].append(r[3])
    for column in results_dict:
        results_dict[column] = concat_text(column)
    return results_dict


app = Flask(__name__)
api = Api(app)


database_query_get = reqparse.RequestParser()
database_query_get.add_argument('package', type=str, help='package name')
database_query_get.add_argument('new', type=str, help='new version')
database_query_get.add_argument('old', type=str, help='old version')
database_query_get.add_argument('time', type=str, help='time')
database_query_get.add_argument('update', type=str, help='critical update (y/n)')


class UpdateCheckReq(Resource):
    # def get(self):
    #     search_keys = database_query_get.parse_args()
    #     database_search_results = search_for_query(search_keys)
    #     return database_search_results
    def get(self):
        search_keys = database_query_get.parse_args()
        search_keys_cleaned = dict(search_keys)
        for entry in search_keys:
            if search_keys[entry] is None:
                search_keys_cleaned.pop(entry)
                continue
            search_keys_cleaned[entry] = search_keys_cleaned[entry].split(';')
        database_search_results = search_for_query(search_keys_cleaned)
        return database_search_results


api.add_resource(UpdateCheckReq, '/')

if __name__ == '__main__':
    app.run()
