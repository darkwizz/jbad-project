#!/bin/bash
export STORAGE_HOST=localhost
export STORAGE_PORT=6379
export CITY_ID=3094802
export CITY_NAME=Krakow
export MODEL_SERVER_URL=localhost:7722
export EXPIRE_TIME_MINUTES=30
export REFRESH_TIME_MINUTES=5  # 15

if [[ -z $WEATHER_DB_PATH ]] ; then
	export WEATHER_DB_PATH=weather-db
fi

if [[ -z $API_KEY_PATH ]] ; then
	API_KEY_PATH=../weather-api.key
fi

if [[ -f $API_KEY_PATH ]] ; then
	export API_KEY=`cat $API_KEY_PATH`
fi

