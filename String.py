import datetime

class String(object):

    def toTimeStamp(self, string, splitter, decimalTime):
        stringArr = string.split(splitter)
        if len(stringArr) is 3:
            (h, m, s) = tuple(stringArr)
            if decimalTime:
                decTime = int(h) * 3600 + int(m) * 60 + int(s)
                return decTime
            time = datetime.time(int(h) + int(m) + int(s))
            return time
        else:
            return None    
