import click
import os
import requests
import yaml
import socket
from pathlib import Path
from click_repl import repl as clickrepl
from prompt_toolkit.history import FileHistory


# import nacl.utils
# from nacl.public import PrivateKey, Box


# import libvirt
# import libxml2

# import json
import sys

with open('config.yaml', 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as e:
        print(f"E: {e}")


def download(img_src, img_dst, img_desc, force):
    filename = os.path.basename(img_dst)
    directory = os.path.dirname(img_dst)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if os.path.isfile(img_dst) and not force:
        print(f'File {img_dst} exists. You must use -f/--force to update/overwrite.')
    else:
        print(f'Downloading: {img_desc}')
        r = requests.get(img_src, stream=True)
        if r.status_code != requests.codes.ok:
            logging.log(level=logging.ERROR, msg='Unable to connect {0}'.format(img_src))
            r.raise_for_status()
        total_size = int(r.headers.get('Content-Length'))
        with click.progressbar(r.iter_content(1024), length=total_size) as bar, open(img_dst, 'wb') as file:
            for chunk in bar:
                file.write(chunk)
                bar.update(len(chunk))



CONTEXT_SETTINGS = dict(
    default_map=config['cli']
)

home_dir = str(Path.home())

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@click.group(help='A group that holds a subcommand')
def group():
    pass

def list_users(ctx, args, incomplete):
    users = [('bob', 'butcher'),
             ('alice', 'baker'),
             ('jerry', 'candlestick maker')]
    return [user for user in users if incomplete in user[0] or incomplete in user[1]]


@cli.command()
@click.option('--port', default=8000)
def runserver(port):
    click.echo('Serving on http://127.0.0.1:%d/' % port)

def display_ips():
    private_ip = get_private_ip()
    public_ip = get_public_ip()
    txt = (f'private ip: {private_ip}\n'
           f'public ip: {public_ip}'
          )
    print(txt)
    # sys.stdout.write(txt)

def get_private_ip():
    # socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    private_ip = s.getsockname()[0]
    s.close() 
    return private_ip

def get_public_ip():
    ip = requests.get('https://api.ipify.org').text
    return ip

@cli.command()
def show_ips():
    display_ips()
    pass

@cli.command()
@click.option('--port', default=8000)
def sync(port):
    click.echo('Syncing')
    click.echo('Port %s' % port)
    click.echo(str(Path.home()))


@cli.command()
@click.option('--img-src', default='https://cdimage.debian.org/cdimage/openstack/testing/debian-testing-openstack-amd64.qcow2')
@click.option('--img-dst', default=f'{home_dir}/.mycli/base-assets/base-os.qcow2')
@click.option('--img-desc', default=f'mycli base disk image')
# @click.option('-f', '--force/--no-force', default=False)
@click.option('-f', '--force', is_flag=True)
def update_base_assets(img_src, img_dst, img_desc, force):
    click.echo('Update Base Assets')
    download(img_src, img_dst, img_desc, force)


@group.command(help='Choose a user')
@click.argument('user', type=click.STRING, autocompletion=list_users)
@click.argument('home_dir', default=str(Path.home()))
def subcmd(user, home_dir):
    click.echo('Chosen user is %s' % user)
    click.echo('home_dir is %s' % home_dir)
    print(f'home_dir: {home_dir}')


@cli.command()
def repl():
    prompt_kwargs = {
        'history': FileHistory(f'{home_dir}/.mycli/repl-history'),
    }
    clickrepl(click.get_current_context(), prompt_kwargs=prompt_kwargs)

cli.add_command(group)

###TRASH###

# config_json = json.dumps(config)
# config_json = json.loads(config_json)
