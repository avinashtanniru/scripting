#!/usr/bin/python
###########################################################
#
# This python script is used for mysql database backup
# using mysqldump utility.
#
# Written by : Venkata Avinash
# Website: http://ibm.biz/avinash
# Created date: May 25, 2017
# Last modified: May 25, 2017
# Tested with : Python 2.6.6
# Script Revision: 1.1
#
##########################################################

# Import required python libraries
import os
import time
import datetime

# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databses names one on each line and assignd to DB_NAME variable.

DB_HOST = '9.120.216.53'
DB_USER = 'root'
DB_USER_PASSWORD = '@U[]3Q6V+dSOs'
DB_NAME = 'dbnames.txt'
# DB_NAME = 'db_name'
BACKUP_PATH = '/home/ventanni/Avinash/SMO-KB/dbbackup/'

# Getting current datetime to create seprate backup folder like "12012013-071334".
DATETIME = time.strftime('%d%m%Y-%H%M%S')

TODAYBACKUPPATH = BACKUP_PATH + DATETIME

# Checking if backup folder already exists or not. If not exists will create it.
print "creating backup folder"
if not os.path.exists(TODAYBACKUPPATH):
    os.makedirs(TODAYBACKUPPATH)

# Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
print "checking for databases names file."
if os.path.exists(DB_NAME):
    file1 = open(DB_NAME)
    multi = 1
    print "Databases file found..."
    print "Starting backup of all dbs listed in file " + DB_NAME
else:
    print "Databases file not found..."
    print "Starting backup of database " + DB_NAME
    multi = 0

# Starting actual database backup process.
if multi:
   in_file = open(DB_NAME,"r")
   flength = len(in_file.readlines())
   in_file.close()
   p = 1
   dbfile = open(DB_NAME,"r")

   while p <= flength:
       db = dbfile.readline()   # reading database name from file
       db = db[:-1]         # deletes extra line
       dumpcmd = "mysqldump -h " + DB_HOST +" -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + "| gzip" +" > " + TODAYBACKUPPATH + "/" + db + ".sql" + ".gz"
       os.system(dumpcmd)
       p = p + 1
   dbfile.close()
else:
   db = DB_NAME
   dumpcmd = "mysqldump -h " + DB_HOST +" -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + "| gzip" +" > " + TODAYBACKUPPATH + "/" + db + ".sql" + ".gz"
   os.system(dumpcmd)

print "Backup script completed"
print "Your backups has been created in '" + TODAYBACKUPPATH + "' directory"
