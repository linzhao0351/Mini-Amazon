#!/bin/bash

echo "You may need to tweak .flashenv and db/setup.sh manually"
sudo apt-get -qq coreutils # On Mac, use brew install 
mypath=`realpath $0`
mybase=`dirname $mypath`
user=`whoami`
echo "Assume your database user name is: $user" # need to create a user in Postgres
read -p "Enter database password and press [ENTER]: " dbpasswd

secret=`tr -dc 'a-z0-9-_' < /dev/urandom | head -c50`
cd $mybase
cp -f flaskenv-template.env .flaskenv # create a copy flaskenv-lin.env, directly modify the file
sed -i "s/default_secret/'$secret'/g" .flaskenv # set it to some random string
sed -i "s/default_db_user/$user/g" .flaskenv # set it to linzhao, the postgres users
sed -i "s/default_db_password/$dbpasswd/g" .flaskenv # set it to postgres pwd

sudo apt-get -qq update # not necessary
sudo apt-get -qq --yes install python3-virtualenv # On Mac, use brew install pyenv-virtualenv
virtualenv env # not sure if need to run everytime
source env/bin/activate # statrt virtual env
pip install -r requirements.txt # directly run this line in shell
db/setup.sh # manually run
