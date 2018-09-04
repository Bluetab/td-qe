#! /bin/bash

SCRIPT=$0
OPTION=$1
PROJECT_PATH=/home/ec2-user/td_qe
ORACLE_HOME=/truedat/oracle/instantclient_11_2

main(){

  case "$OPTION" in
    (stop)
      stop
      exit 0
      ;;
    (start)
      start
      exit 0
      ;;
    (foreground)
      foreground
      exit 0
      ;;
    (status)
      status
      exit 0
      ;;
    (restart)
      stop
      start
      exit 0
      ;;
    (*)
      echo "Usage: $SCRIPT {stop|start|foreground|restart|status}"
      exit 2
      ;;
  esac
}

stop(){
  stringStatus=`status`
  if [[ ! -z ${stringStatus} ]]; then
    kill -9 `ps aux | grep gunicorn | grep td_qe | awk '{ print $2 }'`
  fi
}

start(){
  source ${PROJECT_PATH}/venv/bin/activate
  cd $PROJECT_PATH
  export ORACLE_HOME=$ORACLE_HOME
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME
  APP_ENV=Production gunicorn -c python:api.common.gunicorn wsgi --daemon
  status
}

foreground(){
  source ${PROJECT_PATH}/venv/bin/activate
  cd $PROJECT_PATH
  export ORACLE_HOME=$ORACLE_HOME
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME
  APP_ENV=Production gunicorn -c python:api.common.gunicorn wsgi
  status
}

status(){
  ps aux | grep gunicorn | grep td_qe
}

main
