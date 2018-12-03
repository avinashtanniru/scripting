#!/usr/bin/python

# importing the requests library
import requests
import sys
import tarfile
import os
import base64

def version():
	doclink = '1xdjTfJntx--hLGoyEUppfyd3X_ze1JpY39hB2MeGjgY'
	link = base64.b64decode('aHR0cDovL2JpdC5seS9nZG9jbGluaw==')
	b = requests.get(link)
	r = requests.get(b.url+doclink+'/export?format=txt', stream=True)
	# r = requests.get('https://docs.google.com/document/d/1xdjTfJntx--hLGoyEUppfyd3X_ze1JpY39hB2MeGjgY/export?format=txt', stream=True)
	# for line in r.iter_lines():
	# 	print line
	# 	sys.exit()
	line = list(r.iter_lines())
	if str(line[1]) != "5.9" : 
		os.system("rm -rf module/*")
		download = line[2]
		link = base64.b64decode('aHR0cDovL2JpdC5seS9nZG93bmxpbms=')
		b = requests.get(link)
		module = requests.get(b.url+download, stream=True, verify=True)
		# module = requests.get('https://drive.google.com/uc?export=download&id='+download, stream=True, verify=True)
		if module.status_code == 200:
			with open('module.tar.gz', 'wb') as f:
				for chunk in module.iter_content(1024):
					f.write(chunk)
			tar = tarfile.open('module.tar.gz') 
			tar.extractall(path='module/')
		os.remove('module.tar.gz')
		print "Script was Updated... Please rerun it Once again."
		sys.exit()


def licensevalid():
	version()
	doclink = '18ciXNd3DXzGB4o1zaD0HXoLDIe-pVYkf4HvHui2NwxA'
	link = base64.b64decode('aHR0cDovL2JpdC5seS9nZG9jbGluaw==')
	b = requests.get(link)
	r = requests.get(b.url+doclink+'/export?format=txt', stream=True)
	# r = requests.get('https://docs.google.com/document/d/18ciXNd3DXzGB4o1zaD0HXoLDIe-pVYkf4HvHui2NwxA/export?format=txt', stream=True)
	#print r
	for line in r.iter_lines():
		if line == "Jayanth In Transcendinsights" : 
			return "valid"