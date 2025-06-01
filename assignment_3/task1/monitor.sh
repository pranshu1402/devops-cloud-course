#!/bin/sh

current_dir=$(pwd)
working_dir=$(echo "$(dirname $0)" | sed "s|^$current_dir/||;" | sed 's#^\./##; s#^\.##; s#^/##; s#/$##')

if [ -z "$working_dir" ]; then
    script_dir="$current_dir"
elif echo "$current_dir" | grep -q "^/home"; then
    script_dir="/$working_dir"
else
    script_dir="$current_dir/$working_dir"
fi

# log_dir="$HOME/logs/monitoring"

log_dir="$script_dir/monitoring-logs"

current_timestamp=$(date +%Y-%m-%d_%H-%M-%S)

echo "Starting monitoring within $log_dir at $current_timestamp..."

###################### Monitor CPU usage #####################
cpu_usage=$(top -b -n 1 | grep "Cpu(s)" | awk '{print $2 + $4}')
echo "$current_timestamp: CPU Usage: $cpu_usage%" >> $log_dir/cpu_usage.log

###################### Monitor memory usage #####################
memory_usage=$(free -m | awk 'NR==2{printf "%.2f%%", ($3/$2)*100}')
echo "$current_timestamp: Memory Usage: $memory_usage%" >> $log_dir/memory_usage.log

####################### Monitor top 5 memory consuming processes
top_memory_consuming_processes=$(ps aux --sort=-%mem | head -n 5)
echo "$current_timestamp: Top 5 Memory-consuming processes:" >> $log_dir/memory_consuming_processes.log
echo "$top_memory_consuming_processes" >> $log_dir/memory_consuming_processes.log
echo "" >> $log_dir/memory_consuming_processes.log

###################### Monitor disk usage #####################
disk_usage=$(df -h | awk 'NR==2{printf "%.2f%%", ($3/$2)*100}')
echo "$current_timestamp: Disk Usage: $disk_usage%" >> $log_dir/disk_usage.log

################ Monitor disk space usage by top 5 largest files/folders
disk_space=$(du -h $current_dir | sort -hr | head -n 5 | awk '{print $1}')
echo "$current_timestamp: Disk Space Usage: $disk_space" >> $log_dir/disk_space.log
echo "" >> $log_dir/disk_space.log

############## Monitor process usage ###########
process_usage=$(ps aux --sort=-%cpu | head -n 5)
echo "$current_timestamp: Top 5 CPU-consuming processes:" >> $log_dir/process_usage.log
echo "$process_usage" >> $log_dir/process_usage.log
echo "" >> $log_dir/process_usage.log

echo "$current_timestamp: Monitoring completed" >> $log_dir/audit.log

exit 0