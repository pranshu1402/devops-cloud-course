#!/bin/sh

if [ "$(id -u)" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

echo "Creating backup of PAM configuration..."
if [ ! -f /etc/pam.d/common-password.backup ]; then
    sudo cp /etc/pam.d/common-password /etc/pam.d/common-password.backup
else
    echo "Backup already exists"
fi

echo "Installing required packages..."
sudo apt-get update
sudo apt-get install -y libpam-pwquality

echo "Configuring password policy..."
sudo cat > /etc/pam.d/common-password << 'EOF'
password    requisite     pam_pwquality.so retry=3 minlen=12 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1 minclass=3
password    [success=1 default=ignore]  pam_unix.so obscure yescrypt
password    required      pam_deny.so
EOF

echo "Password policy has been configured with the following requirements:"
echo "- Minimum length: 12 characters"
echo "- Must contain at least one uppercase letter"
echo "- Must contain at least one lowercase letter"
echo "- Must contain at least one number"
echo "- Must contain at least one special character"

echo "Configuration completed successfully!"

