#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

# Install Nginx
apt-get update
apt-get -y install nginx
# Create the folder /data/ if it doesn’t already exist
# Create the folder /data/web_static/ if it doesn’t already exist
# Create the folder /data/web_static/releases/ if it doesn’t already exist
# Create the folder /data/web_static/shared/ if it doesn’t already exist
mkdir -p /data/web_static/shared/
# Create the folder /data/web_static/releases/test/ if it doesn’t already exist
mkdir -p /data/web_static/releases/test/
# Create a fake HTML file
echo '<html>
	<head>
	</head>
	<body>
		AirBnB
	</body>
      </html>' > /data/web_static/releases/test/index.html
# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder.
ln -sf /data/web_static/releases/test/ /data/web_static/current
# Give ownership of the /data/ folder to the ubuntu user AND group
chown -hR ubuntu:ubuntu /data/
# update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
sed -i '51 i \\n\tlocation /hbnb_static {\n\talias /data/web_static/current;\n\t}' /etc/nginx/sites-available/default
# restart Nginx
service nginx restart


