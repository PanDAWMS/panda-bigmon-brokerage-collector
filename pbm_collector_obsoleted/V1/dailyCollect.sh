#!/bin/bash
source /home/ookey/.bash_profile

cd /home/ookey/workspace/PandaBrokerageMonitor
/usr/bin/python parse_analy_brokerage_log.py >> logs/PBMon.log 2>&1
/usr/bin/python my_logfile.py > /dev/null 2>&1
