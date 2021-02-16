#!/bin/sh

MINING_APP_PATH=$( realpath weathergrabber.py )
PYTHON_PATH=$( which python )
CMD_PATH=$( realpath mine.sh )

TEMP_CRON=mycron
crontab -l > $TEMP_CRON
echo "*/15 * * * * $CMD_PATH $CITY_ID $PYTHON_PATH $MINING_APP_PATH" >> $TEMP_CRON


DISPATCHER_FILE=dispatcher_proxy.py
DISPATCHER_PATH=$( realpath $DISPATCHER_FILE )
REFRESH_TIME=$( python $DISPATCHER_FILE --register \
 -c $CITY_ID -m $MODEL_SERVER_URL -n $CITY_NAME -d $DISPATCHER_URL )

echo "*/$REFRESH_TIME * * * * $PYTHON_PATH $DISPATCHER_PATH --refresh \
 -c $CITY_ID -d $DISPATCHER_URL" >> $TEMP_CRON


crontab $TEMP_CRON
rm $TEMP_CRON


PTH_FILE='root.pth'

echo $PWD > $PTH_FILE
find $PWD -name __init__.py | awk -F'/__init' '{print $1}' >> root.pth
ENV_PATH=$( which python | awk -F'bin' '{print $1}' )
# echo $ENV_PATH

SITE_PACKAGES=$( find $ENV_PATH -name site-packages )
# echo $SITE_PACKAGES

cp $PTH_FILE $SITE_PACKAGES
# cleanup
rm $PTH_FILE


export FLASK_ENV=development
export FLASK_APP=server.py
export WEATHER_DB_PATH=${MINING_APP_PATH%/*.*}/weather-db

if [[ -z $CITY_ID || -z $CITY_NAME || -z $MODEL_SERVER_URL ]] ; then
	echo "City ID, city name and model server url should be specified"
	exit
fi


flask run -p $PORT --host=0.0.0.0