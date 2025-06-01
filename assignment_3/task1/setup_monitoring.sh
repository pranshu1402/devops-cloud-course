#!/bin/sh

current_dir=$(pwd)
working_dir=$(echo "$(dirname $0)" | sed 's#^\./##; s#^\.##; s#^/##; s#/$##')

if [ -z "$working_dir" ]; then
    current_file_dir="$current_dir"
else
    current_file_dir="$current_dir/$working_dir"
fi

script_path="$current_file_dir/monitor.sh"
echo "Script path: $script_path"

# sudo cp $current_file_dir/monitor.sh $HOME/monitor.sh
# script_path="$HOME/monitor.sh"
# echo "Updated Script path: $script_path"

chmod +x $script_path

# Run monitoring script every minute
(crontab -l 2>/dev/null; echo "* * * * * /bin/sh $script_path >> /tmp/cron.log 2>&1") | crontab -
echo "Cron job added successfully"

sudo mkdir -p $current_file_dir/monitoring-logs

sudo apt update && sudo apt install -y htop nmon