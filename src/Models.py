import re
from src.config import SysLog, TomcatLog, ApacheLog
from src.util import Utils
from datetime import datetime

class Tomcat:
    def __init__(self, rawLog):
        self.rawLog = rawLog
        self.isValidFormat = False
        self.ip_address = None
        self.remote_user = None
        self.authenticated_user = None
        self.timestamp = None
        self.request_line = None    
        self.status_code = None   
        self.response_size = None   
        self.analyzeRawLog()
        
    def analyzeRawLog(self):
        rawLog = self.rawLog.strip()
        regex = '^(\S+) (\S+) (\S+) \[(.*?) .+\] "(.*?)" (\d+) (\d+|-)$'
        matches = re.match(regex, rawLog)
        if matches:
            self.ip_address = matches.group(1)
            self.remote_user = matches.group(2)
            self.authenticated_user = matches.group(3)
            self.timestamp = Utils.dateToTimestamp(matches.group(4), TomcatLog)
            self.request_line = matches.group(5)
            self.status_code = matches.group(6)
            self.response_size = matches.group(7)
            self.isValidFormat = True
        else:
            # print(rawLog)
            print("Log line did not match the expected format.")
        
    def display(self):
        time = Utils.timestampToDate(float(self.timestamp), TomcatLog)
        print(f"{self.ip_address} {self.remote_user} {self.authenticated_user} {time} {self.request_line} {self.status_code} {self.response_size}")
    
    def export(self):
        time = Utils.timestampToDate(float(self.timestamp), TomcatLog)
        data = f"{self.ip_address} {self.remote_user} {self.authenticated_user} {time} {self.request_line} {self.status_code} {self.response_size}"
        return data
    
class Apache:
    def __init__(self, rawLog):
        self.rawLog = rawLog
        self.isValidFormat = False
        self.ip_address = None
        self.remote_user = None
        self.authenticated_user = None
        self.timestamp = None
        self.request_line = None  
        self.status_code = None
        self.response_size = None
        self.referer = None
        self.user_agent = None
        self.analyzeRawLog()
        
    def analyzeRawLog(self):
        rawLog = self.rawLog.strip()
        regex = '^(\S+) (\S+) (\S+) \[(.+) .+\] "(.+)" (\d+) (\d+) "(.+)" "(.+)"$'
        matches = re.match(regex, rawLog)
        if matches:
            self.ip_address = matches.group(1)
            self.remote_user = matches.group(2)
            self.authenticated_user = matches.group(3)
            self.timestamp = Utils.dateToTimestamp(matches.group(4), ApacheLog)
            self.request_line = matches.group(5)
            self.status_code = matches.group(6)
            self.response_size = matches.group(7)
            self.referer = matches.group(8)
            self.user_agent = matches.group(9)
            self.isValidFormat = True
        else:
            print("Log line did not match the expected format.")
            
    def display(self):
        time = Utils.timestampToDate(float(self.timestamp), ApacheLog)
        print(f"{self.ip_address} {self.remote_user} {self.authenticated_user} {time} {self.request_line} {self.status_code} {self.response_size} {self.referer} {self.user_agent}")

    def export(self):
        time = Utils.timestampToDate(float(self.timestamp), TomcatLog)
        data = f"{self.ip_address} {self.remote_user} {self.authenticated_user} {time} {self.request_line} {self.status_code} {self.response_size} {self.referer} {self.user_agent}"
        return data
    
class System:
    def __init__(self, rawLog):
        self.rawLog = rawLog
        self.isValidFormat = False
        self.timestamp = None
        self.host = SysLog.serverIP
        self.type = SysLog.displayType
        self.message = None
        self.process = None
        self.hostname = None
        self.analyzeRawLog()

    def analyzeRawLog(self):
        rawLog = self.rawLog.strip()
        regex = '^([A-Za-z]{3}\s+\d{1,2} \d{2}:\d{2}:\d{2}) (\S+) (\S+): (.*?)$'
        matches = re.match(regex, rawLog)
        if matches:
            current_year = datetime.now().year
            tempString = matches.group(1).strip() + " " + str(current_year)
            fullDateString = datetime.strptime(tempString, "%b %d %H:%M:%S %Y").strftime("%b %d %Y %H:%M:%S")
            self.timestamp = Utils.dateToTimestamp(fullDateString, SysLog)
            self.message = matches.group(4)
            self.process = matches.group(3)
            self.hostname = matches.group(2)
            self.isValidFormat = True
        else:
            print("Log line did not match the expected format.")
            
    def display(self):
        time = Utils.timestampToDate(float(self.timestamp), SysLog)
        print(f"{time} {self.message} {self.process} {self.hostname}")
        
    def export(self):
        time = Utils.timestampToDate(float(self.timestamp), TomcatLog)
        data = f"{time} {self.message} {self.process} {self.hostname}"
        return data