#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import *
from os import path

env.hosts = ['3.90.80.254', '54.174.136.222']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploy web files to server"""
    if not path.exists(archive_path):
        return False

    try:
        # Extract timestamp from the archive filename
        timestamp = archive_path.split('_')[-1][:-4]

        # Create target directory
        release_dir = "/data/web_static/releases/web_static_{}/".format(timestamp)
        run('sudo mkdir -p {}'.format(release_dir))

        # Upload and uncompress archive
        put(archive_path, '/tmp/')
        run('sudo tar -xzf /tmp/{} -C {}'.format(archive_path, release_dir))

        # Remove the uploaded archive
        run('sudo rm /tmp/{}'.format(archive_path))

        # Move contents into the release directory
        run('sudo mv {}web_static/* {}'.format(release_dir, release_dir))

        # Remove extraneous web_static directory
        run('sudo rm -rf {}web_static'.format(release_dir))

        # Delete pre-existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('sudo ln -s {} /data/web_static/current'.format(release_dir))

        return True

    except Exception as e:
        print(e)
        return False
