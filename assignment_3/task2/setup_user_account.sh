#!/bin/sh

# Receive username and passkey as arguments from command line
# Example: ./setup_user_account.sh mike 123456
username=$1
passkey=$2

if [ -z "$username" ]; then
    echo "Invalid usage: username is required"
    echo "Pass arguments in the format: $0 <username> <passkey>"
    exit 1
fi

if [ -z "$passkey" ]; then
    current_timestamp=$(date +%s)
    passkey="$username@$current_timestamp"
    echo "No password provided, generated password for $username: $passkey"
fi

echo "Creating user account for $username..."
sudo useradd -m -s /bin/bash $username
echo "$username:$passkey" | sudo chpasswd
# Require user to change password on first login & after 30 days
# Also warn 7 days before expiry
sudo chage -M 30 -d 0 -W 3 $username

user_home_dir="/home/$username/workspace"
echo "Setting up workspace directory for $username at $user_home_dir"
sudo mkdir -p $user_home_dir
sudo chown $username:$username $user_home_dir
sudo chmod 700 $user_home_dir

if id -u $username >/dev/null 2>&1; then
    echo "User account created successfully"
else
    echo "User account creation failed"
fi