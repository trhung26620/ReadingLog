import os
from src.config import TomcatLog, ApacheLog, SysLog, ExtendConfig
from src.util import Utils
import gzip
from src.Models import Tomcat, Apache, System
from datetime import datetime
import time
import platform

class Log:
    def displayLog(logArr, logConfig):
        if not logArr:
            Utils.printWarning("\n* Empty log!")
            return None
        try:
            titleStyle = Utils.getStyle(logConfig.titleStyle)
            titleColor = Utils.getColor(logConfig.titleColor)
            title = logConfig.displayTitle
            print(Utils.resetColor() + f"{titleStyle}{titleColor}{title}")
            for log in logArr:
                log.display()
            return None
        except:
            Utils.printError("\n*Something went wrong with displayLog function!")
            return None
    
    def getAllLog(logSetting):
        allLogLines = []
        try:
            folder_path = logSetting.folderPath
            for filename in os.listdir(folder_path):
                isValidFile = False
                for preFileName in logSetting.preFileNameList:
                    if filename.startswith(preFileName):                                
                        isValidFile = True
                        break
                if isValidFile:
                    file_path = os.path.join(folder_path, filename)
                    if os.path.isfile(file_path) and filename.endswith("." + logSetting.zipExtension):
                        with gzip.open(file_path, 'rb') as f:
                            allLogLines += Utils.trimStringArr(Utils.byteArrToStrArr(f.readlines()))
                    elif os.path.isfile(file_path):
                        with open(file_path, 'r') as file:
                            allLogLines += Utils.trimStringArr(file.readlines())
                    else:
                        Utils.printError("\n*Something went wrong with getAllLog function!")
            return Log.logStrArrTologObjArr(allLogLines, logSetting.logType)
        except:
            Utils.printError("\n*Something went wrong with getAllLog function!")
            return []

    def logStrArrTologObjArr(logArr, logType):
        objArr = []
        try:
            for log in logArr:
                if logType == "Tomcat":
                    logObj = Tomcat(log)
                elif logType == "Apache":
                    logObj = Apache(log)
                elif logType == "System":
                    logObj = System(log)
                if logObj.isValidFormat:
                    objArr.append(logObj)
                else:
                    continue
            objArr.sort(key=lambda x: -x.timestamp)
            return objArr
        except:
            Utils.printError("\n*Something went wrong with logStrArrTologObjArr function!")
            return objArr
    
    def filterLogsByString(logObjArr, filterStr):
        filteredObjArr = []
        try:
            for logObj in logObjArr:
                if filterStr in logObj.rawLog:
                    filteredObjArr.append(logObj)
            return filteredObjArr
        except:
            Utils.printError("\n*Something went wrong with filterLogsByString function!")
            return filteredObjArr

    def filterLogsByIp(logObjArr, ip):
        filteredObjArr = []
        try:
            for logObj in logObjArr:
                if ip in logObj.ip_address:
                    filteredObjArr.append(logObj)
            return filteredObjArr
        except:
            Utils.printError("\n*Something went wrong with filterLogsByString function!")
            return filteredObjArr        
        
    def filterLogsByTime(logObjArr, startTime, endTime):
        filteredObjArr = []
        try:
            start_time = datetime.strptime(startTime, ExtendConfig.filterTimeFormat)
            end_time = datetime.strptime(endTime, ExtendConfig.filterTimeFormat)
            for logObj in logObjArr:
                timestamp_datetime = datetime.fromtimestamp(float(logObj.timestamp))
                if start_time <= timestamp_datetime <= end_time:
                    filteredObjArr.append(logObj)
            return filteredObjArr
        except:
            return filteredObjArr
        
    def exportFile(logObjArr, folderPath, logConfig):
        try:
            logLineList = [] 
            slash = ""
            if platform.system() == 'Windows':
                slash = "\\"
            elif platform.system() == 'Linux':
                slash = "/"
            else:
                return None
            fileName = logConfig.preFileNameForExport + '_' + str(int(time.time())) + ".txt"
            filePath = folderPath + slash + fileName
            for logObj in logObjArr:
                logLineList.append(logObj.export())
            if logLineList:
                output = "\n".join(logLineList)
                f = open(filePath, "w")
                f.write(output)
                f.close()
                return filePath
            else:
                return None
        except:
            Utils.printError("\n*Something went wrong with exportFile function!")
            return None