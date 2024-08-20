#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py) that distributes an
archive to your web servers, using the function do_deploy:
"""
from fabric.api import put, run, env
from os import path

env.hosts = ['52.87.231.249', '54.157.147.24']

def do_deploy(archive_path):
    """Distributes an archive to the web servers.
    """
    try:
        if not (path.exists(archive_path)):
            return False

        put(archive_path, '/tmp/')
        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'.format(timestamp))
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C /data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* /data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.format(timestamp))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/web_static_{}/ /data/web_static/current'.format(timestamp))
    except:
        return False

    return True


"""def do_deploy(archive_path):
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
"""