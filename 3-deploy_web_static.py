#!/usr/bin/python3
"""Fabric script (based on the file 2-do_deploy_web_static.py) that creates
and distributes an archive to your web servers, using the function deploy:
"""
do_pack = __import__("1-pack_web_static").do_pack()

def deploy():
    """creates and distributes an archive to your web servers,
    """
    archive_path = 