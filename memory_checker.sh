# !/bin/bash
echo "Low memory alarm";
echo "Specify the trigger threshold in MB:"
read threshold;
echo "Specify url:";
read url;
memory_avaliable=`free -m | awk 'NR==2{printf "%s\n", $6 }'`;
while true; do
    if [ "$memory_avaliable" -lt "$threshold" ];
    then
        curl "$url"?memory="$memory_avaliable"
    fi;
    sleep 5s
done;