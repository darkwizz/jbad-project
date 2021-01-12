#!/bin/bash

MINING_APP_PATH=$( realpath weathergrabber.py )
PYTHON_PATH=$( which python )
CMD_PATH=$( realpath mine-weather.sh )
VARS_SH_PATH=$( realpath init-vars.sh )

# echo $MINING_APP_PATH
# echo $PYTHON_PATH
# echo $VARS_SH_PATH
# echo $CMD_PATH

TEMP_CRON=mycron
crontab -u $USER -l > $TEMP_CRON
$CMD_PATH $VARS_SH_PATH $PYTHON_PATH $MINING_APP_PATH
# echo "*/30 * * * * $CMD_PATH $API_KEY $PYTHON_PATH $MINING_APP_PATH" >> $TEMP_CRON
# crontab -u $USER $TEMP_CRON
rm $TEMP_CRON