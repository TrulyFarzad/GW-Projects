"""
the purpose of this script is to be run on the preset schedule (like as a cronjob) and check for updates in the
Custom Build --> Update Software of the Directadmin server.
then check if the new update for each file contains any bug fixes or security fixes etc. based on preset keywords.
and return the final results in a List format along with current time.
"""

try:
    from scrape_rules import check_package
except ModuleNotFoundError:
    from Scripts.scrape_rules import check_package
from datetime import datetime
from typing import List


def directadmin_check() -> List:
    # get a list of new package updates from '/usr/local/directadmin/custombuild/build versions'
    results = []
    add = []

    while True:
        try:
            package = input()
            if package.split(' ')[0].lower() == 'latest':
                pckg = package.split(' ')
                add.append(pckg[3][0:-1].strip())
                add.append(pckg[-1].strip())
            elif package.split(' ')[0].lower() == 'installed':
                pckg = package.split(' ')
                add.append(pckg[-1].strip())
                print(f'add is: {add[1]}')
                results.append(add)
                add = []
            else:
                continue
        except:
            break
    return results


def check_updates() -> List:
    # check for updates with directadmin and return the check results of which ones contain crucial updates.
    new_updates = directadmin_check()
    results = []
    for package in new_updates:
        try:
            package.append(str(datetime.now()))
            package.append(check_package(package))
        except Exception as error:
            results.append([f'failed to check_updates for {package}: {error}', 0, 0, str(datetime.now()), 'error'])
        finally:
            return results


if __name__ == '__main__':
    print('this is the updateCheck.py file.\nto run the program run the main.py file and make an API request to it.')
    check = check_updates()
    for i in check[0]:
        print(i)
