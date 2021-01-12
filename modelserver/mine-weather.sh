#!/bin/bash

if [[ $# -lt 3 ]] ; then
	echo "Not enough parameters"
	exit
fi

VARS_SH=$1
PYTHON_PATH=$2
APP_PATH=$3

source $VARS_SH

$PYTHON_PATH $APP_PATH
