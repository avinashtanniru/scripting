#!/usr/bin/python

# importing the requests library

import MySQLdb
import sys
import requests
import json

def get_ut():
	conn = MySQLdb.connect (host = "localhost",
	                           user = "root",
	                           passwd = "password",
	                           db = "smolive")
	cursor = conn.cursor ()
	cursor.execute ("SELECT UpdateTime FROM test_tvc ORDER BY test_tvc.UpdateTime DESC LIMIT 1")
	results = cursor.fetchall ()
	conn.close()
	for row in results:
	   global UpdatedTime
	   UpdatedTime = row[0]
	   return UpdatedTime
   # print "UpdateTime=%s" %(UpdatedTime)
   # global UpdatedTime
# for row in results:
#       ids = row[0]
#       emails = row[1]
#       date = row[2]
#       hours = row[3]
#       UpdateTime = row[4]
#       # Now print fetched result
#       print "ids=%s,emails=%s,date=%s,hours=%s,UpdateTime=%s" % \
#              (ids, emails, date, hours, UpdateTime )

# defining the api-endpoint 
API_ENDPOINT = "https://localhost/SMILive/KTController/tvcsync"
 
# your API key here
API_KEY = "XXXXXXXXXXXXXXXXX"
 
get_ut()
# UpdatedTime = '2017-05-07 01:00:00'
 
# data to be sent to api
data = {'api_dev_key':API_KEY,
        'api_ut':UpdatedTime,
        'api_paste_format':'python'}
 
# sending post request and saving response as response object
r = requests.post(url = API_ENDPOINT, verify=False, data = data)
 
# extracting response text 
result = r.text
array_r = json.loads(result)

# print array_r

for i in range(len(array_r)):
   ids = array_r[i]['Id']
   email = array_r[i]['email']
   date = array_r[i]['Date']
   hours = array_r[i]['Hours']
   udt = array_r[i]['UpdateTime']

   conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="password",
                  db="smolive")
   x = conn.cursor()

   x.execute("""SELECT * FROM test_tvc WHERE id = """+ids)
   rows_affected = x.rowcount
   # print rows_affected
   if (rows_affected == 1):
      print ids+'row Updating'
      x.execute("UPDATE test_tvc SET email=%s, Date=%s, Hours=%s, UpdateTime=%s WHERE id=%s", (email,date,hours,udt,ids))
      conn.commit()
      
   else:
      print ids+'row Inserting'
      x.execute("""INSERT INTO test_tvc(id, email, Date, Hours, UpdateTime) VALUES (%s,%s,%s,%s,%s)""",(ids,email,date,hours,udt))
      conn.commit()

   conn.close()

