#!/usr/bin/python

# importing the requests library
import sys
import requests
import os
import tarfile
import subprocess
from subprocess import call
import base64
import lic as l
from log import log
import banner as ban
import json

def Install():
	##Reading Config File
	fileDir = os.path.dirname(os.path.realpath('__file__'))
	filename = os.path.join(fileDir, 'config.json')
	with open(filename) as f:
		data = json.load(f)
	##########
	ban.main('Oracle java 1.8.0_161','/opt/oracle/java')
	sys.stdout.write("\033[1;32m")
	yes_no = raw_input("Do you want to continue(y/n): ")
	sys.stdout.write("\033[0m")
	if yes_no == 'y':
		lic = l.licensevalid()
		if lic == 'valid':

			os.system("sudo mkdir -p /opt/java/jre/")
			os.system("sudo chmod -R 777 /opt/java/jre")
			# Downloading Java File
			log('java.log','Downloading Jar File from Server ......!')
			#############Download FIles
			# downlink = '1xCQXiwGArwafbO4P7u_xGCI3HoocTgJb'
			# link = base64.b64decode('aHR0cDovL2JpdC5seS9nZG93bmxpbms=')
			# b = requests.get(link)
			# # javafile = requests.get('https://drive.google.com/uc?export=download&id=1xCQXiwGArwafbO4P7u_xGCI3HoocTgJb', stream=True, verify=True)
			# javafile = requests.get(b.url+downlink, stream=True, verify=False)
			# ###########################
			javafile = requests.get(data['java']['url'], stream=True, verify=False)
			if javafile.status_code == 200:
				with open('/opt/java/jre/server-jre-8u161-linux-x64.tar.gz', 'wb') as f:
					for chunk in javafile.iter_content(1024):
						f.write(chunk)
			tar = tarfile.open('/opt/java/jre/server-jre-8u161-linux-x64.tar.gz')
			tar.extractall(path='/opt/java/jre/')
			# os.makedirs('/opt/java/jre/current-jre/')
			# Creating Soft Link
			os.system("sudo ln -s /opt/java/jre/jdk1.8.0_161 /opt/java/jre/current-jre")
			# Append Java Configuration files
			if os.path.exists('/etc/profile.d/tsi.sh'):
				log('java.log','Java Configuration File Exists.....!')

			else :
				os.system("sudo touch /etc/profile.d/tsi.sh")
			os.system("sudo chown $(id -u):$(id -u) /etc/profile.d/tsi.sh")
			with open('/etc/profile.d/tsi.sh', 'a') as file:
	    			file.write('\n#java')
	    			file.write('\nexport JAVA_HOME=/opt/java/jre/current-jre')
	    			file.write('\n#export ANT_HOME=/opt/Java/jre/current-apache-ant')
	    			file.write('\n#export MAVEN_HOME=/opt/Java/jre/current-apache-maven')
	    			file.write('\n#gradle')
	    			file.write('\n#export GRADLE_HOME=/usr/local/gradle/current-gradle')
	    			file.write('\nexport PATH=$JAVA_HOME/bin:$PATH')
	    			file.write('\n#export PATH=$GRADLE_HOME/bin:$JAVA_HOME/bin:$ANT_HOME/bin:$MAVEN_HOME/bin:$PATH')
			os.system("sudo chown root:root /etc/profile.d/tsi.sh")
	    	#Deleting tar file
			os.remove('/opt/java/jre/server-jre-8u161-linux-x64.tar.gz')
			log('java.log','Oracle Java 1.8 is installed Successfully......!')
			#Banner
			ban.banjava()
			ban.banner('oracle java 1.8.0_161','na','/opt/oracle/java','/etc/profile.d/tsi.sh','na','/var/log/srx/java.log','na')
		else:
			print "Please Contact Script Owner"
	else:
		print "\n\t\033[1;31;40mScript terminated\033[0m"