from typing import List
from bs4 import BeautifulSoup
import requests

# list all the words the program will look for when checking if an update is crucial or not.
word_check_list = \
    [
        'crucial',
        'critical',
        'bug',
        'bugs',
        'fix',
        'fixes',
        'fixed'
        'bug-fix',
        'bug-fixes',
        'bugfix',
        'bugfixes'
        'security',
        'secure'
        'issue',
        'issues',
        'important',
        'vital'
    ]

# the link of the release-notes webpage of each package. False means the link is unknown.
# if you want to add new packages to be checked, insert their name (as shown in directadmin) and release-note url here.
# NOTE: if the release-note's page layout is unusual, you must write rules for it in the check package function
#   according to the page's html format.
package_release_note_links = \
    {
        'cwaf_rules_nginx_3': False,
        'cwaf_rules_ls': False,
        'cwaf_rules': False,
        'cwaf_rules_nginx': False,
        'imap': False,
        'letsencrypt': False,
        'apache': 'https://github.com/apache/commons-text/blob/master/RELEASE-NOTES.txt',
        'xapien': False,
        'imapsync': False,
        'msmtp': False,
        'bubblewrap': False,
        'jailshell': False,
        'apr': False,
        'modsecurity': False,
        'owasp': False,
        'libmaxminddb': False,
        'geoipupdate': False,
        'nginx': False,
        'unit': False,
        'openlitespeed': False,
        'composer': False,
        'wp-cli': False,
        'lego': False,
        'dnsproviders': False,
        'lua': False,
        's-nail': False,
        'awstats': False,
        'curl': 'https://github.com/curl/curl/blob/master/RELEASE-NOTES',
        'dovecot': False,
        'pigeonhole': False,
        'libspf2': False,
        'exim': False,
        'clamav': 'https://blog.clamav.net/',
        'blockcracking': False,
        'easy_spam_figther': False,
        'imagick': False,
        'phalcon': False,
        'snuffleupagus': False,
        'igbinary': False,
        'phpredis': False,
        'xmlrpc': False,
        'psr': False,
        'imagemagick': False,
        'redis': False,
        'libzip': False,
        'mysql': False,
        'mariadb': False,
        'jemalloc': False,
        'galera': False,
        'php7': 'https://www.php.net/ChangeLog-7.php',
        'php8': 'https://www.php.net/ChangeLog-8.php',
        'proftpd': False,
        'ncftp': False,
        'pureftpd': False,
        'roundcubemail': False,
        'rc_direct_login': False,
        'pma_direct_login': False,
        'spamassassin': False,
        'sa': False,
        'rspamd': False,
        'squirrelmail': False,
        'fcgid': False,
        'htscanner': False,
        'ruid2': False,
        'suphp': False,
        'webalizer': False,
        'zendopcache': False,
        'ioncube': False,
        'suhosin': False
    }


def concat_text(list_input: List) -> str:
    # concat all the provider names resulted from check_ip operation into a ';' separated string.
    if len(list_input) == 0:
        return ''
    result = ''
    for text in list_input:
        result += f'{text} \n'
    result = result[0:-1]
    return result


def check_keyword(release_notes: str) -> str:
    result = 'n'
    for keyword in word_check_list:
        if keyword in release_notes.lower():
            result = 'y'
    return result


# def curl():
# URL = 'https://github.com/curl/curl/blob/master/RELEASE-NOTES'
# release_notes_html = requests.get(URL).text
# soup = BeautifulSoup(release_notes_html, 'lxml')
# release_notes = soup.find('table', class_='highlight tab-size js-file-line-container
# js-code-nav-container js-tagsearch-file')
# info = []
# trs = release_notes.find_all('tr')
# for html in trs:
#     notes = html.find_all('td')[1].text
#     info.append(notes)
# info = concat_text(info)
# print(check_keyword(info))
# return check_keyword(info)


def check_package(package_name: str) -> str:
    if package_release_note_links[package_name]:
        release_notes = requests.get(package_release_note_links[package_name]).text
        # unique release-note page layout rules:
        if package_name in ['php7', 'php8']:
            soup = BeautifulSoup(release_notes, 'lxml')
            release_notes = soup.find('section', class_='version').text
            print(release_notes)
            print(check_keyword(release_notes))
            return check_keyword(release_notes)
        elif package_name in 'clamav':
            soup = BeautifulSoup(release_notes, 'lxml')
            release_notes = soup.find('div', class_='date-outer').text
            print(release_notes)
            print(check_keyword(release_notes))
            return check_keyword(release_notes)
        else:
            # other release-nte html layouts. this will work with any webpage that only contains information about
            #   the latest release. for any other format, rules must be written above accordingly.
            # text = ''
            # append_flag = 0
            # for i in range(len(release_notes)):
            #     if release_notes[i:i + 1] == '>':
            #         append_flag = 1
            #     elif append_flag == 1:
            #         if release_notes[i:i + 1] == '<':
            #             append_flag = 0
            #         else:
            #             text += release_notes[i:i + 1]
            soup = BeautifulSoup(release_notes, 'lxml')
            text = soup.text
            # text = text.strip()
            print(text)
            print(check_keyword(text))
            return check_keyword(text)
    else:
        return 'link_unknown'
