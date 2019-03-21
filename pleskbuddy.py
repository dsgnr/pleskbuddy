#!/usr/bin/env python
# pleskbuddy.py created by Dan Hand

from __future__ import absolute_import, division, print_function

# Standard Library
import argparse
import sys
from subprocess import call


__version__ = '1.0.0'


def options():
    psa_parser = argparse.ArgumentParser()
    psa_parser.add_argument('-v', '--version', dest='show_version',
                            action='store_true', help='Shows version information')
    psa_parser.add_argument('--sub-list', dest='subscription_list',
                            action='store_true', help='Shows a list of subscriptions')
    psa_parser.add_argument('--domain-list', dest='domain_list',
                            action='store_true', help='Shows a list of domains with their IP addresses')
    psa_parser.add_argument('--list-components', dest='show_components',
                            action='store_true', help='Creates a list of available components')
    psa_parser.add_argument('--install-component', dest='component_install', type=str,
                            help='Allows installation of available component')
    return psa_parser


# Check if Plesk is installed
try:
    CHECK_PSA = open('/usr/local/psa/version', 'r')
except IOError as ex:
    sys.exit('It doesn\'t look like Plesk is installed!')


class Color(object):
    RED = '\033[31m\033[1m'
    GREEN = '\033[32m\033[1m'
    YELLOW = '\033[33m\033[1m'
    BLUE = '\033[34m\033[1m'
    MAGENTA = '\033[35m\033[1m'
    CYAN = '\033[36m\033[1m'
    WHITE = '\033[37m\033[1m'
    RESET = '\033[0m'


# Variables
PSA_PARSER = options()
PSA_ARGS = PSA_PARSER.parse_args()


def show_version():
    print(Color.CYAN + r'''
           _           _    _               _     _
     _ __ | | ___  ___| | _| |__  _   _  __| | __| |_   _
    | '_ \| |/ _ \/ __| |/ / '_ \| | | |/ _` |/ _` | | | |
    | |_) | |  __/\__ \   <| |_) | |_| | (_| | (_| | |_| |
    | .__/|_|\___||___/_|\_\_.__/ \__,_|\__,_|\__,_|\__, |
    |_|                                             |___/

    version: %s ''' % (__version__), Color.RESET)


def subscription_list():
    print(Color.MAGENTA + '==== Plesk Subscription List ====' + Color.RESET)
    subscription_list = 'plesk bin subscription --list'
    call(subscription_list, shell=True)


def domain_list():
    print(Color.MAGENTA + '==== Plesk Domain List ====' + Color.RESET)
    domain_list = 'MYSQL_PWD=`cat /etc/psa/.psa.shadow` mysql -u admin -Dpsa -e"SELECT dom.id, dom.name, \
                   ia.ipAddressId, iad.ip_address FROM domains dom LEFT JOIN DomainServices d ON \
                   (dom.id = d.dom_id AND d.type = \'web\') LEFT JOIN IpAddressesCollections ia ON \
                   ia.ipCollectionId = d.ipCollectionId LEFT JOIN IP_Addresses iad ON iad.id = ia.ipAddressId"'
    call(domain_list, shell=True)


def show_components():
    print(Color.MAGENTA + '==== Plesk Component List ====' + Color.RESET)
    component_list = 'plesk installer --select-release-current --show-components'
    call(component_list, shell=True)


def component_install():
    call(['plesk', 'installer', '--select-release-current',
          '--install-component', PSA_ARGS.component_install])


def main():
    if PSA_ARGS.show_version:
        return show_version()
    if PSA_ARGS.subscription_list:
        return subscription_list()
    if PSA_ARGS.domain_list:
        return domain_list()
    if PSA_ARGS.show_components:
        return show_components()
    if PSA_ARGS.component_install:
        return component_install()
    return PSA_PARSER


if __name__ == '__main__':
    main()
