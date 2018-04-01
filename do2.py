#!venv/bin/python3

import requests
import json
import click

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
        print(color_red2_on + '{:45}'.format(k) + color_red2_off + ':' + '{0}'.format(v))
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


@click.command(options_metavar='[options]', short_help='Return droplets information')
@click.option('-i', '--id', 'droplet_id', default=0, help='ID of droplet on which to request information')
def return_droplets(droplet_id):
    """
    :param: droplet_id
    :return: 
    """
    if droplet_id:
        print(color_red2_on + '\nNot yet implemented\n' + color_off)
        return
    else:
        click.echo()
        get_droplets = get_stuff(suffix='droplets')

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
                    print(color_red2_on + 'Name: ' + color_red2_off + item['name'])
                    print(color_red2_on + 'ID: ' + color_red2_off + str(item['id']))
                    print(color_red2_on + 'Memory: ' + color_red2_off + str(item['size']['slug']))
                    print(color_red2_on + 'vCPUs: ' + color_red2_off + str(item['vcpus']))
                    print(color_red2_on + 'Disk: ' + color_red2_off + str(item['disk']))
                    print(color_red2_on + 'Status: ' + color_red2_off + str(item['status']))
                    print(color_red2_on + 'Created: ' + color_red2_off + str(item['created_at']))
                    print(color_red2_on + 'Image Information: ' + color_red2_off)
                    print(color_blue2 + '\tID: ' + color_off + str(item['image']['id']))
                    print(color_blue2 + '\tName: ' + color_off + str(item['image']['name']))
                    print(color_blue2 + '\tDistribution: ' + color_off + str(item['image']['distribution']))
                    print(color_red2_on + 'Monthly Price: ' + color_red2_off + '$' +
                          str(item['size']['price_monthly']))
                    print(color_red2_on + 'Networking Information: ' + color_red2_off)
                    for thing, other_thing in item['networks'].items():
                        for address_stuff in other_thing:
                            print(color_blue2 + '\tip address: ' + color_off + address_stuff['ip_address'])
                            print(color_blue2 + '\tip net mask: ' + color_off + address_stuff['netmask'])
                            print(color_blue2 + '\tip gateway: ' + color_off + address_stuff['gateway'])
                            print(color_blue2 + '\tip type: ' + color_off + address_stuff['type'])
                            print('\t-----------------------')
                    print(color_red2_on + 'Region Name: ' + color_off + item['region']['name'] +
                          ' (' + color_yellow2 + item['region']['slug'] + color_off + ')')
                    print(color_red2_on + 'Tags: ' + color_red2_off + str(item['tags']))
            else:
                click.echo()
                # print(color_red2_on + '{0}'.format(k) + color_red2_off + ': {0}'.format(v))

    print_dict(get_droplets)

cli_init.add_command(return_account_info, 'account')
cli_init.add_command(return_images, 'images')
cli_init.add_command(return_droplets, 'droplets')

cli_init()
