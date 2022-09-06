from flask import Flask
from flask_restful import Api, Resource, reqparse
from typing import List, Dict
from update_check.Scripts.info import mysql_connection_info
import mysql.connector


# connect to the MySQL server
db = mysql.connector.connect(
    host=mysql_connection_info.HOST,
    user=mysql_connection_info.USER,
    password=mysql_connection_info.PASSWORD,
    port=mysql_connection_info.PORT,
    database=mysql_connection_info.DATABASE
)
cursor = db.cursor()


def search_for_query(keywords_dict: Dict) -> Dict:
    single_results = {}
    for entry in keywords_dict:
        if keywords_dict[entry] is None:
            keywords_dict.pop(entry)
        else:
            single_results[entry] = []
            for value in keywords_dict[entry]:
                cursor.execute(f"SELECT * FROM directadmin_update_check WHERE {entry} = '{value}' ORDER BY time DESC")
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
            for j in range(1, key_len):
                check_flag.append(i in single_results[keys[j]])
            if False not in check_flag:
                final_results.append(i)
        return {'results': final_results}


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
