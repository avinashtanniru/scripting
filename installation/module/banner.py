#!/usr/bin/python
# -*- coding: utf-8 -*-
# importing the requests library
import sys


def main(name,path):
	print "============================"
	print name + " Installer            "
	print "============================"

	if ("mysql" in name.lower()) or ("mongod" in name.lower()):
		print "\nThis script is going to install " +name
	else :
		print "\nThis script is going to install " +name+" in " +path
	if "mysql" in name.lower():
		print "\nBefore Installing MySql please remove Mariadb libraries."
	if "kafka" in name.lower():
		print "\nApache kafka supports only oracle java 8."
		print "\nIf the script didn’t find any java version,it will automatically install oracle java 1.8.0_161."
		print "\nMake sure zookeper service started before starting kafka service."
	if "zookeeper" in name.lower():
		print "\nApache Zookeeper supports only oracle java 8."
		print "\nIf the script didn’t find any java version,it will automatically install oracle java 1.8.0_161."
	if "spark" in name.lower():
		print "\nApache Spark supports only oracle java 8 and mongod-client."
		print "\nIf the script didn’t find any java and mongodb client, it will install oracle java 1.8.0_161 and mongodb client 3.4.15 by itself."
	if "flink" in name.lower():
		print "\nApache Flink supports only oracle java 8."
		print "\nIf the script didn’t find any java version,it will automatically install oracle java 1.8.0_161."
	print "\nIMPORTANT: This script should only be used on a clean installed system:"

	print "\n   RedHat Enterprise, CentOS, Fedora, Cloud Linux or Oracle"

def bankafka():
	sys.stdout.write("\033[1;36;40m")
	print " _       _  "
	print "| |     / / "
	print "| |    / / "
	print "| |   / /  "
	print "| |__/ /                _ _ _ _  _    _         "
	print "|  _  /         /\     |  _ _ _|| |  / /     /\ "
	print "| | \ \        /  \    | |      | | / /     /  \  "
	print "| |  \ \      / /\ \   | |_ _ _ | |/ /     / /\ \  "
	print "| |   \ \    / /  \ \  |  _ _ _||  _ \    / /  \ \  "
	print "| |    \ \  / / == \ \ | |      | | \ \  / / == \ \ "
	print "|_|     \_\/_/      \_\|_|      |_|  \_\/_/      \_\ "
	sys.stdout.write("\033[0m") # Reset Print Colors

def bannagios():
	sys.stdout.write("\033[1;36;40m")
	print " _        _ "
	print "| \      | |"                                                                                      
	print "|  \     | |"             
	print "| | \    | |               _ _ _ _ _ _  _ _ _ _ _ _ _   _ _ _ __     _ _ _ _ _ "
	print "| |\ \   | |      /\      |  _ _ _ _ _||_ _ _   _ _ _| /   _ _   \  |  _ _ _ _\ "
	print "| | \ \  | |     /  \     | |                | |      |  /     \  | | |"
	print "| |  \ \ | |    / /\ \    | |                | |      | |       | | | |"
	print "| |   \ \| |   / /  \ \   | |  _ _ _ _       | |      | |       | | | |_  _ _ _ "
	print "| |    \ | |  / / == \ \  | | |_ _  _ |      | |      | |       | | |_  _  _   |"                             
	print "| |     \  | / /      \ \ | |_ _ _ _| | _ _ _| |_ _ _ |  \_ _ _/  | _ _ _ _ _| |"                                  
	print "|_|      \_|/_/        \_\|_ _ _ _ _ _||_ _ _ _ _ _ _| \_ _ _ _ _/  \ _ _ _ _ _|"
	sys.stdout.write("\033[0m") # Reset Print Colors

def banjava():
	sys.stdout.write("\033[1;36;40m")
	print " _ _ _ _ _ _ _"
	print "|_ _ _   _ _ _|"
	print "      | |      "
	print "      | | "
	print "   _  | |      _       _    "
	print "  \ \ | |    /\\ \    / //\ "
	print "   \ \| |   /  \\ \  / //  \ "
	print "    \ | |  / /\ \\ \/ // /\ \ "
	print "     \  | / /= \ \\  // /= \ \ "
	print "      \_|/_/    \_\\//_/    \_\ "
	sys.stdout.write("\033[0m") # Reset Print Colors

def banmongo():
	sys.stdout.write("\033[1;36;40m")        
	print "|\          /|"
	print "| \        / |"
	print "|  \      /  |"
	print "|   \    /   |  _ _ _ _    _     _  _ _ _ _ _ _  _ _ _ _   _ _ _ __ "
	print "| |  \  /  | | /  _ _   \ |  \  | ||  _ _ _ _ / /  _ _  \ |  _ _ _ \ "
	print "| |\  \/  /| ||  /    \  || | \ | || |         |  /   \  || |     \ \ "
	print "| | \    / | || |      | || |\ \| || |  _ _ _ _| |     | || |      | | "
	print "| |  \  /  | || |      | || | \ | || | |_  _  || |     | || |      | | "
	print "| |   \/   | ||  \_ _ /  || |  \  || |_ _ _ | ||  \_ _/  || |_ _ _/ / "
	print "|_|        |_| \_ _ _ _ / |_|   \_||_ _ _ _ __| \_ _ _ _/ |_ _ _ __/  "
	sys.stdout.write("\033[0m") # Reset Print Colors    

def banspark():
	sys.stdout.write("\033[1;36;40m")                                                                                                      
	print  " _ _ _ _ _ _ "
	print  "|  _ _ _ _ _\ "                                                                            
	print  "| |            "                                                                    
	print  "| |           _ _ _ _             _ _ _ _    _    __ "
	print  "| |_ _  _  _ |  _ _  \    /\     |  _ _ _ \ | |  / / "                            
	print  "|_ _  _  _  || |    \ |  /  \    | |     \ \| | / /  "                                    
	print  "          | || |_ _ / | / /\ \   | | _ _ / /| |/ /   "                                 
	print  "          | ||  _ _ _/ / /  \ \  | | \   _/ |  _ \  "                                              
	print  " _ _ _ _ _| || |      / / == \ \ | |  \ \   | | \ \  "                                              
	print  "\ _ _ _ _ __||_|     /_/      \_\|_|   \ \  |_|  \ \ "                                                         
	print  "                                        \_\       \_\ "
	sys.stdout.write("\033[0m") # Reset Print Colors

def banzookeeper():
	sys.stdout.write("\033[1;36;40m")
	print " _ _ _ _ _ _  "
	print "|_ _ _ _ _  | "
	print "          | | " 
	print "         / /   "
	print "        / /   "
	print "       / /        _ _ _ _    _ _ _ _   _    _  _ _ _ _  _ _ _ _  _ _ _    _ _ _ _  _ _ _ _   "
	print "      / /        /  _ _  \  /  _ _  \ | |  / /|  _ _ _||  _ _ _||  _ _ \ |  _ _ _||  _ _  \  "
	print "     / /        |  /   \  ||  /   \  || | / / | |_ _ _ | |_ _ _ | |   \ || |_ _ _ | |    \ \ "
	print "    / /         | |     | || |     | || |/ /  |  _ _ _||  _ _ _|| |_ _/ ||  _ _ _|| | _ _/ | "
	print "   / /          | |     | || |     | ||  _ \  | |      | |      |  _ _ / | |      | | \  _/  "
	print "  / /_ _ _ _ __ |  \_ _/  ||  \_ _/  || | \ \ | |_ _ _ | |_ _ _ | |      | |_ _ _ | |  \ \   "
	print " /_ _ _ _ _ _ _| \_ _ _ _/  \_ _ _ _/ |_|  \_\|_ _ _ _||_ _ _ _||_|      |_ _ _ _||_|   \ \  "
	print "                                                                                         \_\ "
	sys.stdout.write("\033[0m") # Reset Print Colors

def banmysql():
	sys.stdout.write("\033[1;36;40m")
	print "|\            /|    "                                     
	print "| \          / |    "                                                             
	print "|  \        /  |    "                                                                     
	print "| | \      / | | _  "                           
	print "| |\ \    / /| |\ \    /\ _ _ _ _ _    _ _ _    _        "                                            
	print "| | \ \  / / | | \ \  / /|  _ _ _ _| /  _ _  \ | |       "                                                        
	print "| |  \ \/ /  | |  \ \/ / | |_ _ _ _ |  /   \  || |       "                                        
	print "| |   \  /   | |   \  /  |_ _ _ _  || |     | || |       "                          
	print "| |    \/    | |   / /    _ _ _ _| ||  \_ _/ / | |_ _ _  "                           
	print "|_|          |_|  /_/    |_ _ _ _ _| \ _ _ _ \ |_ _ _ _| "
	print "                                            \/ "   

def bantomcat():
	sys.stdout.write("\033[1;36;40m")
	print " _ _ _ _ _ _ _  "
	print "|_ _ _   _ _ _|  "                                                                        
	print "      | |         "                                                                         
	print "      | |  _ _ _ _   _      _   _ _ _ _          _ _ _ _ _ _ _  "
	print "      | | /  _ _  \ | \    / | /  _ _ _|     /\ |_ _ _   _ _ _| "                    
	print "      | ||  /   \  ||  \  /  ||  /          /  \      | |       "                               
	print "      | || |     | || | \/ | || |          / /\ \     | |       "                                                 
	print "      | || |     | || |\  /| || |         / /  \ \    | |       "                                               
	print "      | ||  \_ _/  || | \/ | ||  \_ _ _  / / == \ \   | |       "                                               
	print "      |_| \_ _ _ _/ |_|    |_| \ _ _ _ |/_/      \_\  |_|       "                                         

def banflink():
	sys.stdout.write("\033[1;36;40m")
	print " _ _ _ _ _ _  "
	print "|  _ _ _ _ _| "
	print "| |           _      _ _ _ _ _ _ _      _  _    _   "
	print "| |          | |    |_ _     _ _| \    | || |  / /  "
	print "| |_ _ _ _ _ | |         | |    |  \   | || | / /   "
	print "|  _ _ _ _ _|| |         | |    | | \  | || |/ /    "
	print "| |          | |         | |    | |\ \ | ||  _ \    "
	print "| |          | |         | |    | | \ \| || | \ \   "
	print "| |          | |_ __  _ _| |_ _ | |  \ \ || |  \ \  "
	print "|_|          |_ _ _ ||_ _ _ _ _||_|   \_ ||_|   \_\ "

def banner(name,service,dire,config,data,log,dep):
	print "\033[1;35;40m"+name+"\033[0m"
	sys.stdout.write("\033[1;33;40m") # Print below lines with Yellow                                                                                                     
	print "\nTITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITI\n"
	if "java" in name.lower():
		pass
	else :
		print "\033[1;33;40m\033[0m   \033[1;35;40mService               :    \033[1;34;40m"+service+"\033[1;33;40m"
	if ("mysql" in name.lower()) or ("mongo" in name.lower()):
		pass
	else :
		print "\033[1;33;40m\033[0m   \033[1;35;40mHome Directory        :    \033[1;34;40m"+dire+"\033[1;33;40m\n",
	if "mongo" in name.lower():
		pass
	else :
		print "\033[1;33;40m\033[0m   \033[1;35;40mConfig File           :    \033[1;34;40m"+config+"\033[1;33;40m\n",
	if ("kafka" in name.lower()) or ("zookeeper" in name.lower()):
		print "\033[1;33;40m\033[0m   \033[1;35;40mData Directory        :    \033[1;34;40m"+data+"\033[1;33;40m"
	else :
		pass
	# print "\n\033[1;33;40m\033[0m   \033[1;35;40mUser                  :    \033[1;34;40m"+user+" \033[1;33;40m"
	print "\033[1;33;40m\033[0m   \033[1;35;40mInstallationLog       :    \033[1;34;40m"+log+"\033[1;33;40m"
	if "na" in dep.lower():
		pass
	else :
		print "\033[1;33;40m\033[0m   \033[1;35;40mDependency package    :    \033[1;34;40m"+dep+"\033[1;33;40m"
	print "\n\033[1;33;40mTITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITITI\033[0m\n"