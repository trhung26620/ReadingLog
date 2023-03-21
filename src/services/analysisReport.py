from src.util import Utils
from src.config import TomcatLog, ApacheLog, SysLog, MenuConfig, ExtendConfig, analyzeModeConfig
import copy
from src.services.log import Log
from src.services.renderReport import Render
from src.Models import Tomcat, Apache


class Analyzer:
    def __init__(self):
        self.startTime = None
        self.endTime = None
        self.tomcatLogObjList = []
        self.apacheLogObjList = []
        self.systemLogObjList = []
        self.nmapLog = []
        self.metasploitLog = []
        self.nmapReqIP = []
        self.metasploitReqIP = []
        self.numberReqIP = {}
        self.detectedAttackType = []

    def getDateArrange(self):
        try:
            self.startTime = input(Utils.getStyle("BRIGHT") + Utils.getColor("YELLOW") +
                                   f"+ Start time (E.g:{ExtendConfig.formatExampleForFilterTime}): ")
            self.endTime = input(Utils.getStyle("BRIGHT") + Utils.getColor("YELLOW") +
                                 f"+ End time (E.g:{ExtendConfig.formatExampleForFilterTime}): ")
        except:
            Utils.printError(
                "\n*Something went wrong with getDateArrange function!")

    def fetchLogObjLists(self):
        try:
            self.tomcatLogObjList = Log.filterLogsByTime(
                Log.getAllLog(TomcatLog), self.startTime, self.endTime)
            self.apacheLogObjList = Log.filterLogsByTime(
                Log.getAllLog(ApacheLog), self.startTime, self.endTime)
            self.systemLogObjList = Log.filterLogsByTime(
                Log.getAllLog(SysLog), self.startTime, self.endTime)
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
            # Log.displayLog(self.metasploitLog, analyzeModeConfig)
        except:
            Utils.printError(
                "\n*Something went wrong with fetchMetasploitRequest function!")

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

    def reportPrinter(self):
        self.getDateArrange()
        self.fetchLogObjLists()
        self.fetchNmapRequest()
        self.fetchMetasploitRequest()
        self.fetchNumberRequestById()
        if self.nmapReqIP:
            self.detectedAttackType.append('Nmap scanning')
        if self.metasploitReqIP:
            self.detectedAttackType.append('Metasploit attack')
        self.detectedAttackType.append('DoS')
        render = Render(self.startTime, self.endTime, self.detectedAttackType, self.distinguishTomcatAndApache(
            self.nmapLog), self.distinguishTomcatAndApache(self.metasploitLog))
        render.outputReport()
        print('Exported File: ' + analyzeModeConfig.reportFolder)
