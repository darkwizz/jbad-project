#!/bin/sh

MINING_APP_PATH=$( realpath weathergrabber.py )
PYTHON_PATH=$( which python )
CMD_PATH=$( realpath mine-weather.sh )

TEMP_CRON=mycron
crontab -l > $TEMP_CRON
echo "*/15 * * * * $CMD_PATH $CITY_ID $PYTHON_PATH $MINING_APP_PATH" >> $TEMP_CRON
# crontab $TEMP_CRON
cat $TEMP_CRON
rm $TEMP_CRON
