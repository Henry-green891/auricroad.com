#!/bin/bash

export ENV_NAME="auricroad"

ENV_OPSTS="--no-site-packages --distribute"

unset PYTHONDONTWRITEBYTECODE
echo "Making Virtual Environment"
os="`uname -a`"
source `which virtualenvwrapper.sh`


cd $WORKON_HOME
mkvirtualenv --distribute $ENV_OPTS $ENV_NAME  -ppython3
cd -
workon $ENV_NAME
export DJANGO_SETTINGS_MODULE=$ENV_NAME.$ENV_NAME.settings.local
echo $VIRTUAL_ENV

#install requirements
if [ ! -d ${HOME}/.pip-packages ]
then
    mkdir -p ${HOME}/.pip-packages
fi


if [  -d $WORKON_HOME/auricroad/build/ ]
then
    rm -rf $WORKON_HOME/auricroad/build/
fi

if [ $? -ne 0 ]; then
    pip install --download ${HOME}/.pip-packages --exists-action w -r requirements-dev.txt
    pip install --no-index --exists-action w --find-links=file://${HOME}/.pip-packages/ -r requirements-dev.txt
else
    pip install -r requirements-dev.txt
fi

npm install

#check if postgres installed
RESULT=`psql -l | grep "auricroad" | wc -l | awk '{print $1}'`;
if test $RESULT -eq 0; then
    echo "Creating Database";
    psql -c "create role auricroad with createdb encrypted password 'auricroad' login;"
    psql -c "alter user auricroad superuser;"
    psql -c "create database auricroad with owner auricroad;"
else
    echo "Database exists"
fi

#run initial setup of database tables
python manage.py migrate

#link up with git!
if [ -d .git ]; then
  echo "Git exists";
else
    echo "Setting up Git"
    git init .
    git remote add origin "git@github.com:Lightmatter/auricroad.git"
    #todo - add all and make initial push
fi

#todo - git flow init

chmod +x manage.py
