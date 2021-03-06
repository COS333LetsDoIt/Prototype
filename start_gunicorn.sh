APPNAME=prototype
APPDIR=/home/ec2-user/$APPNAME/

LOGFILE=$APPDIR'gunicorn.log'
ERRORFILE=$APPDIR'gunicorn-error.log'

NUM_WORKERS=3

ADDRESS=127.0.0.1:8001

cd $APPDIR

source ~/.bashrc
#workon $APPNAME

sudo service nginx restart

exec gunicorn $APPNAME.wsgi:application \
-w $NUM_WORKERS --bind=$ADDRESS \
--log-level=debug 
#--log-file=$LOGFILE 2>>$LOGFILE  1>>$ERRORFILE &