#!/usr/bin/python

# importing the requests library
import os
import base64

def user(name):
	option = raw_input("Do you want to modify the default user details ? (y/n) :")
	guser = name
	if option.lower() == 'y' :
		user = raw_input("Enter UserName    :   ")
		group = raw_input("Enter GroupName   :   ")
		userID = raw_input("Enter UserID      :   ")
		groupID = raw_input("Enter GroupID     :   ")
		# Adding Group 
		os.system("sudo groupadd -g "+groupID+" "+group)
		# Adding User 
		os.system("sudo useradd -u "+userID+" -g "+group+" -c '"+guser+" User' "+user)
		# Changing Password for User
		if guser.lower() == 'flink' :
			os.system("echo '"+user+":"+base64.b64decode('NGxpbmsh')+"' | sudo chpasswd")
		elif guser.lower() == 'kafka-user' :
			os.system("echo '"+user+":"+base64.b64decode('SzRma2FVMmVyIQ==')+"' | sudo chpasswd")
		elif guser.lower() == 'spark' :
			os.system("echo '"+user+":"+base64.b64decode('dCRpMjAxOA==')+"' | sudo chpasswd")
		elif guser.lower() == 'tomcat' :
			pass
		elif guser.lower() == 'zookeeper-user' :
			os.system("echo '"+user+":"+base64.b64decode('WjBvS2VlcGVyVTJlciE=')+"' | sudo chpasswd")

		os.system("sudo su "+user+" -c 'echo "+"hello from "+"$USER'")
		# global guser
		guser = user
		return guser
	else :  
		if guser.lower() == 'flink' :
			# Adding Group flink-user 
			os.system("sudo groupadd -g 16000 flink")
			# Adding User flink-user 
			os.system("sudo useradd -u 16000 -g flink -c 'flink User' flink")
			# Changing Password for User flink-user
			os.system("echo 'flink:"+base64.b64decode('NGxpbmsh')+"' | sudo chpasswd")
			os.system("sudo su flink -c 'echo "+"hello from "+"$USER'")
			return guser
		elif guser.lower() == 'kafka-user' :
			# Adding Group kafka-user 
			os.system("sudo groupadd -g 13000 kafka-user")
			# Adding User kafka-user 
			os.system("sudo useradd -u 13000 -g kafka-user -c 'kafka-user User' kafka-user")
			# Changing Password for User Kafka-user
			os.system("echo 'kafka-user:"+base64.b64decode('SzRma2FVMmVyIQ==')+"' | sudo chpasswd")
			os.system("sudo su kafka-user -c 'echo "+"hello from "+"$USER'")
			return guser
		elif guser.lower() == 'spark' :
			# Adding Group spark-user 
			os.system("sudo groupadd -g 12000 spark")
			# Adding User spark-user 
			os.system("sudo useradd -u 12000 -g spark -c 'Spark User' spark")
			# Changing Password for User spark-user
			os.system("echo 'spark:"+base64.b64decode('dCRpMjAxOA==')+"' | sudo chpasswd")
			os.system("sudo su spark -c 'echo "+"hello from "+"$USER'")
			return guser
		elif guser.lower() == 'tomcat' :
			# Adding Group tomcat-user 
			os.system("sudo groupadd -g 15000 tomcat")
			# Adding User tomcat-user 
			os.system("sudo useradd -u 15000 -g tomcat -c 'tomcat User' tomcat")
			# Changing Password for User Tomcat
			# os.system("echo 'kafka-user:"+base64.b64decode('SzRma2FVMmVyIQ==')+"' | sudo chpasswd")
			os.system("sudo su tomcat -c 'echo "+"hello from "+"$USER'")
			return guser
		elif guser.lower() == 'zookeeper-user' :
			# Adding Group zookeeper-user 
			os.system("sudo groupadd -g 13500 zookeeper-user")
			# Adding User zookeeper-user 
			os.system(" sudo useradd -u 13500 -g zookeeper-user -c 'zookeeper-user User' zookeeper-user")
			# Changing Password for User zookeeper-user
			os.system("echo 'zookeeper-user:"+base64.b64decode('WjBvS2VlcGVyVTJlciE=')+"' | sudo chpasswd")
			os.system("sudo su zookeeper-user -c 'echo "+"hello from "+"$USER'")
			return guser