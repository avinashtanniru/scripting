#!/usr/bin/python

# importing the requests library
import sys, getopt

def main(argv):
   cfile = ''
   Hfile = ''
   try:
      opts, args = getopt.getopt(argv,"hc:H:",["cfile=","Hfile="])
   except getopt.GetoptError:
      print 'test.py -c <configfile> -H <Hostfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -c <configfile> -H <Hostfile>'
         sys.exit()
      elif opt in ("-c", "--cfile"):
         cfile = arg
      elif opt in ("-H", "--Hfile"):
         Hfile = arg
   print 'Config file is "', cfile
   print 'Hostnames file is "', Hfile

if __name__ == "__main__":
   main(sys.argv[1:])