#!/usr/bin/python

# importing the requests library
import sys, paramiko, time, getpass, re

# if len(sys.argv) < 4:
#     print "args missing"
#     sys.exit(1)

# hostname = sys.argv[1]
# password = sys.argv[2]
# command = sys.argv[3]

# username = "admin"
# port = 22
username = raw_input('Enter Userid:')
password = getpass.getpass(prompt='Password:')
with open('hostnames') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
print content
c = 1
for x in content:
	print x

	try:
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.WarningPolicy)

		client.connect(x, port=22, username=username, password=password)

		# stdin, stdout, stderr = client.exec_command('echo "@V!n@sh2" | sudo su; ls -l /root/')
		# print stdout.read()
		# stdin, stdout, stderr = client.exec_command('/bin/su root -c "smartctl -a /dev/sda > /tmp/smartctl_output"', get_pty=True)
		# stdin.write('\n')
		# stdin, stdout, stderr = client.exec_command('sudo -i ls -l /root/ > /tmp/root.txt')
		# stdin.write('@V!n@sh2\n')
		# stdin, stdout, stderr = client.exec_command('sudo -i -H -- echo $USER ; echo $USER > /tmp/user.txt')

		# stdin, stdout, stderr = client.exec_command('su - root', get_pty=True)
		stdin, stdout, stderr = client.exec_command('/bin/su root -c "smartctl -a /dev/sda > /tmp/smartctl_output"', get_pty=True)
		stdin.write('password\n')
		# stdin.flush()
		stdin, stdout, stderr = client.exec_command('ls -l /root/ > /tmp/root.txt')
		stdin.write(password+'\n')
		# stdin.flush()
		stdin, stdout, stderr = client.exec_command('id -un > /tmp/user.txt')
		stdin.write(password+'\n')
		stdin.flush()
		# data = stdout.read.splitlines()
		# for line in data:
		# 	if line.split(':')[0] == 'AirPort':
		# 		print line


		# stdin.flush()
		# print stdout.read()

		shell = client.invoke_shell()
		
		time.sleep(1)
		# shell.send('ls -l /root/ > /tmp/root'+str(c)+'.txt' + '\n')
		# time.sleep(1)
		# receive_buffer = shell.recv(1024)
		# print receive_buffer
		# time.sleep(2)
		shell.send("sudo su\n")
		time.sleep(1)
		shell.send(password + "\n")
		shell.send('/usr/bin/whoami > /tmp/user_shell.txt')
		time.sleep(1)
		shell.close()

		# ftp_client=client.open_sftp()
		# ftp_client.get('remotefileth','localfilepath')
		# ftp_client.close()
	finally:
		client.close()
	c += 1