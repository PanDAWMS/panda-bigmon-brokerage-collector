#!/bin/bash
source /home/ookey/.bash_profile

cd /home/ookey/workspace/PandaBrokerageMonitor
/usr/bin/python parse_analy_brokerage_log.py >> /tmp/PBMon.log 2>&1
