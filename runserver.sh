LOGFILE=/var/log/gunicorn/ckw.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=8

test -d $LOGDIR || mkdir -p $LOGDIR

cd ..
source ./activate
cd chickenwing2
gunicorn --reload -D -w $NUM_WORKERS -b 0.0.0.0:3001 ChickenWing.wsgi:application --log-level=debug --log-file=$LOGFILE 2>>$LOGFILE
