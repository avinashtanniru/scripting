#!/bin/bash
if [ $(ps -ef | grep java | awk '{print $2}' | wc -l) == 3 ]; then echo "OK - 3 Process running";exit 0; else echo "CRITICAL - Some procees not started";exit 2; fi
