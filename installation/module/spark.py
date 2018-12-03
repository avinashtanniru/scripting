#!/usr/bin/python

# importing the requests library
import sys
import requests
import os
import tarfile
import subprocess
# import fileinput
from subprocess import call
import base64
import lic as l
from log import log
import mongod
import java
import json
import useradd
import banner as ban
def Install():
	###Initial Checks
	if os.path.exists('/opt/apache/spark/current-spark/conf/spark-env.sh'):
		log('spark.log','There are few Configuration Files Left Please Uninstall them first...!')
		sys.exit()
	##Reading Config File
	fileDir = os.path.dirname(os.path.realpath('__file__'))
	filename = os.path.join(fileDir, 'config.json')
	with open(filename) as f:
		data = json.load(f)
	# print(data['spark']['url'])
	ban.main('Apache Spark v'+data['spark']['version'],'/opt/apache')
	sys.stdout.write("\033[1;32m")
	yes_no = raw_input("Do you want to continue(y/n): ")
	sys.stdout.write("\033[0m")
	if yes_no == 'y':
		lic = l.licensevalid()
		if lic == 'valid':
			log('spark.log','Creating spark log directory in /var/log/srx/....!')
			log('spark.log','Checking Dependency Mongo ......!')

			mongo_rc = 2
			try:

				mongo_rc = call(["mongo","-version"])
			except OSError as e:
				log('spark.log','Mongo Not Installed...!')
			
			if mongo_rc == 0:
				log('spark.log','Mongo is already exists on your machine')

			else:
				log('spark.log','Mongo is Installing on your machine')
				mongod.Install()

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
			
			log('spark.log','Apache Spark Installation Started...!')
			log('spark.log','Creating spark-user....!')

			print "\033[1;34;40mDefault Spark user and ID are mentioned below\033[0m"
			sys.stdout.write("\033[1;32m")
			print "\t\t******************"
			print "\t\tuser-name  - spark"
			print "\t\tgroup-name - spark"
			print "\t\tuserID     - 12000"
			print "\t\tgroupID    - 12000"
			print "\t\t******************"
			sys.stdout.write("\033[0m")
			guser = useradd.user('spark')
			
			# option = raw_input("Do you want to modify the default user details ? (y/n): ")
			# guser = 'spark'

			# if option.lower() == 'y' :
			# 	user = raw_input("Enter UserName    :   ")
			# 	group = raw_input("Enter GroupName   :   ")
			# 	userID = raw_input("Enter UserID      :   ")
			# 	groupID = raw_input("Enter GroupID     :   ")
			# 	# Adding Group kafka-user 
			# 	os.system("sudo groupadd -g "+groupID+" "+group)
			# 	# Adding User kafka-user 
			# 	os.system("sudo useradd -u "+userID+" -g "+group+" -c 'Spark User' "+user)
			# 	# Changing Password for User Kafka-user
			# 	os.system("echo '"+user+":"+base64.b64decode('dCRpMjAxOA==')+"' | sudo chpasswd")
			# 	os.system("sudo su "+user+" -c 'echo "+"hello from "+"$USER'")
			# 	global guser
			# 	guser = user
			# else :	
			# 	# Adding Group kafka-user 
			# 	os.system("sudo groupadd -g 12000 spark")
			# 	# Adding User kafka-user 
			# 	os.system("sudo useradd -u 12000 -g spark -c 'Spark User' spark")
			# 	# Changing Password for User Kafka-user
			# 	os.system("echo 'spark:"+base64.b64decode('dCRpMjAxOA==')+"' | sudo chpasswd")
			# 	os.system("sudo su spark -c 'echo "+"hello from "+"$USER'")

			#Creating Directory
			log('spark.log','Creating Directory Spark in /opt/apache')

			os.system("sudo mkdir -p /opt/apache/spark/")
			os.system("sudo chmod -R 777 /opt/apache/spark")
			#Downloading Spark File
			log('spark.log','Downloading Spark from Artifactory....!')

			spark_agent = requests.get(data['spark']['url'], stream=True, verify=False)
			
			if spark_agent.status_code == 200:
				with open('/opt/apache/spark/sparkpak-1.2.0-deploy.tgz', 'wb') as f:
					for chunk in spark_agent.iter_content(1024):
						f.write(chunk)
			log('spark.log','Extracting spark tar file in /opt/apache/spark....!')
			tar = tarfile.open('/opt/apache/spark/sparkpak-1.2.0-deploy.tgz') 
			tar.extractall(path='/opt/apache/spark/')
			
			# Add Envrionment Variables in Bashrc
			os.system("sudo chmod -R 777 /home/"+guser+"")
			with open('/home/'+guser+'/.bashrc', 'a') as file:
					file.write('\nexport SPARK_PAK=$HOME/sparkpak_1.2_deploy')
					file.write('\n. $SPARK_PAK/conf/spark-env.sh')
			os.system("sudo chmod -R 700 /home/"+guser+"")

			# Copy Files
			os.system("cp /opt/apache/spark/sparkpak_1.2_deploy/spark-2.3.0-bin-hadoop2.7/conf/spark-env.sh.template /opt/apache/spark/sparkpak_1.2_deploy/spark-2.3.0-bin-hadoop2.7/conf/spark-env.sh")
			# Change Permissions to spark

			# os.system("sudo chown "+guser+":"+guser+" /opt/apache/spark/sparkpak_1.2_deploy/spark-2.3.0-bin-hadoop2.7/conf/spark-env.sh")
			# Append Configuration files
			log('spark.log','Modifying saprk-env.sh file in /opt/apache/spark/current-spark/conf/....!')
			with open('/opt/apache/spark/sparkpak_1.2_deploy/spark-2.3.0-bin-hadoop2.7/conf/spark-env.sh', 'a') as file:
					file.write('\nSPARK_WORKER_PORT=7080')
					file.write('\nSPARK_WORKER_MEMORY=16g')
					file.write('\nSPARK_WORKER_CORES=8')
			#Change Permissions to spark
			os.system("sudo chown -R "+guser+":"+guser+" /opt/apache/spark")
			os.system("sudo chown -R "+guser+":"+guser+" /opt/apache/spark/sparkpak_1.2_deploy")
			# Create Link to Home Directory
			log('spark.log','Creating symbolic link current-spark in /opt/apache/spark....!')
			os.system("sudo ln -s /opt/apache/spark/sparkpak_1.2_deploy/spark-2.3.0-bin-hadoop2.7 /opt/apache/spark/current-spark")
			os.system("sudo ln -s /opt/apache/spark/sparkpak_1.2_deploy/ /home/"+guser+"")
			os.system("sudo chown -R "+guser+":"+guser+" /opt/apache/spark/current-spark")
			#########Choose Master Or Slave ##########
			print "\033[1;34;40mPlease Choose Your Option Below:\033[0m"
			print "\033[1;34;40m(A) Spark-Master \t(OR)\t (B) Spark-Slave\033[0m"
			
			while True:
					server = raw_input("Choose ? (A/B): ")
					if server.lower() == 'a':

					os.system("sudo cp /opt/apache/spark/current-spark/spark-2.3.0-bin-hadoop2.7/conf/slaves.template /opt/apache/spark/current-spark/spark-2.3.0-bin-hadoop2.7/conf/slaves")
					slave = raw_input("Please Enter Spark Slaves IPAddress ? : ")
					with open('/opt/apache/spark/current-spark/spark-2.3.0-bin-hadoop2.7/conf/slaves', 'a') as file:
						file.write('\n'+slave)

					#########Download Service########
					downlink = '1-HS7T00j9Q-0tSS-oFxEJoYQrkcayRdi'
					link = base64.b64decode('aHR0cDovL2JpdC5seS9nZG93bmxpbms=')
					s = requests.get(link)
					spark_service = requests.get(s.url+downlink, stream=True)
					if spark_service.status_code == 200:
						with open('/opt/apache/spark/spark.txt', 'wb') as f:
							for chunk in spark_service.iter_content(1024):
								f.write(chunk)

					#Changing the Configurations
					for line in fileinput.input('/opt/apache/spark/spark.txt', inplace = 1):
						print line.replace("USER=spark" , "USER="+guser)

					os.system("sudo mv /opt/apache/spark/spark.txt /etc/init.d/spark")
					os.system("sudo chmod 777 /etc/init.d/spark")
					log('spark.log','Attempting to Start Spark service from spark....!')
					os.system("sudo service spark start")
					break
				if server.lower() == 'b':
					print "This is a configured as slave only...!"
					break
				print "You have made an invalid choice, try again."
			#Deleting tar file
			os.remove('/opt/apache/spark/sparkpak-1.2.0-deploy.tgz')
			log('spark.log','Apache Spark is installed Successfully......!')
			#Banner
			ban.banspark()
			ban.banner('Apache Spark v'+data['spark']['version'],'spark','/opt/apache/spark','/opt/apache/Spark/current-spark/conf','NA','/var/log/srx/spark.log','java 8,mongo-client')
		else:
			print "Please Contact Script Owner"
	else:
		print "\n\t\033[1;31;40mScript terminated\033[0m" 