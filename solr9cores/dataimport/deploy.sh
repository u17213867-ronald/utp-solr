#!/bin/bash
envt=$1
rm -rf env
rm -rf __pycache__
rm -rf utils/__pycache__
aws s3 cp s3://infraestructura.neoauto.$envt/config/ec2/neoauto/$envt/solr/db-connection.json config/
aws s3 cp s3://infraestructura.neoauto.$envt/config/ec2/neoauto/$envt/solr/.env .
virtualenv -p python3.10 env
source ./env/bin/activate
pip3.10 install -r requirements.txt
pip3.10 list
deactivate
chown root:root -R *
systemctl restart flask
systemctl status flask
