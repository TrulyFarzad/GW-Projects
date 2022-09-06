"""
the purpose of this script is to be run on the preset schedule (like as a cronjob) and check for updates in the
Custom Build --> Update Software of the Directadmin server.
then check if the new update for each file contains any bug fixes or security fixes etc. based on preset keywords.
and return the final results in a List format along with current time.
"""

from scrap_rules import *
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
import requests


def concat_text(list_input: List) -> str:
    # concat all the provider names resulted from check_ip operation into a ';' separated string.
    if len(list_input) == 0:
        return ''
    result = ''
    for text in list_input:
        result += f'{text};'
    result = result[0:-1]
    return result


def check_update(url: str = 'https://5.182.44.209:4041/admin/plugins/custombuild?tab=update-software') -> List:
    # use the Directadmin page of Custom Build --> Update Software to get a list of new updates for packages.
    time = str(datetime.now())
    try:
        html_text = requests.get(url).text  # scrap data from url
        soup = BeautifulSoup(html_text, 'lxml')  # parse scrapped data
        updates = soup.find_all('tr', class_='table-row')  # each row of the updates table
        packages = []
        for row in updates:
            packages.append(row.td.text)  # extract each package's name from its update table's row
        return [packages, [time for _ in range(len(packages))]]
    except Exception as error:
        return [[f'Error in check_update operation: {error}'], [time]]


def crucial_updates(new_updates: List) -> List:
    # get the result of the check_update operation and return a list of only those which contain crucial updates.
    if 'Error in check_update operation:' in new_updates[0][0]:
        return new_updates
    check_results = {}
    return_value = []
    for package in new_updates:
        if package == 'clamav':
            check_results[package] = clamav()
        elif package == 'php':
            check_results[package]: php()
        elif package == 'apache':
            check_results[package]: apache()
    for result in check_results:
        if check_results[result] == 'y':
            return_value.append(result)
    return return_value


if __name__ == '__main__':
    print('this is the updateCheck.py file.\nto run the program run the main.py file and make an API request to it.')
    check = check_update()
    for i in check[0]:
        print(i)
