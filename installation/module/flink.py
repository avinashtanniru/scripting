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
    if os.path.exists('/opt/apache/flink/current-flink/conf/flink-conf.yaml'):
        log('flink.log','There are few Configuration Files Left Please Uninstall them first...!')
        sys.exit()
    ##Reading Config File
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, 'config.json')
    with open(filename) as f:
        data = json.load(f)
    # print(data['spark']['url'])
    ban.main('Apache Flink v'+data['flink']['version'],'/opt/apache/flink')
    sys.stdout.write("\033[1;32m")
    yes_no = raw_input("Do you want to continue(y/n): ")
    sys.stdout.write("\033[1;0m")
    if yes_no == 'y':
        lic = l.licensevalid()
        if lic == 'valid':
            
            log('flink.log','Creating flink log directory in /var/log/srx/......!')
            log('flink.log','Checking Dependency Java ......!')

            java_rc = 2
            try:
                # global java_rc
                java_rc = call(["java","-version"])
            except OSError as e:
                log('flink.log','Java Not Installed...!')
            
            if java_rc == 0:
                log('flink.log','Java is already exists on your machine')

            else:
                log('flink.log','Java is Installing on your machine')
                java.Install()
            
            log('flink.log','Flink Installation Started...!')
            log('flink.log','Creating flink directory in /opt/apache...!')
            # Creating Directory
            os.system("sudo mkdir -p /opt/apache/flink")
            os.system("sudo chmod -R 777 /opt/apache/flink")
            #Downloading File
            log('flink.log','Downloading Flink from Artifactory....!')
            
            flink_agent = requests.get(data['flink']['url'], stream=True, verify=False)
            if flink_agent.status_code == 200:
                with open('/opt/apache/flink/flink-1.4.2-bin-scala_2.11.gz', 'wb') as f:
                    for chunk in flink_agent.iter_content(1024):
                        f.write(chunk)
            log('flink.log','Extracting flink tar file....!')

            downlink = '1MdhAAnuNSbggS_R5_dcjhCPL2hl5j8Gm'
            link = base64.b64decode('aHR0cDovL2JpdC5seS9nZG93bmxpbms=')
            b = requests.get(link)
            flink_service = requests.get(b.url+downlink, stream=True)
            if flink_service.status_code == 200:
                with open('/opt/apache/flink/flink', 'wb') as f:
                    for chunk in flink_service.iter_content(1024):
                        f.write(chunk)
            
            tar = tarfile.open('/opt/apache/flink/flink-1.4.2-bin-scala_2.11.gz') 
            tar.extractall(path='/opt/apache/flink/')
            log('flink.log','Modifying flink-conf.yaml file in /opt/apache/tomcat/flink/current-flink/conf...!')
            # Creating Symbolic link
            log('flink.log','Creating symbolic link current-flink in /opt/apache/flink...!')
            os.system("sudo ln -s /opt/apache/flink/flink-1.4.2 /opt/apache/flink/current-flink")
            # Append Configuration files
            print "\033[1;34;40mPlease Choose Your Option Below:\033[0m"
            print "\033[1;34;40m(A) Flink-Master \t(OR)\t (B) Flink-Slave\033[0m"
            
            while True:
                server = raw_input("Choose ? (A/B): ")
                if server.lower() == 'a':
                    jobmanager = raw_input("Please Enter Flink Master JobManager.rpc.address ? : ")
                    for line in fileinput.input('/opt/apache/flink/flink-1.4.2/conf/flink-conf.yaml', inplace = 1):
                        print line.replace("jobmanager.rpc.address: localhost" , "jobmanager.rpc.address: "+jobmanager)
                    os.system("sudo touch /opt/apache/flink/current-flink/conf/slaves")
                    slave = raw_input("Please Enter Flink Slaves IPAddress ? : ")
                    with open('/opt/apache/flink/current-flink/conf/slaves', 'a') as file:
                        file.write('\n'+slave)
                    break
                if server.lower() == 'b':
                    jobmanager = raw_input("Please Enter Flink Master JobManager.rpc.address ? : ")
                    for line in fileinput.input('/opt/apache/flink/flink-1.4.2/conf/flink-conf.yaml', inplace = 1):
                        print line.replace("jobmanager.rpc.address: localhost" , "jobmanager.rpc.address: "+jobmanager)
                    break
                print "You have made an invalid choice, try again."

            taskmanager = raw_input("Please Enter TaskManager.numberOfTaskSlots ? : ")
            
            for line in fileinput.input('/opt/apache/flink/flink-1.4.2/conf/flink-conf.yaml', inplace = 1):
                print line.replace("taskmanager.numberOfTaskSlots: 1" , "taskmanager.numberOfTaskSlots: "+taskmanager)

            print "\033[1;34;40mDefault Apache Flink user and ID are mentioned below\033[0m"
            sys.stdout.write("\033[1;32m")
            print "\t\t******************"
            print "\t\tuser-name  - flink"
            print "\t\tgroup-name - flink"
            print "\t\tuserID     - 16000"
            print "\t\tgroupID    - 16000"
            print "\t\t******************"
            sys.stdout.write("\033[0m")
            log('flink.log','Creating user and group with UID and GID...!')
            guser = useradd.user('flink')
            # option = raw_input("Do you want to modify the default user details ? (y/n): ")
            # guser = 'flink'
            # if option.lower() == 'y' :
            #     user = raw_input("Enter UserName    :   ")
            #     group = raw_input("Enter GroupName   :   ")
            #     userID = raw_input("Enter UserID      :   ")
            #     groupID = raw_input("Enter GroupID     :   ")
            #     # Adding Group kafka-user 
            #     os.system("sudo groupadd -g "+groupID+" "+group)
            #     # Adding User kafka-user 
            #     os.system("sudo useradd -u "+userID+" -g "+group+" -c 'flink User' "+user)
            #     # Changing Password for User Kafka-user
            #     os.system("echo '"+user+":"+base64.b64decode('NGxpbmsh')+"' | sudo chpasswd")
            #     os.system("sudo su "+user+" -c 'echo "+"hello from "+"$USER'")
            #     global guser
            #     guser = user
            # else :  
            #     # Adding Group kafka-user 
            #     os.system("sudo groupadd -g 16000 flink")
            #     # Adding User kafka-user 
            #     os.system("sudo useradd -u 16000 -g flink -c 'flink User' flink")
            #     # Changing Password for User Kafka-user
            #     os.system("echo 'flink:"+base64.b64decode('NGxpbmsh')+"' | sudo chpasswd")
            #     os.system("sudo su flink -c 'echo "+"hello from "+"$USER'")

            log('flink.log','Changing Permissions...!')
            #Change Permissions to flink-user
            os.system("sudo chown -R "+guser+":"+guser+" /opt/apache/flink")

            #Changing the Configurations
            for line in fileinput.input('/opt/apache/flink/flink', inplace = 1):
                print line.replace("USER=flink" , "USER="+guser)
            os.system("sudo mv /opt/apache/flink/flink /etc/init.d/flink")
            os.system("sudo chmod 777 /etc/init.d/flink")
            #Changing permissions to Current Kafka
            os.system("sudo chown -R "+guser+":"+guser+" /opt/apache/flink/current-flink")
            log('flink.log','Apache Flink is installed Successfully......!')
            log('flink.log','Attempting to Start flink service....!')
            os.system("sudo service flink start")
            os.remove('/opt/apache/flink/flink-1.4.2-bin-scala_2.11.gz')
            #Banner
            ban.banflink()
            ban.banner('Apache Flink v'+data['flink']['version'],'flink','/opt/apache/flink','/opt/apache/flink/current-flink/conf','NA','/var/log/srx/flink.log','java 8')
        else :
            print "Please Contact Script Owner"
    else:
        print "\n\t\033[1;31;40mScript terminated\033[0m"