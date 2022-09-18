import requests

BASE_URL = 'http://127.0.0.1:5000/'
# TODO: add a request to get the ip checklist from the local server.
# ip_checklist = requests.get('http://185.50.37.24:4567/')
ip_checklist = \
    [
        '157.90.205.145'
        '151.80.93.33',
        '138.201.79.233',
        '148.251.200.145',
        '147.135.173.17',
        '5.9.220.53'
    ]

check_response = requests.put(BASE_URL, {'ip': ip_checklist})


# get_query_search_values = \
#     {
#         'ip': [],   # list of ips to search for in the MySQL database
#         'blacklisted': [],   # list of blacklisted providers to search for in the MySQL database
#         'timeout': [],  # list of failed providers to search for in the MySQL database
#         'time': []  # list of ip_check times (string) to search for in the MySQL database.
#     }
#
# get_query = requests.get(BASE_URL, get_query_search_values)
#
# print(check_response.json())
