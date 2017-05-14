#!venv/bin/python3

import digitalocean
import click

with open('uid.txt', 'r') as f:
    uid = (f.readline().rstrip())
manager = digitalocean.Manager(token=uid)
keys = manager.get_all_sshkeys()


@click.group()
def cli_init():
    """
    main entry point for command line interface of program
    :return: 
    """
    pass


@click.command(options_metavar='[options]', short_help='Get my droplets')
@click.option('-t', '--tag', 'tag', help='search by tag')
def get_droplets(tag=''):
    """
    return a list of all of my current Digital Ocean droplets
    :return: 
    """
    if tag:
        my_droplets = manager.get_all_droplets(tag_name=tag)
        print(my_droplets)

    else:
        my_droplets = manager.get_all_droplets()
        print(my_droplets)


@click.command(options_metavar='[options]', short_help='Add tag to existing droplets')
@click.option('-t', '--tag', 'my_tag', help='tag to add')
@click.option('-i', '--id', 'droplet_id', help='ID of droplet to add tag to')
def add_tag(my_tag='', droplet_id=0):
    tag = digitalocean.Tag(token=uid, name=my_tag)
    tag.create()
    tag.add_droplets([droplet_id])


@click.command(options_metavar='[options]', short_help='Shut down all droplets')
def shutdown():
    my_droplets = manager.get_all_droplets()
    for droplet in my_droplets:
        droplet.shutdown()


@click.command(options_metavar='[options]', short_help='Create a droplet')
@click.option('-n', '--name', 'my_name', default='no-name', help='name of droplet to create (default = no_name)')
@click.option('-r', '--region', 'my_region', default='nyc1', help='region in which to create droplet (default = nyc1)')
@click.option('-i', '--image', 'do_image', default='coreos-beta', help='which image to use for droplet'
                                                                       '(default = coreos-beta)')
@click.option('-s', '-size', 'droplet_size', default='512mb', help='memory size of droplet (default = 512MB)')
@click.option('-a', '-another', 'another_size', default='512mb', help='some other size')
@click.option('-b', '--backup', 'do_backups', default=True, help='should this droplet be backed up (default=True)')
def create_droplet(my_name, my_region, do_image, droplet_size, another_size, do_backups):
    my_droplet = digitalocean.Droplet(token=uid,
                                      name=my_name,
                                      region=my_region,
                                      image=do_image,
                                      size_slug=droplet_size,
                                      size=another_size,
                                      backups=do_backups,
                                      ssh_keys=keys)

    my_droplet.create()
    actions = my_droplet.get_actions()
    for action in actions:
        action.load()
        print(action.status)

cli_init.add_command(get_droplets, 'get')
cli_init.add_command(add_tag, 'tag')
cli_init.add_command(shutdown, 'shutdown')
cli_init.add_command(create_droplet, 'create')

cli_init()
