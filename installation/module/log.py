#!/usr/bin/python

import os
from datetime import datetime

def log(name,message):
	print message
	f=open("/var/log/srx/"+name, "a+")
	f.write('['+str(datetime.now())+'] '+message+'\n')

os.system("sudo mkdir -p /var/log/srx")
os.system("sudo chown $(id -u):$(id -u) /var/log/srx")