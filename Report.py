import datetime

class Report(object):

    def __init__(self):
        self.Name = ""
        self.Status = "SUCCESS"
        self.InitialTimeStamp = datetime.time(0,0,0)
        self.GeneratedTimeStamp = datetime.time(0,0,0)
        self.sortByTime = 0

    def __repr__(self):
        return '{}: {}\nInitial Time: {}\nEnd Time: {}\n'.format(self.__class__.__name__,
                                  self.Name,
                                  self.InitialTimeStamp,
                                  self.GeneratedTimeStamp)
    def __cmp__(self, other):
        if hasattr(other, 'sortByTime'):
            return self.sortByTime.__cmp__(other.sortByTime)
        
    def setName(self, name):
        self.Name = name
    def getName(self):
        return self.Name.upper()
    
    def setStatus(self, status):
        self.Status = status
    def getStatus(self):
        return self.Status.upper()

    def setInitialTimeStamp(self, initTime):
        self.InitialTimeStamp = initTime
    def getInitialTimeStamp(self):
        return self.InitialTimeStamp
    
    def setGeneratedTimeStamp(self, genTime):
        self.GeneratedTimeStamp = genTime
    def getGeneratedTimeStamp(self):
        return self.GeneratedTimeStamp

    def setSortByTime(self, sortTime):
        self.sortByTime = sortTime
    def getSortByTime(self):
        return self.sortByTime
