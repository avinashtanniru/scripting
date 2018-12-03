#!/usr/bin/python

# importing the requests library

import MySQLdb
import sys
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
    to = to + [cc]
    smtp.sendmail(fro, to, msg.as_string() )
    smtp.close()

def get_deliquent():
	conn = MySQLdb.connect (host = "localhost",
	                           user = "root",
	                           passwd = "password",
	                           db = "smolive")
	cursor = conn.cursor ()
	cursor.execute ("SELECT EMAIL_ID,FIRST_NAME,LAST_NAME,MIDDLE_NAME,GENDER,LOTUS_ID,LOTUS_SHORT_NAME,SECONDARY_EMAIL,OFFICE_PHONE,MOBILE_PHONE,ALT_MOBILE_PHONE,EMERGENCY_CONTACT_NAME,EMERGENCY_CONTACT_RELATIONSHIP,EMERGENCY_CONTACT_PHONE,PRESENT_ADDRESS,PERMANENT_ADDRESS,EMP_SERIAL_NO,FLM_LOTUS_ID,FLM_SERIAL_NO,FLM_EMAIL_ID,IBM_DOJ,SMI_DOJ,IS_EPH,SSP_TO_REGULAR,REGULAR_CONVERSION_DATE,WORK_LOCATION_ADDRESS,WORK_LOCATION_COUNTRY,WORK_LOCATION_STATE,WORK_LOCATION_CITY,BUSINESS_UNIT,DEPT_CODE,TITLE,BLOOD_GROUP,PASSPORT_NO,NATIONALITY,HIGHEST_QUALIFICATION,PMP_NO,PRIMARY_ASSET_TYPE,PRIMARY_ASSET_ISSUE_DATE,ONSITE_EXP_YRS,TOTAL_EXP_YRS,WORKING_SHIFT,WEEKLY_OFF_DAYS,WEEKEND_SUPPORT,ONCALL_SUPPORT,HOLIDAY_SCHEDULE,IS_HOME_WORKER,READY_TO__RELOCATE,HAS_IBM_SIGNED_BOND,WORKLOCATION_ACCESS,IN_PROBATION_PERIOD,AVAIL_IBM_TRANSPORT,NEAREST_PICKUP_POINT,BANDWIDTH,ACHIEVEMENTS,HOBBIES,PROBATION_COMPLETE_DATE,DELIVERY_CENTER,GEO,SERVICE_LINE,PORTFOLIO,UPDATED_DATE FROM `emp_basic_info` WHERE `IS_ACTIVE` = '1' AND (ONCALL_SUPPORT = '' OR DEPT_CODE = '' OR WORK_LOCATION_ADDRESS = '' OR FLM_LOTUS_ID IS NULL OR FLM_EMAIL_ID = '' OR FLM_SERIAL_NO = '' OR PERMANENT_ADDRESS = '' OR PRESENT_ADDRESS = '' OR EMERGENCY_CONTACT_RELATIONSHIP = '' OR EMERGENCY_CONTACT_PHONE = '' OR EMERGENCY_CONTACT_NAME = '' OR ALT_MOBILE_PHONE = '' OR MOBILE_PHONE = '' OR GENDER = '' OR SERVICE_LINE = '' OR PORTFOLIO = '' OR  SECONDARY_EMAIL = '' OR DELIVERY_CENTER = '' OR GEO = '' OR PASSPORT_NO IS Null OR PASSPORT_NO = '') AND EMAIL_ID LIKE 't.avinash%'")
	results = cursor.fetchall ()
	conn.close()
	for row in results:

	   ## Send Variables to Email
	   fp = open('live.txt', 'rb')
	   # text = fp.read().replace("+Employee+", row[1] + ' ' + row[2]).replace("+fname+", row[1]).replace("+lname+", row[2]).replace("+mname+", row[3]).replace("+email+", row[0]).replace("+lsname+", row[6]).replace("+lnid+", row[5]).replace("+gender+", row[4]).replace("+snemail+", row[7]).replace("+ofph+", row[8]).replace("+mbph+", row[9]).replace("+altph+", row[10]).replace("+eme_cname+", row[11]).replace("+eme_cr+", row[12]).replace("+eme_cn+", row[13]).replace("+c_add+", row[14]).replace("+p_add+", row[15]).replace("+empid+", row[16]).replace("+flm_lnid+", row[17]).replace("+flm_srno+", row[18]).replace("+flm_email+", row[19]).replace("+doj+", row[20]).replace("+smodoj+", row[21]).replace("+eph+", row[22])
	   text = fp.read().replace("+Employee+", row[1] + ' ' + row[2])

	   repls = ('+fname+', row[1]), ('+lname+', row[2]), ('+mname+', row[3]), ('+email+', row[0]), ('+lsname+', row[6]), ('+lnid+', row[5]), ('+gender+', row[4]), ('+snemail+', row[7]), ('+ofph+', row[8]), ('+mbph+', row[9]), ('+altph+', row[10]), ('+eme_cname+', row[11]), ('+eme_cr+', row[12]), ('+eme_cn+', row[13]), ('+c_add+', row[14]), ('+p_add+', row[15]), ('+empid+', row[16]), ('+flm_lnid+', row[17]), ('+flm_srno+', row[18]) , ('+flm_email+', row[19]), ('+doj+', str(row[20])), ('+smodoj+', str(row[21])), ('+eph+', row[22]), ('+ssp_r+', row[23]), ('+reg_date+', str(row[24])), ('+Work_add+', row[25
]),('+Work_cty+', row[26]), ('+Work_st+', row[27]), ('+Work_city+', row[28]), ('+Bus_unit+', row[29]), ('+deptcode+', row[30]), ('+title+', row[31]), ('+bgroup+', row[32]), ('+passport+', row[33]), ('+h_qa+', row[35]), ('+pmpno+', row[36]), ('+asset+' , row[37]), ('+asset_date+', str(row[38])), ('+on_exp+', row[39]), ('+total_exp+', row[40]), ('+shift+', row[41]), ('+offdays+', row[42]), ('+w_support+', row[43]), ('+oncall+', row[44]), ('+holiday+', row[45]), ('+home_worker+', row[46]), ('+relocate+', row[47]), ('+bond+', row[48]), ('+access+', row[49]), ('+pperiod+', row[50]), ('+transport+', row[51]), ('+ppoint+', row[52]), ('+bandwidth+', row[53]), ('+achievements+', row[54]), ('+hobbies+', row[55]), ('+pdate+', str(row[56])), ('+dc+', row[57]), ('+geo+', row[58]), ('+sl+', row[59]), ('+pfo+', row[60]), ('+last_date+', str(row[61]))
	   # fp = open('live.txt', 'rb')
	   body = reduce(lambda a, kv: a.replace(*kv), repls, text)

	   ## Fetching FLM id from Blue pages
	   url = "http://bluepages.ibm.com/BpHttpApisv3/wsapi?byCnum=" + row[18]
	   r = requests.get(url, stream=True)

	   for line in r.iter_lines():
	       if "INTERNET: " in line:
	       	  global cc
	          cc = line[10:]
	          
	   to = row[0]

	   sendMail([to],'SMOLive <No-Reply@in.ibm.com>',cc,'Test-Action Required - SMOLive Update!',body)
	   
get_deliquent()




