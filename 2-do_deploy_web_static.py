#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py) that distributes an
archive to your web servers, using the function do_deploy:
"""
import fabric
from fabric.api import put, run, env
import os

env.hosts = ['100.26.136.151', '54.157.147.24']


def do_deploy(archive_path):
    """Distributes an archive to the web servers.
    """
    if os.path.exists(archive_path):
        flname = archive_path.replace('versions/', '')
        arc_pth = archive_path.replace('versions/', '').replace('.tgz', '')
        put(archive_path, '/tmp/')
        run(f'mkdir -p /data/web_static/releases/{arc_pth}/')
        run(f'tar -xzf /tmp/{flname} -C /data/web_static/releases/{arc_pth}/')
        run(f'rm /tmp/{flname}')
        run(f'mv /data/web_static/releases/{arc_pth}/web_static/* /data/web_static/releases/{arc_pth}/')
        run(f'rm -rf /data/web_static/releases/{arc_pth}/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s /data/web_static/releases/{arc_pth}/ /data/web_static/current')
        return True
    else:
        return False
