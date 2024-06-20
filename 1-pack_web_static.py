#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the 
web_static folder of your AirBnB Clone repo, using the function do_pack
"""
from fabric.api import local
from datetime import datetime

def do_pack():
    x = datetime.now()
    local("mkdir -p versions")
    local(f"tar -cvzf versions/web_static_{x.year}{x.month}{x.day}{x.hour}{x.minute}{x.second}.tgz web_static")
