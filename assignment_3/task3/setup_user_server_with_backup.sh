#!/bin/sh

username=$1
webserver=$2

if [ "$(id -u)" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

if [ -z "$username" ] || [ -z "$webserver" ]; then
    echo "Usage: $0 <username> <webserver>"
    exit 1
fi

if [ ! -d "/home/$username" ]; then
    echo "User $username does not exist"
    exit 1
fi

if [ ! "$webserver" = "apache2" ] && [ ! "$webserver" = "nginx" ]; then
    echo "Invalid webserver: $webserver, must be either apache2 or nginx"
    exit 1
fi

echo "Setting up $webserver server for $username with backup"

current_dir=$(pwd)
working_dir=$(echo "$(dirname $0)" | sed "s|^$current_dir/||;" | sed 's#^\./##; s#^\.##; s#^/##; s#/$##')

if [ -z "$working_dir" ]; then
    script_dir="$current_dir"
elif echo "$current_dir" | grep -q "^/home"; then
    script_dir="/$working_dir"
else
    script_dir="$current_dir/$working_dir"
fi

# Copy backup script to user's workspace
sudo cp $script_dir/backup_server.sh /home/$username/workspace/backup.sh
sudo chown $username:$username /home/$username/workspace/backup.sh
sudo chmod +x /home/$username/workspace/backup.sh

if [ ! -f "/home/$username/workspace/backup.sh" ]; then
    echo "Backup script not copied to user's workspace"
    exit 1
fi

# Switch to user's workspace
# sudo -u $username
# cd /home/$username/workspace
# If current working directory is not user's workspace, exit script
# if [ "$(pwd)" != "/home/$username/workspace" ]; then
#     echo "Current working directory is not user's workspace"
#     exit 1
# fi

# If nginx or apache2 is already installed and running, stop it
if [ "$(sudo systemctl is-active apache2)" = "active" ]; then
    sudo systemctl stop apache2
fi

if [ "$(sudo systemctl is-active nginx)" = "active" ]; then
    sudo systemctl stop nginx
fi

# Install apache2 or nginx inside user's workspace
if [ "$webserver" = "apache2" ]; then
    sudo apt-get update
    sudo apt-get install -y apache2
    sudo systemctl enable apache2 > /dev/null 2>&1
    sudo systemctl start apache2
elif [ "$webserver" = "nginx" ]; then
    sudo apt-get update
    sudo apt-get install -y nginx   
    sudo systemctl enable nginx
    sudo systemctl start nginx
fi

echo "Webserver $webserver installed and activated"

# Setup backups directory
sudo mkdir -p /home/$username/workspace/backups

# Create cron job
if [ -z "$(sudo crontab -u $username -l | grep -w "/home/$username/workspace/backup.sh")" ]; then
    (sudo crontab -u $username -l 2>/dev/null; echo "0 0 * * 2 /bin/sh /home/$username/workspace/backup.sh $username $webserver") | sudo crontab -u $username -
    echo "Cron job set up"
else
    echo "Cron job already exists"
fi

sudo sh $script_dir/backup_server.sh $username $webserver

echo "Backup script created and cron job set up"