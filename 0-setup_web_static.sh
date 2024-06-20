#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

# install nginx
sudo apt-get install nginx -y
# create folders
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo "Hello Holberton" | sudo tee /data/web_static/releases/test/index.html
# symbolic link /data/web_static/current linked to /data/web_static/releases/test/
sudo ln -s /data/web_static/releases/test /data/web_static/current
# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown ubuntu:ubuntu -R /data/
sudo chmod -R 755 /data/
# Update the Nginx configuration to serve the content of /data/web_static/current/
echo "server {
        listen 80 default_server;
        listen [::]:80 default_server;

        server_name _;

        root /var/www/html;
        index index.htm index.html index.nginx-debian.html;

        location / {
                try_files $uri $uri/ =404;
                add_header X-Served-By $hostname;
        }
        location /hbnb_static/ {
                alias /data/web_static/current/;
                autoindex off;
        }

        rewrite ^/redirect_me/?$ http://wanyama-ken.tech/ permanent;

        error_page 404 /custom_404.html;
        location = /custom_404.html {
            internal;
        }

}" | sudo tee /etc/nginx/sites-enabled/default

# check nginx conf file
sudo nginx -t

# restart nginx
Sudo service nginx restart