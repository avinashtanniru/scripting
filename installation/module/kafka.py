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
	###Initial Checks
	if os.path.exists('/opt/apache/kafka/current-kafka/config/server.properties'):
		log('kafka.log','There are few Configuration Files Left Please Uninstall them first...!')
		sys.exit()
	##Reading Config File
	fileDir = os.path.dirname(os.path.realpath('__file__'))
	filename = os.path.join(fileDir, 'config.json')
	with open(filename) as f:
		data = json.load(f)
	# print(data['spark']['url'])
	ban.main('Apache Kafka v'+data['kafka']['version'],'/opt/apache')
	sys.stdout.write("\033[1;32m")
	yes_no = raw_input("Do you want to continue(y/n): ")
	sys.stdout.write("\033[0m")
	if yes_no == 'y':
		lic = l.licensevalid()
		if lic == 'valid':
			log('kafka.log','Creating kafka log directory in /var/log/srx/....!')
			log('kafka.log','Checking Dependency Java ......!')

			java_rc = 2
			try:
				# global java_rc
				java_rc = call(["java","-version"])
			except OSError as e:
				log('kafka.log','Java Not Installed...!')
			
			if java_rc == 0:
				log('kafka.log','Java is already exists on your machine')

			else:
				log('kafka.log','Java is Installing on your machine')
				java.Install()
			
			log('kafka.log','Apache Kafka Installation Started...!')
			log('kafka.log','Creating Directory Kafka in /opt/apache')
			log('kafka.log','Creating Kafka Data Directory in /u01/apps/apache')


			# Creating Directory
			os.system("sudo mkdir -p /var/opt/apache")
			os.system("sudo mkdir -p /opt/apache/kafka")
			os.system("sudo mkdir -p /u01/apps/apache/kafka/data")
			os.system("sudo mkdir -p /u01/apps/apache/kafka/log")
			os.system("sudo chmod -R 777 /var/opt/apache")
			os.system("sudo chmod -R 777 /opt/apache/kafka")
			os.system("sudo chmod -R 777 /u01/apps/apache/kafka/data")
			os.system("sudo chmod -R 777 /u01/apps/apache/kafka/log")


			# Downloading tar file
			log('kafka.log','Downloading Kafka from Apache Server....!')
			
			kafka = requests.get(data['kafka']['url'], stream=True, verify=True)
			if kafka.status_code == 200:
				with open('/opt/apache/kafka/kafka_2.11-1.0.1.tgz', 'wb') as f:
					for chunk in kafka.iter_content(1024):
						f.write(chunk)
			log('kafka.log','Extracting kafka tar file....!')
			tar = tarfile.open('/opt/apache/kafka/kafka_2.11-1.0.1.tgz')
			tar.extractall(path='/opt/apache/kafka/')
			log('kafka.log','Creating kafka-user....!')

			print "\033[1;34;40mDefault Kafka user and ID are mentioned below\033[0m"
			sys.stdout.write("\033[1;32m")
			print "\t\t******************"
			print "\t\tuser-name  - kafka-user"
			print "\t\tgroup-name - kafka-user"
			print "\t\tuserID     - 13000"
			print "\t\tgroupID    - 13000"
			print "\t\t******************"
			sys.stdout.write("\033[0m")
			guser = useradd.user('kafka-user')
			# option = raw_input("Do you want to modify the default user details ? (y/n): ")
			# guser = 'kafka-user'
			# if option.lower() == 'y' :
			# 	user = raw_input("Enter UserName    :   ")
			# 	group = raw_input("Enter GroupName   :   ")
			# 	userID = raw_input("Enter UserID      :   ")
			# 	groupID = raw_input("Enter GroupID     :   ")
			# 	# Adding Group kafka-user 
			# 	os.system("sudo groupadd -g "+groupID+" "+group)
			# 	# Adding User kafka-user 
			# 	os.system("sudo useradd -u "+userID+" -g "+group+" -c 'kafka-user User' "+user)
			# 	# Changing Password for User Kafka-user
			# 	os.system("echo '"+user+":"+base64.b64decode('SzRma2FVMmVyIQ==')+"' | sudo chpasswd")
			# 	os.system("sudo su "+user+" -c 'echo "+"hello from "+"$USER'")
			# 	global guser
			# 	guser = user
			# else :	
			# 	# Adding Group kafka-user 
			# 	os.system("sudo groupadd -g 13000 kafka-user")
			# 	# Adding User kafka-user 
			# 	os.system("sudo useradd -u 13000 -g kafka-user -c 'kafka-user User' kafka-user")
			# 	# Changing Password for User Kafka-user
			# 	os.system("echo 'kafka-user:"+base64.b64decode('SzRma2FVMmVyIQ==')+"' | sudo chpasswd")
			# 	os.system("sudo su kafka-user -c 'echo "+"hello from "+"$USER'")
			#Backup Server Config Files
			os.system('sudo cp /opt/apache/kafka/kafka_2.11-1.0.1/config/server.properties /opt/apache/kafka/kafka_2.11-1.0.1/config/server-orig.properties')
			#Changing the Configurations
			log('kafka.log','Modifying server.properties file in /opt/apache/kafka/current-kafka/config....!')
			for line in fileinput.input('/opt/apache/kafka/kafka_2.11-1.0.1/config/server.properties', inplace = 1):
				print line.replace("log.dirs=/tmp/kafka-logs" , "log.dirs=/u01/apps/apache/kafka/data")
			Allow_hosts = raw_input("Please Enter Zookeepers Server to connect ? (hostname:port): ")
			for line in fileinput.input('/opt/apache/kafka/kafka_2.11-1.0.1/config/server.properties', inplace = 1):
				print line.replace("zookeeper.connect=localhost:2181" , "zookeeper.connect="+Allow_hosts)
			
			#Change Permissions to Kafka-user
			os.system("sudo chown -R "+guser+":"+guser+" /opt/apache/kafka")
			os.system("sudo chown -R "+guser+":"+guser+" /u01/apps/apache/kafka")
			# Creating Symbolic link
			log('kafka.log','Creating symbolic link current-kafka in /opt/apache/kafka....!')
			os.system("sudo ln -s /opt/apache/kafka/kafka_2.11-1.0.1 /opt/apache/kafka/current-kafka")
			os.system("sudo ln -s /u01/apps/apache/kafka/log /opt/apache/kafka/current-kafka/log")

			# Creating Symbolic Link
			# os.system("sudo ln -s /u01/apps/apache/kafka/data /var/opt/apache/kafka")
			#Downloading New Zookeeper Service
			# zoo_service = requests.get('https://docs.google.com/document/d/1GmTLhhfwWesLNUylUsPNj9jYrnjoQZFKY4yujCFqORU/export?format=txt', stream=True)
			downlink = '1p38LrC6s1tiuD70HFHxS7SEaI3KRnRiU'
			link = base64.b64decode('aHR0cDovL2JpdC5seS9nZG93bmxpbms=')
			b = requests.get(link)
			# kafka_service = requests.get('https://drive.google.com/uc?export=download&id=1p38LrC6s1tiuD70HFHxS7SEaI3KRnRiU', stream=True)
			kafka_service = requests.get(b.url+downlink, stream=True)
			if kafka_service.status_code == 200:
				with open('/opt/apache/kafka/kafka.txt', 'wb') as f:
					for chunk in kafka_service.iter_content(1024):
						f.write(chunk)
			
			#Changing the Configurations
			for line in fileinput.input('/opt/apache/kafka/kafka.txt', inplace = 1):
				print line.replace("USER=kafka-user" , "USER="+guser)

			os.system("sudo mv /opt/apache/kafka/kafka.txt /etc/init.d/kafka")
			os.system("sudo chmod 777 /etc/init.d/kafka")

			log('kafka.log','Attempting to Start kafka service from kafka-user....!')

			# os.system("sudo su kafka-user -c 'service kafka start'")
			os.system("sudo service kafka start")

			log('kafka.log','Kafka is successfully installed in /opt/apache/kafka/ ....!')
			# log('kafka.log','Data Directory : /u01/apps/apache')

			#Deleting tar file
			os.remove('/opt/apache/kafka/kafka_2.11-1.0.1.tgz')
			#Changing permissions to Current Kafka
			os.system("sudo chown -R "+guser+":"+guser+" /opt/apache/kafka/current-kafka")
			log('kafka.log','Apache Kafka is installed Successfully......!')
			#Banner
			ban.bankafka()
			ban.banner('Apache Kafka v'+data['kafka']['version'],'kafka','/opt/apache/kafka','/opt/apache/kafka/current-kafka/config','/u01/apps/apache/kafka/data','/var/log/srx/kafka.log','java 8')
		else:
			print "Please Contact Script Owner"
	else:
		print "\n\t\033[1;31;40mScript terminated\033[0m"