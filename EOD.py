#EOD.py

import re, datetime
from String import *
from Report import *
from File import *


class EOD(object):
    
    def __init__(self, filename, export_file, keywords):
        self.DateOfGenerate = datetime.time(0,0,0)
        self.eod_file = filename
        self.export_file = export_file 
        self.keywords = keywords
        self.reportFailList = []
        self.reportSuccessList = []
    
    def loadFile(self):
        try:
            with open(self.eod_file, 'r') as f:
                self.lines = f.readlines()
            f.close()
        except:
            return False
        return True
    
    def filteredFileContent(self):
        try:            
            linesList = [l.strip("\n") for l in self.lines]            
            date = linesList[0].split(':')[1] # get date=                    
            filteredLineList = [reportItem[30:] for reportItem in linesList if all(keyw in reportItem for keyw in self.keywords[:3]) or all(keyw in reportItem for keyw in self.keywords[3:5]) ]
            filteredLineList.append(date)
            #print filteredLineList
        except:
            return None
        return filteredLineList    
        
    def toTimeStamp(self, strTime, isDecimal):
        timeArr = strTime.split(':')        
        if len(timeArr) is 3:
            (h, m, s) = int(timeArr[0]), int(timeArr[1]), int(timeArr[2])
            if isDecimal:
                time = int(h) * 3600 + int(m) * 60 + int(s)
            else:
                time = datetime.time(h, m, s)            
            return time
        else:
            pass

    def timeDiff(self, startDate, initTime, genTime):
        '''
        There is and issue with time.
        If current time 12:21:28 and next time 01:35:37 the difference is 13h:14m:09s
        '''
        date = startDate.split('/')        
        dummydate = datetime.date(int(date[2]),int(date[1]),int(date[0]))#2015,01,01
        t1 = datetime.datetime.combine(dummydate,initTime)
        t2 = datetime.datetime.combine(dummydate,genTime)        
        if '-' in str(t2 - t1):
            dummydate += datetime.timedelta(days=1)
            t2 = datetime.datetime.combine(dummydate,genTime)      

        stringTime = str(t2 - t1)
        timeArr = stringTime.split(':')  
        if len(timeArr) is 3:
            (h, m, s) = stringTime.split(':')                        
            return (h, m, s)
        else:
            return 0
    
    def extactBeautify(self, current_length, m=0, r=0):
        if m == 0:            
            current_length = 64 - current_length            
            
        if current_length < 4:
                r = current_length
                
        while current_length > 4:                                
            current_length = current_length - 4  
            m = m + 1
            if current_length < 4:                
                r = current_length                
                break
        return (m, r)    

    def matchDateTime(self, timeStr):
        m = re.search(r'(\d+):(\d{2}):(\d{2})',timeStr)
        if m:
            return m.group()
        return datetime.time(0,0,0)
    
    def extractReportDetails(self, current_item, next_item):
        tempReport = {}
        try:
            name = re.search(r'(^[A-Z]*[a-z]*)(\d*)(\w*)', current_item).group()
            initTime = self.matchDateTime(current_item)
            genTime = self.matchDateTime(next_item)
            m = re.search(r'sukses', next_item)
            if m:
                status = m.group()
            m = re.search(r'gabim', next_item)
            if m:                
                status = m.group()
            
            tempReport = {
                'name': name,
                'initTime': initTime,
                'genTime': genTime,
                'status': status
            }
        except:
            # There are time that report starts to generate and is cutted in half
            None

        return tempReport
            
    def extract(self):
        try:
            print self.export_file
            target = open(self.export_file, 'w')            
            target.truncate()
            target.write("Report name\t\t\t\t\t\t\t\t\t\t\t\tInitial time   Generate time \t   Duration(H:M:S)\tStatus\n\n")
            reportList = self.filteredFileContent()
            #get report generate starting date                        
            reportDate = reportList[-1]            
            del reportList[-1]
            ##            
            tempReport = {}
            for index in range(len(reportList)):
                if index % 2 is 0: #get the starting-ending points for each generated report
                    #[::-1] used to reverse list
                    current_item = reportList[index] #starting point                    
                    next_item = reportList[index+1] #ending point                    
                    tempReport = self.extractReportDetails(current_item, next_item)
                    #print tempReport
                    reportItem = Report()                                                            
                    reportItem.setName(tempReport['name'])                    
                    reportItem.setStatus(tempReport['status']) 
                    reportItem.setInitialTimeStamp(self.toTimeStamp(tempReport['initTime'], isDecimal=False))                    
                    reportItem.setGeneratedTimeStamp(self.toTimeStamp(tempReport['genTime'], isDecimal=False))                    
                    m, r = self.extactBeautify(len(reportItem.getName())) # m => multiplier, r => reminder(user to calculate whitespace between columns)                    
                    target.write(reportItem.getName())
                    target.write("\t" * m)
                    target.write("" * r) 
                    target.write(str(reportItem.getInitialTimeStamp()))
                    target.write("\t")
                    target.write(str(reportItem.getGeneratedTimeStamp()))
                    target.write("\t\t\t\t")                    
                    h, m, s =  self.timeDiff(reportDate, reportItem.getInitialTimeStamp(), reportItem.getGeneratedTimeStamp())
                    target.write('{}h:{}m:{}s'.format(h,m,s))
                    target.write("\t")
                    target.write(reportItem.getStatus())
                    timeInSec = int(h) * 3600 + int(m) * 60 + int(s)
                    if timeInSec > 1800: # more than 30 min
                        target.write("\t")
                        target.write("DELAYS(more than 30 min)")                        
                    
                    target.write("\n")
            target.close()
        except:
            None
        
    def findFailReport(self):
        try:                    
            reportList = self.filterReportList()
            for reportListItem in reportList:
                reportItem = Report()
                reportItem.setName(reportListItem[0])
                reportItem.setStatus(reportListItem[3])
                reportItem.setGeneratedTimeStamp(self.getFormatedTime(reportListItem[4]))
                reportItem.setSortByTime(self.getDecimalTime(reportListItem[4]))
                self.reportFailList.append(reportItem)            
        except:
            return True
    
    def displayFailReportList(self):
        _reportFailList = sorted(self.reportFailList)
        
        for reportFailItem in _reportFailList:
            print reportFailItem

        print len(_reportFailList)
        #errorsLog = [e if any(tup in self.keywords in e for e in self.contentDictArr]
        #check for keywords in the list with condition that all have to match        
    
