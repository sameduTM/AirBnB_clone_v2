#!/usr/bin/env python3
"""Fabric script (based on the file 1-pack_web_static.py) that distributes an
archive to your web servers"""
from fabric.api import env
from fabric.operations import run, put

env.hosts = ['18.234.253.58', '54.158.192.203']
env.user = "ubuntu"


def do_deploy(archive_path):
    """function distributes an archive to your web servers"""
    arch_file = "web_static_2024620223022"
    if not archive_path:
        return False
    else:
        try:
            put(archive_path, "/tmp/")
            run("mkdir -p /data/web_static/releases/web_static_2024620223022/")
            run("tar -xzf /tmp/web_static_2024620223022.tgz -C\
                /data/web_static/releases/web_static_2024620223022/")
            run("rm /tmp/web_static_2024620223022.tgz")
            run(f"mv /data/web_static/releases/{arch_file}/web_static/*\
                /data/web_static/releases/web_static_2024620223022/")
            run("rm -rf /data/web_static/current")
            run("ln -s /data/web_static/releases/web_static_2024620223022/\
                /data/web_static/current")
            return True
        except Exception:
            return False
