#!/bin/bash

# run this having the project's root directory as current working directory
# searches for a current virtualenv's site-packages directory
# assuming virtualenv is activated and Python is run as `python`

echo $PWD > root.pth
find $PWD -name __init__.py | awk -F'/__init' '{print $1}' >> root.pth
ENV_PATH=$( which python | awk -F'bin' '{print $1}' )
# echo $ENV_PATH

SITE_PACKAGES=$( find $ENV_PATH -name site-packages )
# echo $SITE_PACKAGES

cp root.pth $SITE_PACKAGES
