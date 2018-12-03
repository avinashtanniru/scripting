#!/usr/bin/python

# importing the requests library
import sys, paramiko, time, getpass

with open('hostnames') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
print content
for x in content:
	print x

usew = raw_input('Enter Userid:')
passw = getpass.getpass(prompt='Password:')
print usew
print passw