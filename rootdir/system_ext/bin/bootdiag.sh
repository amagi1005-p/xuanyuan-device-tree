#!/system/bin/sh

D=/metadata/bootdiag

mkdir -p "$D"
chmod 0777 "$D"

rm -f "$D/logcat.txt" "$D/kmsg.start.txt" "$D/kmsg.latest.txt" "$D/getprop.start.txt" "$D/ps.start.txt" "$D/mounts.start.txt" "$D/cmdline.txt" "$D/state.txt"

echo "BOOTDIAG START" > "$D/start.txt"
date >> "$D/start.txt" 2>&1

getprop > "$D/getprop.start.txt" 2>&1
ps -AZ > "$D/ps.start.txt" 2>&1
cat /proc/mounts > "$D/mounts.start.txt" 2>&1
cat /proc/cmdline > "$D/cmdline.txt" 2>&1
dmesg > "$D/kmsg.start.txt" 2>&1

(
    while true; do
        logcat -b all -v threadtime >> "$D/logcat.txt" 2>&1
        echo "logcat exited rc=$?" >> "$D/state.txt"
        sleep 1
    done
) &

while true; do
    dmesg > "$D/kmsg.latest.tmp" 2>&1
    mv -f "$D/kmsg.latest.tmp" "$D/kmsg.latest.txt"
    echo >> "$D/state.txt"
    echo "===== $(date) =====" >> "$D/state.txt"
    getprop | grep -iE 'sys\.powerctl|bootreason|boot\.reason|boot_completed|keystore|keymint|keymaster|crypto|vold|zygote|shutdown|reboot' >> "$D/state.txt" 2>&1
    ps -AZ | grep -iE 'init|keystore|keymint|keymaster|vold|zygote|system_server|boot-service|hwservicemanager|servicemanager' >> "$D/state.txt" 2>&1
    sync
    sleep 2
done
