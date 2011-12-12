import cx_Oracle

### Production
#TABLE_DAILYLOG="dailyLogV2"
#TABLE_LASTUPDATED="LastUpdatedV2"

### Development/tests
TABLE_DAILYLOG="dailyLogV2T1"
TABLE_LASTUPDATED="lastUpdatedV2T1"


class dailyDBV2(object):
    
    _db = None
    _connect = 'PandaBrokerageMonitor_ookey/PandaBrokerageMonitor2@devdb11'
    
    def __init__(self):
        global TABLE_DAILYLOG, TABLE_LASTUPDATED
        # self._db = cx_Oracle.connect('PandaBrokerageMonitor_ookey/PandaBrokerageMonitor2@devdb11')
        self._db = cx_Oracle.connect(self._connect)
        
    def get_max_id(self):
        cursor = self._db.cursor()
        sql = "SELECT MAX(dailyLogId) as maxID from %s" % (TABLE_DAILYLOG)
        cursor.execute(sql)
        maxID = cursor.fetchone()[0]
        cursor.close()
        return maxID
    
    def get_logdate_by_id(self, id):
        cursor = self._db.cursor()
        sql = "SELECT logDate from %s where dailyLogId=%d" % (TABLE_DAILYLOG, id)
        cursor.execute(sql)
        rs = cursor.fetchone()
        if rs is not None:
            logDate = rs[0]
        else:
            logDate = None;
        cursor.close()
        return logDate
    
    def get_last_updated_time(self):
        cursor = self._db.cursor()
        sql = "SELECT LastUpdatedTime from %s ORDER By LastUpdatedTime DESC" % (TABLE_LASTUPDATED)
        cursor.execute(sql)
        rs = cursor.fetchone()
        if rs is not None:
            lastUpdatedTime = rs[0]
        else:
            lastUpdatedTime = None;
        cursor.close()
        return lastUpdatedTime
    
    def set_last_updated_time(self, lastUpdated):
        cursor = self._db.cursor()
        sql = "UPDATE %s SET LastUpdatedTime='%s'" % (TABLE_LASTUPDATED, lastUpdated)
        cursor.execute(sql)
        self._db.commit()
        cursor.close()
        return True
    
    def first_last_updated_time(self):
        cursor = self._db.cursor()
        sql = "INSERT INTO %s (LastUpdatedTime) VALUES ('2011-10-10 12:00')" % (TABLE_LASTUPDATED)
        cursor.execute(sql)
        self._db.commit()
        cursor.close()
        return True
    
    def is_exist_item(self, logDate, jobSet, category, site, dnUser):
        cursor = self._db.cursor()
        sql = "SELECT dailyLogId FROM %s WHERE logDate='%s' AND jobSet='%s' AND category='%s' AND site='%s' AND dnUser='%s'"%(TABLE_DAILYLOG, logDate,jobSet,category,site,dnUser)
        cursor.execute(sql)
        rs = cursor.fetchone()
        if rs is not None:
            dailyLogId = rs[0]
        else:
            dailyLogId = None
        cursor.close()
        return dailyLogId
        
    def add_logs(self,logs):
        cursor = self._db.cursor()
        sql = "INSERT INTO %s ( dailyLogId, logDate, jobSet, category, site, cloud, dnUser, jobdefCount, jobCount, country) " + \
                  "VALUES ( :1, :2, :3, :4, :5, :6, :7, :8, :9, :10 )" % (TABLE_DAILYLOG)
        cursor.executemany(sql, logs)
        self._db.commit()
        cursor.close()
        return True
        
    def increase_logs_count(self,logIds):
        cursor = self._db.cursor()
        sql = "UPDATE %s SET jobdefCount = jobdefCount + 1, jobCount = jobCount + :1 WHERE dailyLogId = :2 " % (TABLE_DAILYLOG)
        cursor.executemany(sql, logIds)
        self._db.commit()
        cursor.close()
        return True
        
    def increase_buf_count(self,logs):
        cursor = self._db.cursor()
        sql = "UPDATE %s SET jobdefCount = jobdefCount + 1, jobCount = jobCount + :1 WHERE logDate = :2 AND jobSet=:3 AND category = :4 AND site = :5 AND dnUser = :6 " % (TABLE_DAILYLOG)
        cursor.executemany(sql, logs)
        self._db.commit()
        cursor.close()
        return True
    
    def query(self,sql):
        cursor = self._db.cursor()
        cursor.execute(sql)
        rs = cursor.fetchall()
        cursor.close()
        return rs
