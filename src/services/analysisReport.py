from src.util import Utils
from src.config import TomcatLog, ApacheLog, SysLog, ExtendConfig, analyzeModeConfig, DosDetectionConfig
from src.services.log import Log
from src.services.renderReport import Render
from src.Models import Tomcat, Apache
import datetime
import copy

class Analyzer:
    def __init__(self):
        self.startTime = None
        self.endTime = None
        self.tomcatLogObjList = []
        self.apacheLogObjList = []
        self.systemLogObjList = []
        self.nmapLog = []
        self.metasploitLog = []
        self.dirbLog = []
        self.dirbIP = []
        self.nmapReqIP = []
        self.metasploitReqIP = []
        self.numberReqIP = {}
        self.detectedAttackType = []
        self.tomcatDosAttackResult = {}
        self.apacheDosAttackResult = {}

    def getDateArrange(self):
        try:
            self.startTime = input(Utils.getStyle("BRIGHT") + Utils.getColor("YELLOW") +
                                   f"+ Start time (E.g:{ExtendConfig.formatExampleForFilterTime}): ")
            self.endTime = input(Utils.getStyle("BRIGHT") + Utils.getColor("YELLOW") +
                                 f"+ End time (E.g:{ExtendConfig.formatExampleForFilterTime}): ")
            if not self.endTime:
               self.endTime = datetime.datetime.now().strftime(TomcatLog.dateInputFormat)
        except:
            Utils.printError(
                "\n*Something went wrong with getDateArrange function!")

    def fetchLogObjLists(self, logType='ALL'):
        try:
            if logType=='ALL':
                self.tomcatLogObjList = Log.filterLogsByTime(
                    Log.getAllLog(TomcatLog), self.startTime, self.endTime)
                self.apacheLogObjList = Log.filterLogsByTime(
                    Log.getAllLog(ApacheLog), self.startTime, self.endTime)
            elif logType=='Tomcat':
                self.tomcatLogObjList = Log.filterLogsByTime(
                    Log.getAllLog(TomcatLog), self.startTime, self.endTime)
            elif logType=='Apache':
                self.apacheLogObjList = Log.filterLogsByTime(
                    Log.getAllLog(ApacheLog), self.startTime, self.endTime)      
            # self.systemLogObjList = Log.filterLogsByTime(
            #     Log.getAllLog(SysLog), self.startTime, self.endTime)
            # print(Log.getIpAddressListFromObjList(self.tomcatLogObjList))
        except:
            Utils.printError(
                "\n*Something went wrong with fetchLogObjLists function!")

    def fetchNmapRequest(self):
        try:
            self.nmapLog += Log.filterLogsByString(
                self.tomcatLogObjList, analyzeModeConfig.nmapDetectionSignature)
            self.nmapLog += Log.filterLogsByString(
                self.apacheLogObjList, analyzeModeConfig.nmapDetectionSignature)
            self.nmapReqIP = Log.getIpAddressListFromObjList(self.nmapLog)
        except:
            Utils.printError(
                "\n*Something went wrong with fetchNmapRequest function!")

    def fetchMetasploitRequest(self):
        try:
            self.metasploitLog += Log.filterLogsByString(
                self.tomcatLogObjList, analyzeModeConfig.metasploitDetectionSignature)
            self.metasploitLog += Log.filterLogsByString(
                self.apacheLogObjList, analyzeModeConfig.metasploitDetectionSignature)
            self.metasploitReqIP = Log.getIpAddressListFromObjList(
                self.metasploitLog)
        except:
            Utils.printError(
                "\n*Something went wrong with fetchMetasploitRequest function!")

    def fetchDirbRequest(self):
        try:
            self.dirbLog += Log.filterLogsByStatusCode(
                self.tomcatLogObjList, analyzeModeConfig.dirbDetectionSignature)
            self.dirbLog += Log.filterLogsByStatusCode(
                self.apacheLogObjList, analyzeModeConfig.dirbDetectionSignature)
            self.dirbIP = Log.getIpAddressListFromObjList(
                self.dirbLog)
        except:
            Utils.printError(
                "\n*Something went wrong with fetchDirbRequest function!")
            
    def fetchNumberRequestById(self):
        try:
            self.numberReqIP = Log.countRequestById(
                self.tomcatLogObjList + self.apacheLogObjList)
        except:
            Utils.printError(
                "\n*Something went wrong with fetchNumberRequestById function!")

    def distinguishTomcatAndApache(self, logArr):
        result = {
            'logDataTomcat': '',
            'logDataApache': ''
        }
        if logArr:
            tomcatLogTemp = []
            apacheLogTemp = []
            for log in logArr:
                if isinstance(log, Tomcat):
                    tomcatLogTemp.append(log.rawLog)
                elif isinstance(log, Apache):
                    apacheLogTemp.append(log.rawLog)
                else:
                    pass
            result['logDataTomcat'] = '\n'.join(tomcatLogTemp)
            result['logDataApache'] = '\n'.join(apacheLogTemp)
            return result
        else:
            return result

    def detectDosAttack(self, requestObjList):
        REQUESTS_THRESHOLD = DosDetectionConfig.minimumRequest
        INTERVAL_MINUTES = DosDetectionConfig.duration
        ip_requests = {}
        dosAttackResult = {}
        sortedRequestObjList = sorted(requestObjList, key=lambda x: x.timestamp)
        for request in sortedRequestObjList:
            ip_address = request.ip_address
            timestamp = Utils.timestampToObj(request.timestamp)
            if ip_address not in ip_requests:
                ip_requests[ip_address] = []
            # first_requests[ip_address] = timestamp
                dosAttackResult[ip_address] = {"count": 0, "timestamp": None}
            # Add the request to the IP address's list of requests
            ip_requests[ip_address].append(timestamp)

            # Remove requests that are older than the 2-minute interval
            if dosAttackResult[ip_address]["count"] < REQUESTS_THRESHOLD:
                oldest_allowed = timestamp - \
                    datetime.timedelta(minutes=INTERVAL_MINUTES)
                ip_requests[ip_address] = [
                    req for req in ip_requests[ip_address] if req >= oldest_allowed]
            else:
                dosAttackResult[ip_address]["count"] += 1
            
            if len(ip_requests[ip_address]) == REQUESTS_THRESHOLD and dosAttackResult[ip_address]["count"] == 0:
                dosAttackResult[ip_address]["count"] = REQUESTS_THRESHOLD
                dosAttackResult[ip_address]["timestamp"] = ip_requests[ip_address][0].strftime("%d/%b/%Y:%H:%M:%S")
        return {k: v for k, v in dosAttackResult.items() if v['count'] != 0}  
    
    def getDoSDataForRender(self): 
        result = {}
        self.tomcatDosAttackResult = self.detectDosAttack(self.tomcatLogObjList)
        self.apacheDosAttackResult = self.detectDosAttack(self.apacheLogObjList)
        data = {
            "tomcat": self.tomcatDosAttackResult,
            "apache": self.apacheDosAttackResult
        }
        for key, value in data.items():
            result[key] = []
            for ip, stats in value.items():
                result[key].append({"ip": ip, "count": stats["count"], "timestamp": stats["timestamp"]})
        return result
        
    def reportPrinter(self):
        self.getDateArrange()
        self.fetchLogObjLists()
        self.fetchNmapRequest()
        self.fetchMetasploitRequest()
        self.fetchDirbRequest()
        self.fetchNumberRequestById()
        if self.nmapReqIP:
            self.detectedAttackType.append('Nmap scanning')
        if self.metasploitReqIP:
            self.detectedAttackType.append('Metasploit attack')
        if self.dirbIP:
            self.detectedAttackType.append('Dirb brute force')
        dosData = self.getDoSDataForRender()
        if dosData["tomcat"] or dosData["apache"]:
            self.detectedAttackType.append('DoS')
        pathLog = {
            'tomcatPath': TomcatLog.folderPath,
            'apachePath': ApacheLog.folderPath,
        }
        render = Render(self.startTime, self.endTime, self.detectedAttackType, self.distinguishTomcatAndApache(
            self.nmapLog), self.distinguishTomcatAndApache(self.metasploitLog), self.distinguishTomcatAndApache(self.dirbLog),dosData, pathLog)
        render.outputReport()
        print('Exported File: ' + analyzeModeConfig.reportFolder)
        
    def tomcatReportPrinter(self):
        self.getDateArrange()
        self.fetchLogObjLists(TomcatLog.logType)
        self.fetchNmapRequest()
        self.fetchMetasploitRequest()
        self.fetchDirbRequest()
        self.fetchNumberRequestById()
        if self.nmapReqIP:
            self.detectedAttackType.append('Nmap scanning')
        if self.metasploitReqIP:
            self.detectedAttackType.append('Metasploit attack')
        if self.dirbIP:
            self.detectedAttackType.append('Dirb brute force')
        dosData = self.getDoSDataForRender()
        if dosData["tomcat"] or dosData["apache"]:
            self.detectedAttackType.append('DoS')
        pathLog = {
            'tomcatPath': TomcatLog.folderPath,
        }
        render = Render(self.startTime, self.endTime, self.detectedAttackType, self.distinguishTomcatAndApache(
            self.nmapLog), self.distinguishTomcatAndApache(self.metasploitLog), self.distinguishTomcatAndApache(self.dirbLog),dosData, pathLog)
        render.outputReport()
        print('Exported File: ' + analyzeModeConfig.reportFolder)
        
    def apacheReportPrinter(self):
        self.getDateArrange()
        self.fetchLogObjLists(ApacheLog.logType)
        self.fetchNmapRequest()
        self.fetchMetasploitRequest()
        self.fetchDirbRequest()
        self.fetchNumberRequestById()
        if self.nmapReqIP:
            self.detectedAttackType.append('Nmap scanning')
        if self.metasploitReqIP:
            self.detectedAttackType.append('Metasploit attack')
        if self.dirbIP:
            self.detectedAttackType.append('Dirb brute force')
        dosData = self.getDoSDataForRender()
        if dosData["tomcat"] or dosData["apache"]:
            self.detectedAttackType.append('DoS')
        pathLog = {
            'apachePath': ApacheLog.folderPath,
        }
        render = Render(self.startTime, self.endTime, self.detectedAttackType, self.distinguishTomcatAndApache(
            self.nmapLog), self.distinguishTomcatAndApache(self.metasploitLog), self.distinguishTomcatAndApache(self.dirbLog),dosData, pathLog)
        render.outputReport()
        print('Exported File: ' + analyzeModeConfig.reportFolder)
