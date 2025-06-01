#!/bin/sh

username=$1
webserver=$2
DATE=$(date +%F)

echo "Backup script started"

if [ -z "$username" ] || [ -z "$webserver" ]; then
    echo "Usage: $0 <username> <webserver>"
    exit 1
fi

if [ ! "$webserver" = "apache2" ] && [ ! "$webserver" = "nginx" ]; then
    echo "Invalid webserver: $webserver, must be either apache2 or nginx"
    exit 1
fi

BACKUP_FILE="/home/$username/workspace/backups/backup_$DATE.tar.gz"
LOG_FILE="/home/$username/workspace/backups/verify_$DATE.log"

echo "$DATE: Starting back up for $webserver server" >> $LOG_FILE

# Backup the required server files
if [ "$webserver" = "apache2" ]; then
    sudo tar -czf $BACKUP_FILE /etc/apache2 /var/www/html
elif [ "$webserver" = "nginx" ]; then
    sudo tar -czf $BACKUP_FILE /etc/nginx /usr/share/nginx/html
fi

echo "$DATE: Backup created: $BACKUP_FILE, starting verification" >> $LOG_FILE

# Verify the backup
sudo tar -tzf $BACKUP_FILE >> /dev/null 2>&1
echo "$DATE: Verification completed successfully" >> $LOG_FILE
echo "" >> $LOG_FILE

echo "Backup script for $username on $webserver Completed"