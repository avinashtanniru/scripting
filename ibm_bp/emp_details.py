#!/usr/bin/python

# importing the requests library

import requests
import time
import MySQLdb
import sys
import csv
import requests
import json
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os
import datetime, calendar

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWD = "@U[]3Q6V+dSOs"
DB_NAME = "smolive"

def emp_details( emp_no ):
   reload(sys)
   sys.setdefaultencoding('utf-8')
   response = requests.get("http://bluepages.ibm.com/BpHttpApisv3/wsapi?byCnum=" + emp_no)
   data = response.text
   text_file = open("Emp.txt", "w")
   text_file.write(data)
   text_file.close()
   f=open('Emp.txt')
   if len(f.readlines()) > 1:
       f=open('Emp.txt')
       lines=f.readlines()
       EMPID = lines[0][6:-1]
       DEPT = lines[13][6:-1]
       DIV = lines[14][5:-1]
       EMPTYPE = lines[15][9:-1]
       if (EMPTYPE == 'P'):
           EMPTYPE = 'Regular'
       elif EMPTYPE == 'C':
           EMPTYPE = 'SSP'
       elif EMPTYPE == 'A':
           EMPTYPE = 'Alternate Work Arrangement'
       elif EMPTYPE == 'L':
           EMPTYPE = 'Leave of Absence'
       elif EMPTYPE == 'O':
           EMPTYPE = 'Assignee-Out'
       elif EMPTYPE == 'V':
           EMPTYPE = 'Vendor'
       INTERNET = lines[22][10:-1]
       USERID = lines[23][8:-1]
       NOTESID = lines[21][9:-1].replace("CN=", "").replace("OU=", "").replace("O=", "")
       BLDG = lines[27][6:-1]
       FLOOR = lines[29][7:-1]
       WORKLOC = lines[30][9:-1]
       if (WORKLOC == 'C4P' or WORKLOC == 'E5T' or WORKLOC == 'J9D'):
       		WORKLOC = 'BANGALORE'
       elif (WORKLOC == 'E4B'):
       		WORKLOC = 'CHENNAI'
       elif (WORKLOC == 'H7J' or WORKLOC == 'C5P' or WORKLOC == 'H7J'):
       		WORKLOC == 'GURGAON'
       elif (WORKLOC == 'D3E' or WORKLOC == 'D4T' or WORKLOC == 'E7A' or WORKLOC == 'I0O' or WORKLOC == 'K0D'):
       		WORKLOC = 'HYDERABAD'
       elif (WORKLOC == 'K0T' or WORKLOC == 'F0G' or WORKLOC == 'H0I' or WORKLOC == 'E5U'):
       		WORKLOC = 'NOIDA'
       elif (WORKLOC == 'C4N' or WORKLOC == 'D3Y' or WORKLOC == 'E7F'):
       		WORKLOC = 'PUNE'
       elif (WORKLOC == 'D3J'):
       		WORKLOC = 'KOLKATA'
       elif (WORKLOC == 'F0H'):
       		WORKLOC = 'MUMBAI'
       MNUM = lines[68][6:-1]
       COUNTRY = lines[33][9:-1]
       MGR = lines[16][5:-1]
       if MGR == 'Y':
           MGR = 'Yes'
       elif MGR == 'N':
           MGR = 'No'
       try:
       	mresponse = requests.get("http://bluepages.ibm.com/BpHttpApisv3/wsapi?byCnum=" + MNUM)
       except requests.exceptions.RequestException as e:  # This is the correct syntax
       	  print(e + "Error - empid: " + emp_no + "Manager ID: " + MNUM)
    	  sys.exit(1)
       mdata = mresponse.text
       mtext_file = open("Mgr.txt", "w")
       mtext_file.write(mdata)
       mtext_file.close()
       f=open('Mgr.txt')
       if len(f.readlines()) > 1:
       	f=open('Mgr.txt')
       	lines=f.readlines()
       	MINTERNET = lines[22][10:-1]
       	MUSERID = lines[23][8:-1]
       	MNOTESID = lines[21][9:-1].replace("CN=", "").replace("OU=", "").replace("O=", "")
       	BP_DATE = time.strftime('%Y-%m-%d %H:%M:%S')

       	conn = MySQLdb.connect(host= DB_HOST,
                  user=DB_USER,
                  passwd=DB_PASSWD,
                  db=DB_NAME)
       	x = conn.cursor()

       	x.execute("""SELECT * FROM emp_basic_info WHERE EMP_SERIAL_NO = '"""+EMPID+"""'""")
       	rows_affected = x.rowcount
       	if (rows_affected == 1):
          x.execute("UPDATE emp_basic_info SET EMAIL_ID=%s, LOTUS_ID=%s, LOTUS_SHORT_NAME=%s, FLM_LOTUS_ID=%s, FLM_SERIAL_NO=%s, FLM_EMAIL_ID=%s, IS_ACTIVE=%s, WORK_LOCATION_COUNTRY=%s, DEPT_CODE=%s, EMPLOYEE_TYPE=%s, IS_MANAGER=%s, DELIVERY_CENTER=%s, BP_DATE=%s WHERE EMP_SERIAL_NO=%s", (INTERNET,NOTESID,USERID,MNOTESID,MNUM,MINTERNET,1,COUNTRY,DEPT,EMPTYPE,MGR,WORKLOC,BP_DATE,EMPID))
          conn.commit()
          conn.close()
          print "User Updated in DB, - ," + emp_no
       	else:
          print "User Not Found in DB, - ," + emp_no
       else:
       	print "Check Manually, - ," + emp_no   
   else:
   	  BP_DATE = time.strftime('%Y-%m-%d %H:%M:%S')
   	  conn = MySQLdb.connect(host= DB_HOST,
                  user=DB_USER,
                  passwd=DB_PASSWD,
                  db=DB_NAME)
   	  x=conn.cursor()
   	  x.execute("UPDATE emp_basic_info SET IS_ACTIVE=%s, BP_DATE=%s WHERE EMP_SERIAL_NO=%s", (0,BP_DATE,emp_no))
   	  conn.commit()
   	  conn.close()
   	  print "User Made Inactive in DB, - ," + emp_no

def sendMail(to, fro, cc, subject, text, files=[],server="localhost"):
    assert type(to)==list
    assert type(files)==list


    msg = MIMEMultipart('alternative')
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg['Cc'] = cc

    msg.attach( MIMEText(text, 'html') )

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(fro, to, msg.as_string() )
    smtp.close()
#### Collecting all Employees Data and 
conn = MySQLdb.connect(host= DB_HOST,
                  user=DB_USER,
                  passwd=DB_PASSWD,
                  db=DB_NAME)
x = conn.cursor()
x.execute("""SELECT EMP_SERIAL_NO  FROM `emp_basic_info` WHERE IS_ACTIVE='1'""")
data=list(x.fetchall())
print "Script Successfully Started at -" + time.strftime('%Y-%m-%d %H:%M:%S')
print "Need to be Updated : " + str(len(data))
# print(str(data[0])[2:-3])	
for x in range(0,len(data)):
   # print "Going to update, - ," + str(data[x])[2:-3]
   emp_details(str(data[x])[2:-3])
   # emp_details('03322N744')
print "Script Successfully Completed at -" + time.strftime('%Y-%m-%d %H:%M:%S')
# # Started
# timestamp=time.strftime('%Y_%m_%d_%H_%M_%S')
# path='/home/ventanni/bpsync'
# os.system('mv '+path+'.log '+path+'_'+timestamp+'.log')
# # os.rename(path+'.log', path+'_'+timestamp+'.log')
# time.sleep(5)
# fp = open('/home/ventanni/Desktop/python/bpmail.txt', 'rb')
# # text = fp.read().replace("+ name +", name)
# text = fp.read()
# attachment = path+'_'+str(timestamp)+'.log'
# sendMail(['t.avinash@in.ibm.com'],'SMOLive <No-Reply@in.ibm.com>','t.avinash@in.ibm.com','SMOLive BluePages Sync Update!',text,[attachment])
# print "Mail Sent Successfully at -" + time.strftime('%Y-%m-%d %H:%M:%S')
# # end