#!/usr/bin/python

# importing the requests library
import sys
import module.log
import module.nagios as nagios
import module.mongod as mongod
import module.kafka as kafka
import module.java as java
import module.zookeeper as zookeeper
import module.spark as spark
import module.mysql as mysql
import module.flink as flink
import module.tomcat as tomcat
import module.banner as b

sys.stdout.write("\033[1;32m") # Print below lines with Green
print "###### Choose the options to install the below packages ######"
print "#                                                            #"
print "#    1) Install Nagios Client                                #"
print "#    2) Install Apache Spark                                 #"
print "#    3) Install MongoDB                                      #"
print "#    4) Install Java JRE 1.8                                 #"
print "#    5) Install Zookeeper                                    #"
print "#    6) Install Kafka                                        #"
print "##############################################################"
option = raw_input("Please Enter Your Option ? : ")
sys.stdout.write("\033[0m") # Reset Print Colors

if option == '1' :
	print "111"
	b.main('Apache Kafka','/var/log')
	b.banner('name','service','dire','config','data','log','dep')
elif option == '2' :
	pass
elif option == '3' :
	pass
elif option == '4' :
	java.install
elif option == '5' :
	pass
elif option == '6' :
	kafka.Install()
elif option == '7' :
	java.Install()
else:
	print "Your Option is not correct"