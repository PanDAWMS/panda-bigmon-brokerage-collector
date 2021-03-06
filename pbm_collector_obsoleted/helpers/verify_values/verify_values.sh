#!/bin/bash
# run on adcmon.cern.ch

MYPYTHON=/usr/bin/python2.5

### adcmon
WORKDIR=/data/jschovan/PandaBrokerageMon/verify_values
#PUBDIR=/var/www/html/PandaBrokerageMon/verify_values
PUBDIR=/data/adcmon-preproduction/PandaBrokerageMon/verify_values
#PUBDIR=/data/adcmon-preproduction/PandaBrokerageMon/verify_values.test

### lxplus
#WORKDIR=/afs/cern.ch/user/j/jschovan/scratch0/PandaBrokerageMon/verify_values
#PUBDIR=${WORKDIR}/pub

LOGDIR=${WORKDIR}/logs
DATESTRING=$(date +%F.%H%M%S)
INDEX=${PUBDIR}/index.html

mkdir -p ${LOGDIR} ${PUBDIR}

cd ${WORKDIR}

echo "Running at ${DATESTRING}."

# get data from DB
/usr/bin/time ${MYPYTHON} verifyDB.py ${WORKDIR} 2>&1 | tee ${LOGDIR}/log.verifyDB.${DATESTRING}

# process data
/usr/bin/time ${MYPYTHON} verify_values.py ${WORKDIR} 2>&1 | tee ${LOGDIR}/log.verify_values.${DATESTRING}

# pack data
cd ${WORKDIR}
rm DAILYLOGV2.py.bz2 LASTUPDATEDV2.py.bz2

bzip2 DAILYLOGV2.py
#bzip2 DAILYLOG.py
#bzip2 LASTUPDATED.py
bzip2 LASTUPDATEDV2.py
#bzip2 MONTHLYLOG.py


# publish data
cp ${WORKDIR}/DAILYLOGV2.py.bz2 ${PUBDIR}/DAILYLOGV2.py.bz2
cp ${LOGDIR}/log.verify_values.${DATESTRING} ${PUBDIR}/log.verify_values.txt

# bzip files
bzip2 ${LOGDIR}/log.verifyDB.${DATESTRING} ${LOGDIR}/log.verify_values.${DATESTRING}

# create index
cd ${PUBDIR}
echo -n >${INDEX}
for file in $(ls . | grep -v "index.html"); 
do
    lsl=$(ls -l $file)
    html="<div>$(echo $lsl | sed -e "s#$file#<a href=\"./$file\">$file</a>#g" | awk '{printf $5 " " $6 " " $7 " " $8 " " $9 " " $10;}')</div>"
    echo $html >> ${INDEX}
done


