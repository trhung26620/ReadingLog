from colorama import Fore, Style
from datetime import datetime
import os
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL


class Utils():
    def resetColor():
        return Style.RESET_ALL + Fore.RESET
        
    def getColor(color):
        mapping = {
            "BLACK": Fore.BLACK,
            "RED": Fore.RED,
            "GREEN": Fore.GREEN,
            "YELLOW": Fore.YELLOW,
            "BLUE": Fore.BLUE,
            "MAGENTA": Fore.MAGENTA,
            "CYAN": Fore.CYAN,
            "WHITE": Fore.WHITE,
            "RESET": Fore.RESET,
        }
        return mapping[color]

    def getStyle(style):
        mapping = {
            "DIM": Style.DIM,
            "NORMAL": Style.NORMAL,
            "BRIGHT": Style.BRIGHT,
            "RESET_ALL": Style.RESET_ALL,
        }
        return mapping[style]

    def printWarning(text):
        print(f"{Style.NORMAL}{Fore.YELLOW}{text}")

    def printError(text):
        print(f"{Style.NORMAL}{Fore.RED}{text}")
        
    def byteArrToStrArr(byteArray):
        strArr = []
        try:
            for text in byteArray:
                if text and text != '\n':
                    strArr.append(text.decode())
            return strArr
        except:
            Utils.printError("\n* Something went wrong with byteArrToStrArr function!")
            return []
        
    def trimStringArr(arrText):
        if arrText:
            newArr = []
            try:
                for text in arrText:
                    if text:
                        data = text.strip().replace('\x00', '')
                        if data:
                            newArr.append(data)
                return newArr
            except:
                Utils.printError("\n* Something went wrong with trimStringArr function!")
                return []
        else:
            return []
        
    def timestampToDate(timestamp, logConfig):
        try:
            date_time = datetime.fromtimestamp(timestamp)
            str_date_time = date_time.strftime(logConfig.dateOutputFormat)
            return str_date_time      
        except:
            Utils.printError("\n* Something went wrong with timestampToDate function!")
            return None

    
    def dateToTimestamp(dateData, logConfig):
        try:
            dt_format = datetime.strptime(dateData, logConfig.dateInputFormat)
            timestamp = dt_format.timestamp()
            return timestamp
        except:
            Utils.printError("\n* Something went wrong with dateToTimestamp function!")
            return None

    def validate_time_input(input_time, timePattern):
        try:
            datetime.strptime(input_time, timePattern)
            return True
        except ValueError:
            return False
        
    def checkExistFolder(folder_path):
        try:
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                return True
            else:
                return False
        except:
            Utils.printError("\n* Something went wrong with checkExistFolder function!")
            return False
    