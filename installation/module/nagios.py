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
import json
import banner as ban
def install():
	ban.main('Nagios client','/opt/nagios')
	lic = l.licensevalid()
	if lic == 'valid':
		#print lic
		if os.path.exists('/etc/nagios/nrpe.cfg'):
			log('nagios.log','There are few Configuration Files Left Please Uninstall them first...!')
			sys.exit()
		if os.path.exists('/usr/local/nagios/etc/nrpe.cfg'):
			log('nagios.log','There are few Configuration Files Left Please Uninstall them first...!')
			sys.exit()
		#Creating Directory
		log('nagios.log','Creating Directory in /opt ......!')
		# os.makedirs('/opt/nagios/nagiosclient/')
		os.system("sudo mkdir -p /opt/nagios/nagiosclient/")
		os.system("sudo chmod -R 777 /opt/nagios/nagiosclient")
		#Downloading Agent
		log('nagios.log','Downloading Nagios Agent from Nagios Server ........!')
		##Reading Config File
		fileDir = os.path.dirname(os.path.realpath('__file__'))
		filename = os.path.join(fileDir, 'config.json')
		with open(filename) as f:
			data = json.load(f)
		# print(data['spark']['url'])
		nrpe_agent = requests.get(data['nagios']['url'], stream=True)
		if nrpe_agent.status_code == 200:
			with open('/opt/nagios/nagiosclient/linux-nrpe-agent.tar.gz', 'wb') as f:
				for chunk in nrpe_agent.iter_content(1024):
					f.write(chunk)
		#Extracting
		tar = tarfile.open('/opt/nagios/nagiosclient/linux-nrpe-agent.tar.gz') 
		tar.extractall(path='/opt/nagios/nagiosclient/')
		#Installing
		log('nagios.log','Installing All Dependencies.......!')
		p = subprocess.Popen(['sudo', './fullinstall'], cwd='/opt/nagios/nagiosclient/linux-nrpe-agent/')
		p.wait()
		#Copying
		#os.rename('/usr/local/nagios/etc/nrpe.cfg', '/usr/local/nagios/etc/nrpe_cfg_bak')
		os.system('sudo cp /usr/local/nagios/etc/nrpe.cfg /usr/local/nagios/etc/nrpe_cfg_bak')
		#Downloading New NRPE Config
		# nrpe_config = requests.get('https://drive.google.com/uc?export=download&id=1eMCEUNDRClZVf1HVKFBdv5UK2PQh2lP-', stream=True)
		downlink = '1eMCEUNDRClZVf1HVKFBdv5UK2PQh2lP-'
		link = base64.b64decode('aHR0cDovL2JpdC5seS9nZG93bmxpbms=')
		b = requests.get(link)
		nrpe_config = requests.get(b.url+downlink, stream=True)
		if nrpe_config.status_code == 200:
			with open('/opt/nagios/nagiosclient/nrpe.cfg.txt', 'wb') as f:
				for chunk in nrpe_config.iter_content(1024):
					f.write(chunk)
		os.system('sudo mv /opt/nagios/nagiosclient/nrpe.cfg.txt /usr/local/nagios/etc/nrpe.cfg')
		# with open('/usr/local/nagios/etc/nrpe.cfg', 'a') as file:
	#   			file.write('\ncommand[check_users]=/usr/local/nagios/libexec/check_users -w 5 -c 10')
	#   			file.write('\ncommand[check_load]=/usr/local/nagios/libexec/check_load -w 80% -c 90%')
	#   			file.write('\ncommand[check_hda1]=/usr/local/nagios/libexec/check_disk -w 20% -c 10% -p /')
	#   			file.write('\ncommand[check_zombie_procs]=/usr/local/nagios/libexec/check_procs -w 5 -c 10 -s Z')
	#   			file.write('\ncommand[check_total_procs]=/usr/local/nagios/libexec/check_procs -w 600 -c 700')
	#   			file.write('\ncommand[check_uptime]=/usr/local/nagios/libexec/check_uptime')
	#   			file.write('\ncommand[check_ssh]=/usr/local/nagios/libexec/check_ssh -p 22 -H 127.0.0.1')
		#Deleting tar file
		log('nagios.log','Removing All Temp Files......!')
		os.remove('/opt/nagios/nagiosclient/linux-nrpe-agent.tar.gz')
		#Restart Xnited service
		log('nagios.log','Attempting to start xnited Service......!!')
		xnited = subprocess.Popen(['sudo', 'service', 'xinetd', 'restart'])
		xnited.wait()

		#Banner
		ban.bannagios()
		ban.banner('nagios client','xinetd','/opt/nagios','/usr/local/nagios/etc/nrpe.cfg','na','/var/log/srx/nagios.log','nagios host')
	else:
		print "Please Contact Script Owner"