#!/usr/bin/python

# importing the requests library
from __future__ import division # We require Python 2.6 or later
import requests
import time
import MySQLdb
import sys
import csv


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
      OFF_CELL = lines[3][8:-1]
      CELL = lines[11][10:-1]
      NAME = lines[12][6:-1]
      DEPT = lines[13][6:-1]
      DIV = lines[14][5:-1]
      EMPTYPE = lines[15][9:-1]
      # if (EMPTYPE == 'P' or EMPTYPE == 'A' or EMPTYPE == 'J' or EMPTYPE == 'O' or EMPTYPE == 'S'):
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
      MGR = lines[16][5:-1]
      if MGR == 'Y':
         MGR = 'Yes'
      elif MGR == 'N':
         MGR = 'No'
      JOBRESPONSIB = lines[18][14:-1]
      NOTESID = lines[21][9:-1]
      NOTESID = NOTESID.replace("CN=", "")
      NOTESID = NOTESID.replace("OU=", "")
      NOTESID = NOTESID.replace("O=", "")
      INTERNET = lines[22][10:-1]
      USERID = lines[23][8:-1]
      NODE = lines[24][6:-1]
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
      C = lines[32][3:-1]
      COUNTRY = lines[33][9:-1]
      HRCOMPANYCODE = lines[51][15:-1]
      HREMPLOYEETYPE = lines[55][16:-1]
      HRFIRSTNAME = lines[57][13:-1]
      HRLASTNAME = lines[59][12:-1]
      MNUM = lines[68][6:-1]
      UPDATED_DATE = time.strftime('%Y-%m-%d %H:%M:%S')
   
      conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="password",
                  db="bluepages")
      x = conn.cursor()

      x.execute("""SELECT * FROM emp_basic_info WHERE EMP_SERIAL_NO = '"""+EMPID+"""'""")
      rows_affected = x.rowcount
      # print rows_affected
      if (rows_affected == 1):
         print EMPID+' Employee is Updating From Blupages'
         if (EMPTYPE == 'SSP'):
            L_NAME = NAME.rsplit(',', 1)[0].strip()
            F_NAME = NAME.rsplit(',', 1)[1].rsplit('*', 2)[0].strip()
            x.execute("UPDATE emp_basic_info SET EMAIL_ID=%s, FIRST_NAME=%s, LAST_NAME=%s, LOTUS_ID=%s, LOTUS_SHORT_NAME=%s, FLM_SERIAL_NO=%s, IS_ACTIVE=%s, WORK_LOCATION_COUNTRY=%s, DEPT_CODE=%s, EMPLOYEE_TYPE=%s, TITLE=%s, IS_MANAGER=%s, DELIVERY_CENTER=%s, BP_DATE=%s WHERE EMP_SERIAL_NO=%s", (INTERNET,F_NAME,L_NAME,NOTESID,USERID,MNUM,1,COUNTRY,DEPT,EMPTYPE,JOBRESPONSIB,MGR,WORKLOC,UPDATED_DATE,EMPID))
            conn.commit()
         else :
            # x.execute("UPDATE emp_basic_info SET EMAIL_ID=%s, FIRST_NAME=%s, LAST_NAME=%s, LOTUS_ID=%s, LOTUS_SHORT_NAME=%s, OFFICE_PHONE=%s, MOBILE_PHONE=%s, FLM_SERIAL_NO=%s, IS_ACTIVE=%s, WORK_LOCATION_COUNTRY=%s, DEPT_CODE=%s, EMPLOYEE_TYPE=%s, TITLE=%s, IS_MANAGER=%s, UPDATED_DATE=%s WHERE EMP_SERIAL_NO=%s", (INTERNET,HRFIRSTNAME,HRLASTNAME,NOTESID,USERID,OFF_CELL,CELL,MNUM,1,COUNTRY,DEPT,EMPTYPE,JOBRESPONSIB,MGR,UPDATED_DATE,EMPID))
            x.execute("UPDATE emp_basic_info SET EMAIL_ID=%s, FIRST_NAME=%s, LAST_NAME=%s, LOTUS_ID=%s, LOTUS_SHORT_NAME=%s, FLM_SERIAL_NO=%s, IS_ACTIVE=%s, WORK_LOCATION_COUNTRY=%s, DEPT_CODE=%s, EMPLOYEE_TYPE=%s, TITLE=%s, IS_MANAGER=%s, DELIVERY_CENTER=%s, BP_DATE=%s WHERE EMP_SERIAL_NO=%s", (INTERNET,HRFIRSTNAME,HRLASTNAME,NOTESID,USERID,MNUM,1,COUNTRY,DEPT,EMPTYPE,JOBRESPONSIB,MGR,WORKLOC,UPDATED_DATE,EMPID))
            conn.commit()
      elif (EMPTYPE == "N"): 
         print EMPID+' Not Added in Database as it is Functional ID'  
      else:
         print EMPID+' Employee is Added From Blupages'
         try:
            if (EMPTYPE == 'SSP') or (EMPTYPE == 'Vendor'):
               L_NAME = NAME.rsplit(',', 1)[0].strip()
               F_NAME = NAME.rsplit(',', 1)[1].rsplit('*', 2)[0].strip()
               x.execute("""INSERT INTO emp_basic_info(EMAIL_ID, FIRST_NAME, LAST_NAME, LOTUS_ID, LOTUS_SHORT_NAME, OFFICE_PHONE, MOBILE_PHONE, EMP_SERIAL_NO, FLM_SERIAL_NO, IS_ACTIVE, WORK_LOCATION_COUNTRY, DEPT_CODE, EMPLOYEE_TYPE, TITLE, IS_MANAGER, DELIVERY_CENTER, CREATION_DATE, BP_DATE) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(INTERNET,F_NAME,L_NAME,NOTESID,USERID,OFF_CELL,CELL,EMPID,MNUM,1,COUNTRY,DEPT,EMPTYPE,JOBRESPONSIB,MGR,WORKLOC,UPDATED_DATE,UPDATED_DATE))
               conn.commit()
            else:   
               x.execute("""INSERT INTO emp_basic_info(EMAIL_ID, FIRST_NAME, LAST_NAME, LOTUS_ID, LOTUS_SHORT_NAME, OFFICE_PHONE, MOBILE_PHONE, EMP_SERIAL_NO, FLM_SERIAL_NO, IS_ACTIVE, WORK_LOCATION_COUNTRY, DEPT_CODE, EMPLOYEE_TYPE, TITLE, IS_MANAGER, DELIVERY_CENTER, CREATION_DATE, BP_DATE) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(INTERNET,HRFIRSTNAME,HRLASTNAME,NOTESID,USERID,OFF_CELL,CELL,EMPID,MNUM,1,COUNTRY,DEPT,EMPTYPE,JOBRESPONSIB,MGR,WORKLOC,UPDATED_DATE,UPDATED_DATE))
               conn.commit()
         except MySQLdb.IntegrityError as err:
            print( emp_no + " - Error: {}".format(err))
            with open("errors.txt", "a") as myfile:
               myfile.write(emp_no + " - Error: {}".format(err) + '\n')

      x.execute("UPDATE emp_basic_info SET FLM_LOTUS_ID=%s, FLM_EMAIL_ID=%s, BP_DATE=%s WHERE FLM_SERIAL_NO=%s", (NOTESID,INTERNET,UPDATED_DATE,EMPID))
      conn.commit()
      conn.close()

   else:
      print 'You Have Entered Invalid EmpId....'
      # exit()

def mgr_details ( flm_id ):
   reload(sys)
   sys.setdefaultencoding('utf-8')
   # flm_id = raw_input("Please Enter A Emp ID To which chain has to Updated along with 744 :")
   response = requests.get("http://bluepages.ibm.com/BpHttpApisv3/wsapi?directReportsOf=" + flm_id)
   data = response.text
   # print json_data
   # mgr = timestr = time.strftime("%Y_%m_%d_%H_%M_%S")
   # mgr = 'MGR_'+mgr+'.txt'
   text_file = open("MGR.txt", "w")
   text_file.write(data)
   text_file.close()
   # my_list = []

   with open('MGR.txt', 'r') as f:
      if len(f.readlines()) > 1:
         with open('MGR.txt', 'r') as f:
            for line in f:
               if "CNUM: " in line:
               	  ids = line.startswith( 'CNUM: ' )
                  if ids:
                     my_list.append(line[6:-1])
                     print line[6:-1]+' IS A Manager'
                     ### Writing All Employes to CSV
                     with open('EmpList.csv', "a") as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(line[6:-1])
                  else:
                     print 'This is Not Employee ' + line 
                  
      else:
         print list+' IS Not A Manager'
         # my_list.append(list)
         # exit()

   # print my_list
   # print "There are %d Managers Under Palas" % len(my_list) 

# #/*******
flm_id = raw_input("Please Enter A Emp ID To which chain has to Updated along with 744 :")
emp_details(emp_no = flm_id)

my_list = []

mgr_details( flm_id = flm_id )
# print my_list
for list in my_list:
   # print "Checking if Manager" + list
   mgr_details(list)
   # print len(my_list)
   # print "\n"


# print my_list
print len(my_list)
print "\n"

##Updating Emp in Database
count = 1
for list in my_list:
   emp_details(list)
   print 'completed ' + str(round((count/len(my_list))*100,2)) + '%'
   count += 1

# #/**********


# ##### Reading All Employes from CSV
# with open('EmpList.csv', 'r') as f:
#   reader = csv.reader(f)
#   my_list = list(reader)

# print my_list
# print len(my_list)
# count = 1
# for list in my_list:
#    my_lst_str = ''.join(map(str, list))
#    emp_details(my_lst_str)
#    print 'completed ' + str(round((count/len(my_list))*100,2)) + '%'
#    count += 1
###########END
