from bs4 import BeautifulSoup
import requests


# # url = 'https://5.182.44.209:4041/admin/plugins/custombuild?tab=update-software'
# url = 'http://libgen.rs/search.php?req=art+of+war&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def'
#
# html_text = requests.get(url).text
#
# soup = BeautifulSoup(html_text, 'lxml')
#
# updates = soup.find_all('tr', class_='table-row')
#
# packages = []
#
# for row in updates:
#     packages.append(row.td.text)

a = [['hello world']]

print('hell wor' in a[0][0])
