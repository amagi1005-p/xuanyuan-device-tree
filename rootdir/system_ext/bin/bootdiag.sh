#!/system/bin/sh

D=/metadata/bootdiag

mkdir -p "$D"
chmod 0777 "$D"

rm -f "$D/logcat.txt" "$D/kmsg.start.txt" "$D/kmsg.latest.txt" "$D/getprop.start.txt" "$D/ps.start.txt" "$D/mounts.start.txt" "$D/cmdline.txt" "$D/state.txt" "$D/start.txt"

echo "BOOTDIAG START" > "$D/start.txt"
date >> "$D/start.txt" 2>&1

getprop > "$D/getprop.start.txt" 2>&1
ps -AZ > "$D/ps.start.txt" 2>&1
cat /proc/mounts > "$D/mounts.start.txt" 2>&1
cat /proc/cmdline > "$D/cmdline.txt" 2>&1
dmesg > "$D/kmsg.start.txt" 2>&1
dmesg > "$D/kmsg.latest.txt" 2>&1

# Keep diagnostics bounded. Never stream logcat into /metadata indefinitely.
logcat -b all -d -v threadtime -t 4000 > "$D/logcat.txt" 2>&1

echo "BOOTDIAG COMPLETE" > "$D/state.txt"
date >> "$D/state.txt" 2>&1
sync
exit 0
