#!/bin/bash
export CITY_ID=3094802

API_KEY_PATH=../weather-api.key
if [[ -f $API_KEY_PATH ]] ; then
	export API_KEY=`cat $API_KEY_PATH`
fi

