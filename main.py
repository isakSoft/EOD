import os, datetime
from EOD import *

def main():
    SERVERS = ('\EOD_LIVE1', '\EOD_LIVE2', '\EOD_BACK2')
    KEYWORDS = ('Gjenerimi', 'perfundoi', 'gabime', 'sukses', 'hapur','skedarin')
    EXPORT_KEYWORDS = ('Duke', 'hapur','skedarin', 'Gjenerimi', 'perfundoi', 'me')

    home_dir = os.path.expanduser("~")

    today = datetime.datetime.now().strftime('%d_%m_%Y')

    for server in SERVERS:
        server_fs = home_dir + '\EOD' + server
        os.chdir(server_fs) #change to server(e.g. EOD_LIVE1) dir        
        if not os.path.isdir(today):
            os.mkdir(today) #create dir as 23_10_2015            
        server_fs_today = server_fs + '\\' + today
        server_fs_dir_list = os.listdir(today)    
        
        for file in server_fs_dir_list:        
            if file.endswith(".txt"):
                EXPORT_FILE2 = file[:21] + 'EXPORTED.txt'
                os.chdir(server_fs_today)
                my_export_file = os.path.join(server_fs_today, EXPORT_FILE2)
                #print file,'\n',my_export_file
                eod = EOD(file, my_export_file, EXPORT_KEYWORDS)            
                if eod.loadFile():                        
                    eod.extract()                        


if __name__ == '__main__':
    main()
