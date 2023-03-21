from src.services.menu import Menu
from src.util import Utils
from src.services.log import Log
from src.config import TomcatLog, ApacheLog, SysLog, MenuConfig, ExtendConfig, analyzeModeConfig
import copy
from src.services.analysisReport import Analyzer


class Controller:
    def __init__(self):
        self.logConfig = None
        self.option = ""
        self.supOption = ""
        self.logObjList = []
        self.logObjForDisplay = []

    def process(self):
        Menu.displayBanner()
        self.option = Menu.proccessMenu(
            MenuConfig.mainMenu, MenuConfig.keyMainOptions)
        if self.option == "1":
            self.logConfig = TomcatLog
        elif self.option == "2":
            self.logConfig = ApacheLog
        elif self.option == "3":
            self.logConfig = SysLog
        elif self.option == "4":
            analyzer = Analyzer()
            analyzer.reportPrinter()
        else:
            exit()
        if self.option != "4":
            self.logObjList = Log.getAllLog(self.logConfig)
            self.logObjForDisplay = copy.deepcopy(self.logObjList)
            if self.logConfig.logType == "System":
                self.processSubMenuForSysLog()
            else:
                self.processSubMenu()

    def processSubMenu(self):
        option = Menu.proccessMenu(
            MenuConfig.subMenu, MenuConfig.keySubOptions)
        if option == "1":
            startTime = input(Utils.getStyle("BRIGHT") + Utils.getColor("YELLOW") +
                              f"+ Start time (E.g:{ExtendConfig.formatExampleForFilterTime}): ")
            endTime = input(Utils.getStyle("BRIGHT") + Utils.getColor("YELLOW") +
                            f"+ End time (E.g:{ExtendConfig.formatExampleForFilterTime}): ")
            self.logObjForDisplay = copy.deepcopy(
                Log.filterLogsByTime(self.logObjForDisplay, startTime, endTime))
            self.processSubMenu()
        elif option == "2":
            ipForFilter = input(Utils.getStyle("BRIGHT") +
                                Utils.getColor("YELLOW") + "+ IP: ")
            self.logObjForDisplay = copy.deepcopy(
                Log.filterLogsByIp(self.logObjForDisplay, ipForFilter))
            self.processSubMenu()
        elif option == "3":
            strForFilter = input(Utils.getStyle(
                "BRIGHT") + Utils.getColor("YELLOW") + "+ Filter: ")
            self.logObjForDisplay = copy.deepcopy(
                Log.filterLogsByString(self.logObjForDisplay, strForFilter))
            self.processSubMenu()
        elif option == "4":
            self.logObjForDisplay = copy.deepcopy(self.logObjList)
            self.processSubMenu()
        elif option == "5":
            Log.displayLog(self.logObjForDisplay, self.logConfig)
            self.processSubMenu()
        elif option == "6":
            saveFolder = input(Utils.getStyle("BRIGHT") +
                               Utils.getColor("YELLOW") + "+ Folder path: ")
            if Utils.checkExistFolder(saveFolder):
                filePath = Log.exportFile(
                    self.logObjForDisplay, saveFolder, self.logConfig)
                if filePath:
                    Utils.printWarning("\n* File exported at: " + filePath)
                else:
                    Utils.printError("\n* Export file error!")
                self.processSubMenu()
            else:
                Utils.printError("\n* Invalid folder path")
                self.processSubMenu()
        else:
            exit()

    def processSubMenuForSysLog(self):
        option = Menu.proccessMenu(
            MenuConfig.subMenuForSysLog, MenuConfig.keySubOptionsForSysLog)
        if option == "1":
            startTime = input(Utils.getStyle("BRIGHT") + Utils.getColor("YELLOW") +
                              f"+ Start time (E.g:{ExtendConfig.formatExampleForFilterTime}): ")
            endTime = input(Utils.getStyle("BRIGHT") + Utils.getColor("YELLOW") +
                            f"+ End time (E.g:{ExtendConfig.formatExampleForFilterTime}): ")
            self.logObjForDisplay = copy.deepcopy(
                Log.filterLogsByTime(self.logObjForDisplay, startTime, endTime))
            self.processSubMenuForSysLog()
        elif option == "2":
            strForFilter = input(Utils.getStyle(
                "BRIGHT") + Utils.getColor("YELLOW") + "+ Filter: ")
            self.logObjForDisplay = copy.deepcopy(
                Log.filterLogsByString(self.logObjForDisplay, strForFilter))
            self.processSubMenuForSysLog()
        elif option == "3":
            self.logObjForDisplay = copy.deepcopy(self.logObjList)
            self.processSubMenuForSysLog()
        elif option == "4":
            Log.displayLog(self.logObjForDisplay, self.logConfig)
            self.processSubMenuForSysLog()
        elif option == "5":
            saveFolder = input(Utils.getStyle("BRIGHT") +
                               Utils.getColor("YELLOW") + "+ Folder path: ")
            if Utils.checkExistFolder(saveFolder):
                filePath = Log.exportFile(
                    self.logObjForDisplay, saveFolder, self.logConfig)
                if filePath:
                    Utils.printWarning("\n* File exported at: " + filePath)
                else:
                    Utils.printError("\n* Export file error!")
                self.processSubMenu()
            else:
                Utils.printError("\n* Invalid folder path")
                self.processSubMenu()
        else:
            exit()
