"""
this script's purpose is to receive an ip and check it in multiple dnsbl servers lists to make sure it's not
blocked.
then it returns the results and the current time in the list format.
"""

import pydnsbl
from datetime import datetime
from pydnsbl.providers import BASE_PROVIDERS, Provider


def concat_text(list_input: list) -> str:
    # concat all the provider names resulted from check_ip operation into a ';' separated string.
    if len(list_input) == 0:
        return ''
    result = ''
    for text in list_input:
        result += f'{text};'
    result = result[0:-1]
    return result


def check_ip(ip: str) -> list:
    # get the blacklisted and timeout providers for both the anti_abuse providers and base ones.
    # then merge the results for both types and return them in ';' separated strings with current time and ip values.
    anti_abuse_servers_list = \
        [
            'cbl.abuseat.org',
            'bl.spamcop.net',
            'dnsbl.sorbs.net',
            'b.barracudacentral.org',
            'dul.dnsbl.sorbs.net',
            'http.dnsbl.sorbs.net',
            'smtp.dnsbl.sorbs.net',
            'misc.dnsbl.sorbs.net',
            'spam.dnsbl.sorbs.net',
            'socks.dnsbl.sorbs.net',
            'zombie.dnsbl.sorbs.net',
            'web.dnsbl.sorbs.net',
            'sbl.spamhaus.org',
            'pbl.spamhaus.org',
            'zen.spamhaus.org',
            'xbl.spamhaus.org',
            'ubl.unsubscore.com',
            'psbl.surriel.com',
            'dyna.spamrats.com',
            'rbl.spamlab.com',
            'spam.spamrats.com',
            'noptr.spamrats.com',
            'cdl.anti-spam.org.cn',
            'cbl.anti-spam.org.cn',
            'drone.abuse.ch',
            'dnsbl.inps.de',
            'korea.services.net',
            'httpbl.abuse.ch',
            'virus.rbl.jp',
            'short.rbl.jp',
            'wormrbl.imp.ch',
            'spamrbl.imp.ch',
            'rbl.suresupport.com',
            'virbl.bit.nl',
            'spamguard.leadmon.net',
            'dsn.rfc-ignorant.org',
            'netblock.pedantic.org',
            'opm.tornevall.org',
            'ix.dnsbl.manitu.net',
            'multi.surbl.org',
            'rbl.efnetrbl.org',
            'tor.dan.me.uk',
            'blackholes.mail-abuse.org',
            'relays.mail-abuse.org',
            'dnsbl.dronebl.org',
            'rbl-plus.mail-abuse.org',
            'db.wpbl.info',
            'access.redhawk.org',
            'query.senderbase.org',
            'rbl.interserver.net',
            'csi.cloudmark.com',
            'bogons.cymru.com',
            'truncate.gbudb.net'
        ]
    providers_list = []

    try:
        for provider in anti_abuse_servers_list:
            # TODO: modify the Provider class to return something other than 'unknown' if necessary.
            providers_list.append(Provider(provider))

        time = str(datetime.now())

        anti_abuse_ip_checker = pydnsbl.DNSBLIpChecker(providers=providers_list)
        result_anti_abuse = anti_abuse_ip_checker.check(ip)

        ip_checker_default = pydnsbl.DNSBLIpChecker(providers=BASE_PROVIDERS)
        result_default = ip_checker_default.check(ip)

        blacklisted_base_providers = concat_text(list(result_default.detected_by.keys()))
        blacklisted_anti_abuse_providers = concat_text(list(result_anti_abuse.detected_by.keys()))

        blacklisted_providers = blacklisted_base_providers + ';' + blacklisted_anti_abuse_providers

        failed_base_providers = concat_text(list(result_default.failed_providers))
        failed_anti_abuse_providers = concat_text(list(result_anti_abuse.failed_providers))

        failed_providers = failed_base_providers + ';' + failed_anti_abuse_providers

        return [ip, blacklisted_providers, failed_providers, time]
    except Exception as error:
        return [ip, str(error), 'ERROR!', str(datetime.now())]


if __name__ == '__main__':
    print('this is the updateCheck.py file.\nto run the program run the main.py file and make an API request to it.')
    check = check_ip('68.128.212.240')
    for i in check:
        print(i)
