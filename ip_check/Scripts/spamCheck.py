"""
this script's purpose is to receive an ip and check it in multiple dnsbl servers lists to make sure it's not
blocked.
then it returns the results and the current time in the list format.
"""

from datetime import datetime
from pydnsbl.providers import BASE_PROVIDERS, Provider
import pydnsbl


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
            'dul.dnsbl.sorbs.net',
            'http.dnsbl.sorbs.net',
            'smtp.dnsbl.sorbs.net',
            'misc.dnsbl.sorbs.net',
            'socks.dnsbl.sorbs.net',
            'zombie.dnsbl.sorbs.net',
            'web.dnsbl.sorbs.net',
            'sbl.spamhaus.org',
            'pbl.spamhaus.org',
            'xbl.spamhaus.org',
            'ubl.unsubscore.com',
            'rbl.spamlab.com',
            'cdl.anti-spam.org.cn',
            'cbl.anti-spam.org.cn',
            'dnsbl.inps.de',
            'httpbl.abuse.ch',
            'short.rbl.jp',
            'rbl.suresupport.com',
            'spamguard.leadmon.net',
            'dsn.rfc-ignorant.org',
            'netblock.pedantic.org',
            'opm.tornevall.org',
            'multi.surbl.org',
            'rbl.efnetrbl.org',
            'tor.dan.me.uk',
            'blackholes.mail-abuse.org',
            'relays.mail-abuse.org',
            'rbl-plus.mail-abuse.org',
            'access.redhawk.org',
            'query.senderbase.org',
            'csi.cloudmark.com',
            'truncate.gbudb.net'
        ]

    # # the providers which are both in BASE_PROVIDERS & anti abuse list
    # common_providers =\
    #     [
    #         'b.barracudacentral.org',
    #         'bl.spamcop.net',
    #         'bogons.cymru.com',
    #         'cbl.abuseat.org',
    #         'db.wpbl.info',
    #         'dnsbl.dronebl.org',
    #         'dnsbl.sorbs.net',
    #         'drone.abuse.ch',
    #         'dyna.spamrats.com',
    #         'ix.dnsbl.manitu.net',
    #         'korea.services.net',
    #         'noptr.spamrats.com',
    #         'psbl.surriel.com',
    #         'rbl.interserver.net',
    #         'spam.dnsbl.sorbs.net',
    #         'spam.spamrats.com',
    #         'spamrbl.imp.ch',
    #         'virbl.bit.nl',
    #         'virus.rbl.jp',
    #         'wormrbl.imp.ch',
    #         'zen.spamhaus.org'
    #     ]
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

        print([ip, blacklisted_providers, failed_providers, time])

        return [ip, blacklisted_providers, failed_providers, time]
    except Exception as error:
        print([ip, str(error), 'ERROR!', str(datetime.now())])
        return [ip, str(error), 'ERROR!', str(datetime.now())]


if __name__ == '__main__':
    print('this is the updateCheck.py file.\nto run the program run the main.py file and make an API request to it.')
    check = check_ip('217.182.22.25')
    for i in check:
        print(i)
