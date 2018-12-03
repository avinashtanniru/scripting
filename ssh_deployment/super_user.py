#!/usr/bin/python2

import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('172.17.0.2', port=22, username='avinash', password='password')

# stdin, stdout, stderr = ssh.exec_command('/bin/su root -c "id -un > /tmp/root.txt"', get_pty=True)
# stdin.write('password\n')

# stdin, stdout, stderr = ssh.exec_command('sudo id -un > /tmp/user.txt')

# # [ add extra code here to execute a command ]

# stdin.flush()

# transport = ssh.get_transport()
# session = transport.open_session()
# session.set_combine_stderr(True)
# session.get_pty()
# #for testing purposes we want to force sudo to always to ask for password. because of that we use "-k" key
# session.exec_command("sudo id -un > /tmp/root.txt")
# session.exec_command("sudo id -un > /tmp/user.txt")

# stdin = session.makefile('wb', -1)
# stdout = session.makefile('rb', -1)
# #you have to check if you really need to send password here 
# stdin.write('password' +'\n')

# # session.exec_command("touch /tmp/user.txt")
# # stdin = session.makefile('wb', -1)
# # stdout = session.makefile('rb', -1)
# # #you have to check if you really need to send password here 
# # stdin.write('password' +'\n')

# stdin.flush()


channel = ssh.invoke_shell()
channel.send('sudo su\n')
while not channel.recv_ready():
    time.sleep(1)
print channel.recv(1024)
channel.send('password\n')
while not channel.recv_ready():
    time.sleep(1)
print channel.recv(1024)
channel.send('id -un > /tmp/root.txt\n')
while not channel.recv_ready():
    time.sleep(1)
print channel.recv(1024)
# stdin.flush()
# print (stdout.readlines())
ssh.close()