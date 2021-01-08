#!/bin/bash
export FLASK_ENV=development
export FLASK_APP=server.py

if [[ -z $CITY_ID || -z $CITY_NAME || -z $MODEL_SERVER_URL ]] ; then
	echo "City ID, city name and model server url should be specified"
	exit
fi


SERVER_KEY="city_$CITY_ID"
redis-cli del $SERVER_KEY
redis-cli hset $SERVER_KEY name $CITY_NAME url $MODEL_SERVER_URL id $CITY_ID

# CRON_ALLOW=/etc/cron.allow
# echo $USER > $CRON_ALLOW

# set key refresh in crontab
TEMP_CRON=mycron
crontab -u $USER -l > $TEMP_CRON
REDIS_CLI=$( which redis-cli )
CMD_PATH=$( realpath server-checkpoint.sh )
# echo $CMD_PATH
echo "*/$REFRESH_TIME_MINUTES * * * * $CMD_PATH $CITY_ID $EXPIRE_TIME_MINUTES $REDIS_CLI" > $TEMP_CRON
crontab -u $USER $TEMP_CRON
rm $TEMP_CRON
# end


flask run -p 7722
crontab -u $USER -r
redis-cli del $SERVER_KEY