class TomcatLog:
    logType = "Tomcat"
    # Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Style: DIM, NORMAL, BRIGHT, RESET_ALL
    folderPath = r'F:\Work\Development\Freelance\ReadingLog\temp\tomcatLog'
    preFileNameList = ["localhost_access_log."]
    zipExtension = "gz"
    color = "RESET"
    style = "RESET_ALL"
    displayTitle = "\n* Display logs:"
    titleColor = "MAGENTA"
    titleStyle = "BRIGHT"
    dateOutputFormat = "%d/%b/%Y:%H:%M:%S"
    dateInputFormat = "%d/%b/%Y:%H:%M:%S"
    preFileNameForExport = "TomcatLog"
    
class ApacheLog:
    logType = "Apache"
    # Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Style: DIM, NORMAL, BRIGHT, RESET_ALL
    folderPath = r'F:\Work\Development\Freelance\ReadingLog\temp\apacheLog'
    # folderPath = r'/mnt/f/Work/Development/Freelance/ReadingLog/temp/apacheLog'
    preFileNameList = ["access.log"]
    zipExtension = "gz"
    color = "RESET"
    style = "RESET_ALL"
    displayTitle = "\n* Display logs:"
    titleColor = "MAGENTA"
    titleStyle = "BRIGHT"
    dateOutputFormat = "%d/%b/%Y:%H:%M:%S"
    dateInputFormat = "%d/%b/%Y:%H:%M:%S"
    preFileNameForExport = "ApacheLog"
    
class SysLog:
    logType = "System"
    # Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Style: DIM, NORMAL, BRIGHT, RESET_ALL
    folderPath = r'F:\Work\Development\Freelance\ReadingLog\temp\sysLog'
    preFileNameList = ["syslog", "auth.log"]
    zipExtension = "gz"
    color = "RESET"
    style = "RESET_ALL"
    displayTitle = "\n* Display logs:"
    titleColor = "MAGENTA"
    titleStyle = "BRIGHT"
    serverIP = "192.168.200.10"
    displayType = "syslog"
    dateOutputFormat = "%d/%b/%Y:%H:%M:%S"
    dateInputFormat = "%b %d %Y %H:%M:%S"
    preFileNameForExport = "SystemLog"
    
class Banner:
    # Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Style: DIM, NORMAL, BRIGHT, RESET_ALL
    color = "YELLOW"
    styte = "BRIGHT"
    bannerText = """
        

    ███████╗██╗      ██████╗  ██████╗ 
    ██╔════╝██║     ██╔═══██╗██╔════╝ 
    █████╗  ██║     ██║   ██║██║  ███╗
    ██╔══╝  ██║     ██║   ██║██║   ██║
    ██║     ███████╗╚██████╔╝╚██████╔╝
    ╚═╝     ╚══════╝ ╚═════╝  ╚═════╝ 
                                    
     
     
    Flog is a digital forensics platform and other digital forensics tools.
    It uses investigate what happened on a computer through viewing log files. 
    You can even use it to identify web attacks.
    
    Flog v1.1.0
    Coded by Hoài Tân, Đức Dương, Gia Thuận, Nhất Lợi, Duy Luân  
 
    """

class ExtendConfig:
    filterTimeFormat= "%d/%b/%Y:%H:%M:%S"
    formatExampleForFilterTime = "18/Feb/2023:22:41:22"
    
class MenuConfig:
    keyMainOptions = ['1', '2', '3', '4']
    keySubOptions = ['1', '2', '3', '4', '5', '6', '7']
    keySubOptionsForSysLog = ['1', '2', '3', '4', '5', '6']
    optionRequestColor = "BLUE"
    optionRequestStyle = "NORMAL"
    optionRequest = """Your option: """
    menuColor = "BLUE"
    menuStyte = "BRIGHT"
    mainMenu = """
- Enter the type of log you want to analyze:
  1. Analyze Tomcat Log 
  2. Analyze Apache Log
  3. Analyze System Log
  4. Exit    
"""

    subMenu = """
+ Enter an action:
  1. Filter by date
  2. Filter by IP
  3. Filter by string
  4. Reset filter 
  5. Display
  6. Export file
  7. Exit
"""

    subMenuForSysLog = """
+ Enter an action:
  1. Filter by date
  2. Filter by string
  3. Reset filter 
  4. Display
  5. Export file
  6. Exit
"""
    dateFilterMenu = """
Please enter with format: dd-MM-yyyy-hh-mm-ss
1. From Date
2. To Date
"""
