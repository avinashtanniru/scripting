#!/usr/bin/python

# importing the requests library
import sys
import getopt
import requests
import os
import tarfile
import json
import shutil
import paramiko
import time
import getpass

############Logging
import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='srxapps.log',level=logging.DEBUG)
logging.info('Script Started')
# logging.info('So should this')
# logging.warning('And this, too')
#################################

def tardir(path, tar_name):
	with tarfile.open(tar_name, "w:gz") as tar_handle:
		for root, dirs, files in os.walk(path):
			for file in files:
				tar_handle.add(os.path.join(root, file))

def shellcode(cfile):
	with open(cfile) as f:
		data = json.load(f)

	try:
		shutil.rmtree('/tmp/deploy')
		logging.warning('Removing Temp Directory')
	except OSError:
		print("Temp Directory Does Not Exists")
		logging.info('Temp Directory Does Not Exists')

			
	os.mkdir('/tmp/deploy')
	logging.info('Temp Folder created')
	sh = open("/tmp/deploy/deploy.sh", "w+")
	sh.write("#!/bin/bash\n")
	sh.write("cd /tmp/deploy/\n")
	for x in range(len(data['app-deployment'])):
		print x
		sh.write("service "+data['app-deployment'][x]['sname']+" stop\n")
		download = requests.get(data['app-deployment'][x]['url'], stream=True, verify=False)
		if download.status_code == 200:
			with open("/tmp/deploy/"+data['app-deployment'][x]['sname']+".tar.gz", 'wb') as f:
				for chunk in download.iter_content(1024):
					f.write(chunk)
		## Untar File
		# sh.write("mv "+data['app-deployment'][x]['extract']+"*.tar.gz "+data['app-deployment'][x]['extract']+"archive/")
		sh.write("tar -xvf "+data['app-deployment'][x]['sname']+".tar.gz -C "+data['app-deployment'][x]['extract']+"\n")
		tarname = tarfile.open("/tmp/deploy/"+data['app-deployment'][x]['sname']+".tar.gz")
		fdname = os.path.commonprefix(tarname.getnames())
		sh.write("chown -R "+data['app-deployment'][x]['user']+":"+data['app-deployment'][x]['user']+" "+data['app-deployment'][x]['extract']+fdname+"\n")
		# sh.write("ln -s "+data['app-deployment'][x]['extract']+data['app-deployment'][x]['link_folder']+" "+data['app-deployment'][x]['extract']+fdname+"\n")
		sh.write("for tar in $(find "+data['app-deployment'][x]['extract']+" -name '*.tar.gz'); do mv $tar $(dirname $tar)/archive; done\n")
		sh.write("unlink "+data['app-deployment'][x]['extract']+data['app-deployment'][x]['link_folder']+"\n")
		sh.write("ln -s "+data['app-deployment'][x]['extract']+fdname+" "+data['app-deployment'][x]['extract']+data['app-deployment'][x]['link_folder']+"\n")
		sh.write("chown -R "+data['app-deployment'][x]['user']+":"+data['app-deployment'][x]['user']+" "+data['app-deployment'][x]['extract']+data['app-deployment'][x]['link_folder']+"\n")
		sh.write("service "+data['app-deployment'][x]['sname']+" start\n")
		sh.write("cp "+data['app-deployment'][x]['sname']+".tar.gz "+data['app-deployment'][x]['extract']+fdname+".tar.gz\n")
	sh.write("rm -rf /tmp/tmp\n")
	sh.write("rm -rf /tmp/deploy\n")
	sh.write("rm -rf /tmp/app-deployment.tar.gz\n")	
	sh.close()
	logging.debug('Code written succesfully...!!!!')


def action(cfile, Hfile):
	username = raw_input('Enter Userid:')
	password = getpass.getpass(prompt='Password:')
	with open(Hfile) as f:
	    content = f.readlines()
	# you may also want to remove whitespace characters like `\n` at the end of each line
	content = [x.strip() for x in content]
	# print content
	for x in content:
		print "Attempting Connecting with - "+x
		logging.info('Attempting Connecting with - %s',x)
		try:
			client = paramiko.SSHClient()
			client.load_system_host_keys()
			client.set_missing_host_key_policy(paramiko.WarningPolicy)

			client.connect(x, port=22, username=username, password=password)
			logging.debug('Connected succesfully with - %s',x)

			shellcode(cfile)
			tardir('/tmp/deploy', '/tmp/app-deployment.tar.gz')
			print('Created tar file.')
			logging.info('Created tar file.')

			###SFTP
			print('Attempting to transfer files.')
			logging.info('Attempting to transfer files - %s',x)
			ftp_client=client.open_sftp()
			ftp_client.put('/tmp/app-deployment.tar.gz','/tmp/app-deployment.tar.gz')
			ftp_client.close()
			print('Files transfered succesfully.')
			logging.debug('Files transfered succesfully - %s',x)
			###Root
			# shell = client.invoke_shell()
			# shell.send("sudo su\n")
			# time.sleep(1)
			# shell.send(password + "\n")
			# time.sleep(1)
			# shell.send('tar -xvf /tmp/app-deployment.tar.gz -C /tmp/')
			# time.sleep(1)
			# shell.send('chmod +x /tmp/deploy/deploy.sh\n')
			# time.sleep(1)
			# shell.send('sh /tmp/deploy/deploy.sh\n')
			# time.sleep(1)
			# receive_buffer = shell.recv(1024)
			# print receive_buffer
			# shell.close()
			channel = client.invoke_shell()
			channel.send('sudo su\n')
			time.sleep(15)
			while not channel.recv_ready():
				time.sleep(1)
			print channel.recv(1024)
			channel.send(password+'\n')
			time.sleep(1)
			while not channel.recv_ready():
				time.sleep(1)
			print channel.recv(1024)
			# channel.send('id -un > /tmp/root.txt\n')
			channel.send('\n')
			while not channel.recv_ready():
				time.sleep(2)
			print channel.recv(1024)
			channel.send('tar -xvf /tmp/app-deployment.tar.gz -C /tmp/\n')
			time.sleep(8)
			while not channel.recv_ready():
				time.sleep(1)
			print channel.recv(1024)
			channel.send('mv /tmp/tmp/deploy /tmp/\n')
			time.sleep(1)
			while not channel.recv_ready():
				time.sleep(1)
			print channel.recv(1024)
			channel.send('chmod +x /tmp/deploy/deploy.sh\n')
			time.sleep(1)
			while not channel.recv_ready():
				time.sleep(1)
			print channel.recv(1024)
			channel.send('sh /tmp/deploy/deploy.sh > /tmp/deploy.log\n')
			time.sleep(5)
			while not channel.recv_ready():
				time.sleep(1)
			print channel.recv(1024)
			# channel.close()
		finally:
			client.close()
			os.remove("/tmp/app-deployment.tar.gz")
			shutil.rmtree('/tmp/deploy')
			print('Files & directories removed succesfully.')
			logging.debug('Files & directories removed succesfully. ')

def main(argv):
	cfile = ''
	Hfile = ''
	try:
		opts, args = getopt.getopt(argv,"hc:H:",["cfile=","Hfile="])
	except getopt.GetoptError:
		print 'test.py -c <configfile> -H <Hostfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -c <configfile> -H <Hostfile>'
			sys.exit()
		elif opt in ("-c", "--cfile"):
			cfile = arg
		elif opt in ("-H", "--Hfile"):
			Hfile = arg
	print 'Config file is "', cfile
	print 'Hostnames file is "', Hfile
	action(cfile, Hfile)
	logging.info('Script Execution Completed')


if __name__ == "__main__":
	main(sys.argv[1:])