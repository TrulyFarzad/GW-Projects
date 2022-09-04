import requests

BASE_URL = 'http://127.0.0.1:5000/'
# TODO: add a request to get the ip checklist from the local server.
# ip_checklist = requests.get('http://185.50.37.24:4567/')
ip_checklist = []

check_response = requests.put(BASE_URL, {'ip': ip_checklist})


get_query_search_values = \
    {
        'ip': [],   # list of ips to search for in the MySQL database
        'blacklisted': [],   # list of blacklisted providers to search for in the MySQL database
        'timeout': [],  # list of failed providers to search for in the MySQL database
        'time': []  # list of ip_check times (string) to search for in the MySQL database.
    }

get_query = requests.get(BASE_URL, get_query_search_values)

print(check_response.json())
