#!/bin/sh

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

export FLASK_APP=server.py
export FLASK_ENV=development
flask run -p $PORT --host=0.0.0.0