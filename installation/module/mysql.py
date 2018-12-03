#!/usr/bin/python

# importing the requests library
import sys
import requests
import os
# import tarfile
# import subprocess
# import fileinput
# from subprocess import call
# import base64
import lic as l
from log import log
import json
import banner as ban
def Install():
	####
	if os.path.exists('/etc/my.cnf'):
		log('mysql.log','There are few Configuration Files Left Please Uninstall them first...!')
		sys.exit()
	##Reading Config File
	fileDir = os.path.dirname(os.path.realpath('__file__'))
	filename = os.path.join(fileDir, 'config.json')
	with open(filename) as f:
		data = json.load(f)
	# print(data['spark']['url'])
	ban.main('MySQL client v'+data['mysql']['version'],'NA')
	sys.stdout.write("\033[1;32m")
	yes_no = raw_input("Do you want to continue(y/n): ")
	sys.stdout.write("\033[0m")
	if yes_no == 'y':
		lic = l.licensevalid()
		if lic == 'valid':
			log('mysql.log','Downloading Mysql from Artifactory....!')
			
			def download(file):
				mysql_agent = requests.get(file, stream=True, verify=False)
				if mysql_agent.status_code == 200:
					with open('/tmp/'+file, 'wb') as f:
						for chunk in mysql_agent.iter_content(1024):
							f.write(chunk)

			download(data['mysql']['common'])
			download(data['mysql']['client'])
			download(data['mysql']['libs'])

			log('mysql.log','Installing Mysql ....!')
			os.system("sudo rpm -ivh /tmp/mysql-community-common-5.7.22-1.el7.x86_64.rpm")
			os.system("sudo rpm -ivh /tmp/mysql-community-libs-5.7.22-1.el7.x86_64.rpm")
			os.system("sudo rpm -ivh /tmp/mysql-community-client-5.7.22-1.el7.x86_64.rpm")

			#Deleting rpm file
			log('mysql.log','Deleteing Temporary Files......!')
			os.system("rm -rf /tmp/mysql-community-*")
			log('mysql.log','Mysql Client 5.7.22 is installed Successfully......!')
			#Banner
			ban.banmysql()
			ban.banner('mysql-clinet v'+data['mysql']['version'],'mysql','na','/etc/my.cnf','na','/var/log/srx/mysql.log','na')
		else:
			print "Please Contact Script Owner"
	else:                                    
		print "\n\t\033[1;31;40mScript terminated\033[0m"