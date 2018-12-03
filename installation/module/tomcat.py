#!/usr/bin/python

# importing the requests library
import sys
import requests
import os
import tarfile
# import subprocess
import fileinput
# from subprocess import call
import base64
import lic as l
from log import log
import json
import useradd
import banner as ban

def Install():
	##Reading Config File
	fileDir = os.path.dirname(os.path.realpath('__file__'))
	filename = os.path.join(fileDir, 'config.json')
	with open(filename) as f:
		data = json.load(f)
	# print(data['spark']['url'])
	ban.main('Apache Tomcat v'+data['tomcat']['version'],'/opt/apache')
	sys.stdout.write("\033[1;32m")
	yes_no = raw_input("Do you want to continue(y/n): ")
	sys.stdout.write("\033[0m")
	if yes_no == 'y':
		lic = l.licensevalid()
		if lic == 'valid':
			log('tomcat.log','Creating tomcat log directory in /var/log/srx/....!')
			log('tomcat.log','Apache Tomcat Installation Started...!')
			# Creating Directory
			log('tomcat.log','Creating tomcat directory in /opt/apache....!')
			os.system("sudo mkdir -p /opt/apache/tomcat")
			os.system("sudo chmod -R 777 /opt/apache/tomcat")
			# Downloading File
			log('tomcat.log','Downloading Apache Tomcat from Artifactory....!')
			
			tomcat_agent = requests.get(data['tomcat']['url'], stream=True, verify=False)
			if tomcat_agent.status_code == 200:
				with open('/opt/apache/tomcat/apache-tomcat-8.5.27.tar.gz', 'wb') as f:
					for chunk in tomcat_agent.iter_content(1024):
						f.write(chunk)
			log('tomcat.log','Extracting tomcat tar file in /opt/apache/tomcat....!')
			tar = tarfile.open('/opt/apache/tomcat/apache-tomcat-8.5.27.tar.gz') 
			tar.extractall(path='/opt/apache/tomcat/')
			log('tomcat.log','Writing Apache Tomcat Configuration...!')
			# Move the config file
			# os.system("mv /opt/apache/tomcat/apache-tomcat-8.5.27/bin/autostart.sh /opt/apache/tomcat/apache-tomcat-8.5.27/bin/autostart_sh.orginal")
			# Download the Config File
			downlink = '1FksdY6-gHI4tIcQWXuiWtcyH9Mq6SCqa'
			link = base64.b64decode('aHR0cDovL2JpdC5seS9nZG93bmxpbms=')
			b = requests.get(link)
			tomcat_service = requests.get(b.url+downlink, stream=True)
			if tomcat_service.status_code == 200:
				with open('/opt/apache/tomcat/apache-tomcat-8.5.27/bin/autostart.sh', 'wb') as f:
					for chunk in tomcat_service.iter_content(1024):
						f.write(chunk)

			os.system("mv /opt/apache/tomcat/apache-tomcat-8.5.27/conf/tomcat-users.xml /opt/apache/tomcat/apache-tomcat-8.5.27/conf/tomcat-users.xml.original")
			xml_file = requests.get(b.url+'1INoyrxQYfiZa96bLX68E-Ejp4MMOyUVE', stream=True)
			if xml_file.status_code == 200:
				with open('/opt/apache/tomcat/apache-tomcat-8.5.27/conf/tomcat-users.xml', 'wb') as f:
					for chunk in xml_file.iter_content(1024):
						f.write(chunk)

			print "\033[1;34;40mDefault Apache Tomcat user and ID are mentioned below\033[0m"
			sys.stdout.write("\033[1;32m")
			print "\t\t******************"
			print "\t\tuser-name  - tomcat"
			print "\t\tgroup-name - tomcat"
			print "\t\tuserID     - 15000"
			print "\t\tgroupID    - 15000"
			print "\t\t******************"
			sys.stdout.write("\033[0m")
			guser = useradd.user('tomcat')
			
			# option = raw_input("Do you want to modify the default user details ? (y/n) :")
			# guser = 'tomcat'
			# if option.lower() == 'y' :
			# 	user = raw_input("Enter UserName    :   ")
			# 	group = raw_input("Enter GroupName   :   ")
			# 	userID = raw_input("Enter UserID      :   ")
			# 	groupID = raw_input("Enter GroupID     :   ")
			# 	# Adding Group kafka-user 
			# 	os.system("sudo groupadd -g "+groupID+" "+group)
			# 	# Adding User kafka-user 
			# 	os.system("sudo useradd -u "+userID+" -g "+group+" -c 'tomcat User' "+user)
			# 	# Changing Password for User Kafka-user
			# 	# os.system("echo '"+user+":"+base64.b64decode('SzRma2FVMmVyIQ==')+"' | sudo chpasswd")
			# 	os.system("sudo su "+user+" -c 'echo "+"hello from "+"$USER'")
			# 	global guser
			# 	guser = user
			# else :  
			# 	# Adding Group kafka-user 
			# 	os.system("sudo groupadd -g 15000 tomcat")
			# 	# Adding User kafka-user 
			# 	os.system("sudo useradd -u 15000 -g tomcat -c 'tomcat User' tomcat")
			# 	# Changing Password for User Tomcat
			# 	# os.system("echo 'kafka-user:"+base64.b64decode('SzRma2FVMmVyIQ==')+"' | sudo chpasswd")
			# 	os.system("sudo su tomcat -c 'echo "+"hello from "+"$USER'")
	        # Editing User in tomcat autostart file
			log('tomcat.log','Modifying autostart.sh file in /opt/apache/tomcat/current-tomcat/bin....!')
			for line in fileinput.input('/opt/apache/tomcat/apache-tomcat-8.5.27/bin/autostart.sh', inplace = 1):
				print line.replace("export TOMCAT_USER=tom" , "export TOMCAT_USER="+guser)
			log('tomcat.log','Changing Permissions...!')
			#Change Permissions to flink-user
			os.system("sudo chown -R "+guser+":"+guser+" /opt/apache/tomcat")
			# Creating Symbolic link
			log('tomcat.log','Creating symbolic link current-tomcat in /opt/apache/tomcat....!')
			os.system("sudo ln -s /opt/apache/tomcat/apache-tomcat-8.5.27 /opt/apache/tomcat/current-tomcat")
			log('tomcat.log','Making Apache Tomcat service autostart on boot...!')
			os.system("sudo chkconfig --add "+guser)
			os.system("sudo chkconfig enable "+guser)
			log('tomcat.log','Creating symbolic link tomcat as as service file in /etc/init.d....!')
			os.system("sudo chmod -R 777 /opt/apache/tomcat")
			os.system("sudo ln -s /opt/apache/tomcat/apache-tomcat-8.5.27/bin/autostart.sh /etc/init.d/tomcat")
			os.system("sudo chmod 777 /etc/init.d/tomcat")
			#Changing permissions to Current Tomcat
			os.system("sudo chown -R "+guser+":"+guser+" /opt/apache/tomcat/current-tomcat")
			os.system("sudo find /opt/apache/tomcat/apache-tomcat-8.5.27/bin/ -type f -iname '*.sh' -exec chmod +x {} \;")
			log('tomcat.log','Attempting to start Apache Tomcat service...!')
			os.system("sudo service tomcat start")
			log('tomcat.log','Apache Tomcat is installed Successfully......!')
			os.remove('/opt/apache/tomcat/apache-tomcat-8.5.27.tar.gz')
			#Banner
			ban.bantomcat()
			ban.banner('Apache Tomcat v'+data['tomcat']['version'],'tomcat','/opt/apache/tomcat','/opt/apache/tomcat/current-tomcat/conf/','na','/var/log/srx/tomcat.log','na')
		else:
			print "Please Contact Script Owner"
	else:
		print "\n\t\033[1;31;40mScript terminated\033[0m"