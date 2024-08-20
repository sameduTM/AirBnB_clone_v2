#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py) that distributes an
archive to your web servers, using the function do_deploy:
"""
from fabric.api import put, run, env

env.hosts = ['52.87.231.249', '54.157.147.24']


def do_deploy(archive_path):
    """Distributes an archive to the web servers.
    """
    if archive_path:
        put(archive_path, '/tmp/')
        flname = archive_path.replace('versions/', '')
        arc_pth = archive_path.replace('versions/', '').replace('.tgz', '')
        run(f'mkdir -p /data/web_static/releases/{arc_pth}/')
        run(f'tar -xzf /tmp/{flname} -C /data/web_static/releases/{arc_pth}/')
        run(f'rm /tmp/{flname}')
        run(f'mv /data/web_static/releases/{arc_pth}/web_static/* /data/web_static/releases/{arc_pth}/')
        run(f'rm -rf /data/web_static/releases/{arc_pth}/web_static')
        run('rm -rf /data/web_static/current')
        run(
            f'ln -s /data/web_static/releases/{arc_pth}/ /data/web_static/current')

        return True
    else:
        return False
