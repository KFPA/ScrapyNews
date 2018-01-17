import logging
import os
import datetime

class logger:
    def __init__(self):
        starttime = datetime.datetime.now()
        self.logfile =  os.getcwd() + '\\log\\' + str(str(starttime).split()[0]) + '.log'
    def getLogfile(self):
        return self.logfile

