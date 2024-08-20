#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py) that distributes an
archive to your web servers, using the function do_deploy:
"""
from fabric.api import put, run, env
import os

env.hosts = ['52.87.231.249', '54.157.147.24']


def do_deploy(archive_path):
    """Distributes an archive to the web servers.
    """
    if os.path.exists(archive_path):
        flname = archive_path.replace('versions/', '')
        arc_pth = archive_path.replace('versions/', '').replace('.tgz', '')
        put(archive_path, f'/tmp/{flname}')
        run(f'sudo mkdir -p /data/web_static/releases/{arc_pth}/')
        run(f'sudo tar -xzf /tmp/{flname} -C /data/web_static/releases/{arc_pth}/')
        run(f'sudo rm /tmp/{flname}')
        run(f'sudo mv /data/web_static/releases/{arc_pth}/web_static/* /data/web_static/releases/{arc_pth}/')
        run(f'sudo rm -rf /data/web_static/releases/{arc_pth}/web_static')
        run('sudo rm -rf /data/web_static/current')
        run(f'sudo ln -s /data/web_static/releases/{arc_pth}/ /data/web_static/current')
        return True
    else:
        return False
