CITY_ID=$1
EXPIRE_TIME_MINUTES=$2
REDIS_CLI=$3

if [[ -z $1 || -z $2 || -z $3 ]] ; then
	echo "Empty input" > /var/log/refresh.log
	echo "TEST" >> /home/artur/test.log
	exit
fi

SERVER_KEY="city_$CITY_ID"
echo $SERVER_KEY >> /home/artur/test.log
EXPIRE_SECONDS=$(( $EXPIRE_TIME_MINUTES * 60 ))
echo $EXPIRE_SECONDS >> /home/artur/test.log
$REDIS_CLI expire $SERVER_KEY $EXPIRE_SECONDS >> /home/artur/test.log
