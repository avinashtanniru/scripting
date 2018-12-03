#!/usr/bin/python

import os
import subprocess

print '\033[1;37mStarting Mariadb Service..........!\033[1;m'
os.system("service mariadb start")
print '\033[1;37mChanging permission to file systems.\033[1;m'
os.system("setenforce 0")
print '\033[1;37mStarting Docker Service...........!\033[1;m'
os.system("service docker start")
os.system("docker start smolive")
os.system("docker exec smolive ./home/start.sh")

ipeth = subprocess.check_output("/sbin/ip -o -4 addr list enp0s25 | awk '{print $4}' | cut -d/ -f1", shell = True)
ipwlan = subprocess.check_output("/sbin/ip -o -4 addr list wlp3s0 | awk '{print $4}' | cut -d/ -f1", shell = True)

with open('/var/www/html/phpMyAdmin/config.inc.php', 'r') as file:
    # read a list of lines into data
    data = file.readlines()

if (ipeth.strip() != ''):
   data[26] = "$cfg['Servers'][$i]['host'] = '"+ ipeth.strip() +"';\n"
else:
   data[42] = "$cfg['Servers'][$i]['host'] = '"+ ipwlan.strip() +"';\n"

with open('/var/www/html/phpMyAdmin/config.inc.php', 'w') as file:
    file.writelines( data )

print '\033[1;32m************Script Completed Successfully************\033[1;m'
