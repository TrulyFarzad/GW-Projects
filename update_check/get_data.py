from flask import Flask
from flask_restful import Api, Resource, reqparse
from typing import List, Dict
from Scripts.info import USER, HOST, MYSQL_PASSWORD, PORT, DATABASE
import mysql.connector


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
        return {'results': f'failed to connect to MySQL server to search for requested update-check query. Error: {error}'}
    cursor = db.cursor()
    for entry in keywords_dict:
        if keywords_dict[entry] is None:
            keywords_dict.pop(entry)
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
    return {'results': results}


app = Flask(__name__)
api = Api(app)


database_query_get = reqparse.RequestParser()
database_query_get.add_argument('package', type=List, help='insert list of packages you want to search for')
database_query_get.add_argument('time', type=List, help='search for ip_check results by time')


class UpdateCheckReq(Resource):
    def get(self):
        search_keys = database_query_get.parse_args()
        database_search_results = search_for_query(search_keys)
        return database_search_results


api.add_resource(UpdateCheckReq, '/')

if __name__ == '__main__':
    app.run()
