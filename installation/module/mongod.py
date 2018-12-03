#!/usr/bin/python

# importing the requests library
import sys
# import requests
# import tarfile
import os
import subprocess
from subprocess import call
import lic as l
from log import log
import banner as ban
def Install():
	ban.main('mongodb-client v3.4.15','NA')
	sys.stdout.write("\033[1;32m")
	yes_no = raw_input("Do you want to continue(y/n): ")
	sys.stdout.write("\033[0m")
	if yes_no == 'y':
		lic = l.licensevalid()
		if lic == 'valid':
			# os.remove('/etc/yum.repos.d/mongodb-org.repo')
			log('mongod.log','Creating Mongo Repo...!')
			with open('/tmp/mongodb-org.repo', 'w+') as file:
					file.write('[mongodb-org-3.4]')
					file.write('\nname=MongoDB 3.4 Repository')
					file.write('\nbaseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/3.4/x86_64/')
					file.write('\ngpgcheck=0')
					file.write('\nenabled=1')
			os.system("sudo mv /tmp/mongodb-org.repo /etc/yum.repos.d/")
			# os.system("sudo yum install mongodb-org -y")
			os.system("sudo yum install mongodb-org-shell -y")
			os.system("sudo yum install mongodb-org-mongos -y")

			log('mongod.log','Mongo CLient installed Successfully...!')
			#start MongoD service
			# mongod = subprocess.Popen(['service', 'mongod', 'start'])
			# mongod.wait()
			#Banner
			ban.banmongo()
			ban.banner('mongo-client v3.4.15','mongo,mongos','na','na','na','/var/log/srx/mongo.log','na')
		else:
			log('mongod.log','Please Contact Script Owner')
	else:
		print "\n\t\033[1;31;40mScript terminated\033[0m"