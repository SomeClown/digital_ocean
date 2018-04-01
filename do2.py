#!venv/bin/python3

import requests
import json
import click
from collections import abc

__author__ = "SomeClown"
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@packetqueue.net"

"""
Copyright 2018 by Teren Bryson

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

api_token = '152f7b796dfb2eb9709adc19d1674e1846fdb2017b1dc95707c6db19ec8058a2'
api_url_base = 'https://api.digitalocean.com/v2/'
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(api_token)}

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
EPILOG = 'Digital Ocean Droplets Utility'

color_black2 = "\033[1;30m"
color_red2_on = "\033[01;31m"
color_red2_off = "\33[00m"
color_green2 = "\033[1;32m"
color_yellow2 = "\033[1;33m"
color_blue2 = "\033[1;34m"
color_purple2 = "\033[1;35m"
color_cyan2 = "\033[1;36m"
color_white2 = "\033[1;37m"
color_off = "\33[00m"


@click.group()
def cli_init():
    """
    main entry point for command line interface of program
    """
    pass


def get_stuff(suffix: str):
    """
    return a python response object to calling object
    :param: suffix
    :return: json object
    """
    api_url = (api_url_base + suffix)
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    elif response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        return None
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code, api_url))
        return None
    elif response.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))
        return None
    elif response.status_code == 400:
        print('[!] [{0}] Bad Request'.format(response.status_code))
        return None
    elif response.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
        return None
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        return None


@click.command(options_metavar='[options]', short_help='Return account information')
def return_account_info():
    """
    Returns account information
    """
    get_account = get_stuff(suffix='account')
    click.echo()
    for k, v in get_account['account'].items():
        print(color_red2_on + '{0}'.format(k) + color_red2_off + ': {0}'.format(v))
    click.echo()


@click.command(options_metavar='[options]', short_help='Return list of available images')
def return_images():
    """
    Returns list of available images
    """
    get_images = get_stuff(suffix='images')
    click.echo()

    def print_dict(d):
        """
        
        :param d: 
        :return: 
        """
        for k, v in d.items():
            if isinstance(v, dict):
                # print(color_red2_on + '{0}: '.format(k))
                print_dict(v)
            elif isinstance(v, list):
                for item in v:
                    print(color_red2_on + 'Image: ' + color_red2_off + '{:45}'.format(item['name']) +
                          color_red2_on + 'Distribution: ' + color_red2_off + item['distribution'])
            else:
                click.echo()
                # print(color_red2_on + '{0}'.format(k) + color_red2_off + ': {0}'.format(v))
    print_dict(get_images)

cli_init.add_command(return_account_info, 'account')
cli_init.add_command(return_images, 'images')

cli_init()
