#!/bin/sh

LOG_PATH=/tmp/weather-miner.log
if [[ $# -lt 3 ]] ; then
	echo "Not enough parameters" >> $LOG_PATH
	exit
fi

export CITY_ID=$1
PYTHON_PATH=$2
APP_PATH=$3

export WEATHER_DB_PATH=${APP_PATH%/*.*}/weather-db
export API_KEY_PATH=${APP_PATH%/*.*}/weather-api.key
echo "$API_KEY_PATH" >> $LOG_PATH
export API_KEY=$( cat $API_KEY_PATH )
# source $VARS_SH

echo "API KEY is $API_KEY" >> $LOG_PATH
echo "Weather DB is $WEATHER_DB_PATH" >> $LOG_PATH


$PYTHON_PATH $APP_PATH >> $LOG_PATH