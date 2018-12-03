#!/usr/bin/python

# importing the requests library
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

#Last Friday
lastFriday = datetime.date.today()
oneday = datetime.timedelta(days=1)

while lastFriday.weekday() != calendar.FRIDAY:
    lastFriday -= oneday
    
# print lastFriday.strftime("%D")
API_DT = lastFriday.strftime("%Y-%m-%d")
print(API_DT)

# defining the api-endpoint 
API_ENDPOINT = "http://localhost/SMILive-1481564750087/KTController/mailtvc"
 
# your API key here
API_KEY = "XXXXXXXXXXXXXXXXX"
 
 
# data to be sent to api
data = {'api_dev_key':API_KEY,
        'api_dt':API_DT,
        'api_paste_format':'python'}
 
# sending post request and saving response as response object
r = requests.post(url = API_ENDPOINT, data = data)
 
# extracting response text 
result = r.text
array_r = json.loads(result)



# Mail Code
def sendMail(to, fro, cc, subject, text, files=[],server="localhost"):
    assert type(to)==list
    assert type(files)==list


    msg = MIMEMultipart('alternative')
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg['Cc'] = cc

    msg.attach( MIMEText(text) )

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

for i in range(len(array_r)):
   print(array_r[i]['email'])
   text = """Hello """+array_r[i]['FIRST_NAME']+""" """+array_r[i]['LAST_NAME']+""".

We are Pleased to inform that your TVC not yet synced till """+API_DT+""". Only """+array_r[i]['Hours']+""" is synced.
The Last Updated is """+array_r[i]['UpdateTime']+"""
   
*** Do Not Reply To This Email.

Regards,
SMOLive
"""
    
   sendMail([array_r[i]['email']],'SMOLive <No-Reply@in.ibm.com>',array_r[i]['FLM_EMAIL_ID'],'SMO TVC Update!',text)

print(len(array_r))

print("The pastebin URL is:%s"%result)