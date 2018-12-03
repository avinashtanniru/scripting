#!/usr/bin/python

# importing the requests library
import sys
import requests
import os
import tarfile
import subprocess
import fileinput
from subprocess import call
import base64
import lic as l
from log import log
import java
import json
import useradd
import banner as ban
def Install():
	###Inital Checks
	if os.path.exists('/opt/apache/zookeeper/current-zookeeper/conf/zoo.cfg'):
		log('kafka.log','There are few Configuration Files Left Please Uninstall them first...!')
		sys.exit()
	##Reading Config File
	fileDir = os.path.dirname(os.path.realpath('__file__'))
	filename = os.path.join(fileDir, 'config.json')
	with open(filename) as f:
		data = json.load(f)
	# print(data['spark']['url'])
	ban.main('Apache Zookeeper v'+data['zookeeper']['version'],'/opt/apache')
	sys.stdout.write("\033[1;32m")
	yes_no = raw_input("Do you want to continue(y/n): ")
	sys.stdout.write("\033[0m")
	if yes_no == 'y':
		lic = l.licensevalid()
		if lic == 'valid':
			log('zookeeper.log','Creating zookeeper log directory in /var/log/srx/......!')
			log('zookeeper.log','Checking Dependency Java ......!')

			java_rc = 2
			try:
				# global java_rc
				java_rc = call(["java","-version"])
			except OSError as e:
				log('zookeeper.log','Java Not Installed...!')
			
			if java_rc == 0:
				log('zookeeper.log','Java is already exists on your machine')

			else:
				log('zookeeper.log','Java is Installing on your machine')
				java.Install()

			log('zookeeper.log','Apache Zookeper Installation Started...!')
			log('zookeeper.log','Creating Directory Zookeeper in /opt/apache')
			log('zookeeper.log','Creating Zookeeper Data Directory in /u01/apps/apache')

			# Creating Directory
			os.system("sudo mkdir -p /opt/apache/zookeeper")
			os.system("sudo mkdir -p /var/opt/apache")
			os.system("sudo mkdir -p /u01/apps/apache/zookeeper/data")
			os.system("sudo chmod -R 777 /opt/apache/zookeeper")
			os.system("sudo chmod -R 777 /var/opt/apache")
			os.system("sudo chmod -R 777 /u01/apps/apache/zookeeper/data")


			# Downloading tar file
			log('zookeeper.log','Downloading Zookeeper from Artifactory....!')
			
			zookeeper = requests.get(data['zookeeper']['url'], stream=True, verify=False)
			if zookeeper.status_code == 200:
				with open('/opt/apache/zookeeper/zookeeper-3.4.12.tar.gz', 'wb') as f:
					for chunk in zookeeper.iter_content(1024):
						f.write(chunk)
			log('zookeeper.log','Extracting zookeeper tar file....!')
			tar = tarfile.open('/opt/apache/zookeeper/zookeeper-3.4.12.tar.gz')
			tar.extractall(path='/opt/apache/zookeeper/')

			log('zookeeper.log','Creating user and group with UID and GID....!')

			print "\033[1;34;40mDefault Zookeeper user and ID are mentioned below\033[0m"
			sys.stdout.write("\033[1;32m")
			print "\t\t******************"
			print "\t\tuser-name  - zookeeper-user"
			print "\t\tgroup-name - zookeeper-user"
			print "\t\tuserID     - 13500"
			print "\t\tgroupID    - 13500"
			print "\t\t******************"
			sys.stdout.write("\033[0m")
			guser = useradd.user('zookeeper-user')
			
			# option = raw_input("Do you want to modify the default user details ? (y/n): ")
			# guser = 'zookeeper-user'
			# if option.lower() == 'y' :
			# 	user = raw_input("Enter UserName    :   ")
			# 	group = raw_input("Enter GroupName   :   ")
			# 	userID = raw_input("Enter UserID      :   ")
			# 	groupID = raw_input("Enter GroupID     :   ")
			# 	# Adding Group kafka-user 
			# 	os.system("sudo groupadd -g "+groupID+" "+group)
			# 	# Adding User kafka-user 
			# 	os.system("sudo useradd -u "+userID+" -g "+group+" -c 'zookeeper-user User' "+user)
			# 	# Changing Password for User Kafka-user
			# 	os.system("echo '"+user+":"+base64.b64decode('WjBvS2VlcGVyVTJlciE=')+"' | sudo chpasswd")
			# 	os.system("sudo su "+user+" -c 'echo "+"hello from "+"$USER'")
			# 	global guser
			# 	guser = user
			# else :	
			# 	# Adding Group zookeeper-user 
			# 	os.system("sudo groupadd -g 13500 zookeeper-user")
			# 	# Adding User zookeeper-user 
			# 	os.system(" sudo useradd -u 13500 -g zookeeper-user -c 'zookeeper-user User' zookeeper-user")
			# 	# Changing Password for User zookeeper-user
			# 	os.system("echo 'zookeeper-user:"+base64.b64decode('WjBvS2VlcGVyVTJlciE=')+"' | sudo chpasswd")
			# 	os.system("sudo su zookeeper-user -c 'echo "+"hello from "+"$USER'")

			log('zookeeper.log','Creating zoo.cfg file in /opt/apache/zookeeper/current-zookeeper/conf....!')
			# Creating zoo.cfg 
			with open('/opt/apache/zookeeper/zookeeper-3.4.12/conf/zoo.cfg', 'w+') as file:
	    			file.write('tickTime=2000')
	    			file.write('\ndataDir=/u01/apps/apache/zookeeper/data')
	    			file.write('\nclientPort=2181')
	    			file.write('\ninitLimit=10')
	    			file.write('\nsyncLimit=5')
	    			file.write('\n#server.1=zoo1:2888:3888')
			#Change Permissions to zookeeper-user
			os.system("sudo chown -R "+guser+":"+guser+" /opt/apache/zookeeper")
			os.system("sudo chown -R "+guser+":"+guser+" /u01/apps/apache/zookeeper")
			# Creating Symbolic link
			log('zookeeper.log','Creating symbolic link current-zookeeper in /opt/apache/zookeeper....!')
			os.system("ln -s /opt/apache/zookeeper/zookeeper-3.4.12 /opt/apache/zookeeper/current-zookeeper")
			# Creating Symbolic Link
			os.system("ln -s /u01/apps/apache/zookeeper/data /var/opt/apache/zookeeper")
			#Downloading New Zookeeper Service
			downlink = '1hDVsLUppGbbbeGHy4eCNBCoChHVSIQ9m'
			link = base64.b64decode('aHR0cDovL2JpdC5seS9nZG93bmxpbms=')
			b = requests.get(link)
			zoo_service = requests.get(b.url+downlink, stream=True)
			# zoo_service = requests.get('https://drive.google.com/uc?export=download&id=1hDVsLUppGbbbeGHy4eCNBCoChHVSIQ9m', stream=True)
			if zoo_service.status_code == 200:
				with open('/opt/apache/zookeeper/zookeeper.txt', 'wb') as f:
					for chunk in zoo_service.iter_content(1024):
						f.write(chunk)
			
			#Changing the Configurations
			for line in fileinput.input('/opt/apache/zookeeper/zookeeper.txt', inplace = 1):
				print line.replace("USER=zookeeper-user" , "USER="+guser)

			os.system("sudo mv /opt/apache/zookeeper/zookeeper.txt /etc/init.d/zookeeper")
			os.system("sudo chmod 777 /etc/init.d/zookeeper")
			os.system("sudo chown -R "+guser+":"+guser+" /opt/apache/zookeeper/current-zookeeper")
			log('zookeeper.log','Attempting to Start zookeeper service from zookeeper-user....!')
			# os.system("su zookeeper-user -c 'service zookeeper start'")
			os.system("sudo service zookeeper start")
			log('zookeeper.log','Zookeeper is successfully installed in /opt/apache/zookeeper/ ....!')
			# print "Data Directory : /u01/apps/apache"
			#Deleting tar file
			os.remove('/opt/apache/zookeeper/zookeeper-3.4.12.tar.gz')
			log('zookeeper.log','Apache Zookeeper is installed Successfully')
			#Banner
			ban.banzookeeper()
			ban.banner('Apache Zookeeper v'+data['zookeeper']['version'],'zookeeper','/opt/apache','/opt/apache/zookeeper/current-zookeeper/conf','/u01/apps/apache/zookeeper/data','/var/log/srx/zookeeper.log','java 8')
		else:
			print "Please Contact Script Owner"
	else:
		print "\n\t\033[1;31;40mScript terminated\033[0m"