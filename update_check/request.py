import requests

BASE_URL = 'http://127.0.0.1:5000/'

get_query_search_values = \
    {
        'packages': [],   # list of packages to search for in the MySQL database
        'time': []  # list of ip_check times (string) to search for in the MySQL database.
    }

get_query = requests.get(BASE_URL, get_query_search_values)

print(get_query)
