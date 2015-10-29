import shutil
'''
Function	Copies Metadata	Copies Permissions  Can Specify Buffer
--------        --------------- -----------------   ------------------
shutil.copy	No	        Yes	            No
shutil.copyfile	No	        No	            No
shutil.copy2	Yes	        Yes	            No
shutil.copyfileobj  No	        No	            Yes
'''
class File(object):

    def __init__(self):
        self.Name = ""
        self.FileExtension = ""
        self.ServerName = ""
        self.RelativePath = ""
        self.AbsolutePath = ""
        self.Status = ""
        self.LastUpdated = ""
        
    def setName(self, name):
        self.Name = name
    def getName(self):
        return self.Name
    
    def setStatus(self, status):
        self.Status = status
    def getStatus(self):
        return self.Status
    
    def setLastUpdated(self, lastUpdated):
        self.LastUpdated = lastUpdated
    def setLastUpdated(self):
        return self.LastUpdated

    def copyFile(src, dest):
        try:
            shutil.copy(src, dest)
        # eg. src and dest are the same file
        except shutil.Error as e:
            print('Error: %s' % e)
        # eg. source or destination doesn't exist
        except IOError as e:
            print('Error: %s' % e.strerror)

    def copyLargeFile(src, dest, buffer_size=50000):
        '''
        50 KB: 29.539s
        100 KB: 27.423s
        500 KB: 25.245s
        1 MB: 26.261s
        10 MB: 25.521s
        100 MB: 24.886s
        '''
        with open(src, 'rb') as fsrc:
            with open(dest, 'wb') as fdest:
                shutil.copyfileobj(fsrc, fdest, buffer_size)
