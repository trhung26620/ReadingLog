# import argparse
import os
import glob
from colorama import Fore, Back, Style
from src.config import Banner, MenuConfig
import colorama
from src.util import Utils


class Menu:
    # def __init__(self):
    # self.args = None

    def displayBanner():
        colorama.init(autoreset=True)
        style = Utils.getStyle(Banner.styte)
        color = Utils.getColor(Banner.color)
        print(f"{style}{color}{Banner.bannerText}")

    def displayMenu(menuData):
        colorama.init(autoreset=True)
        style = Utils.getStyle(MenuConfig.menuStyte)
        color = Utils.getColor(MenuConfig.menuColor)
        print(f"{style}{color}{menuData}")
        optionRequestColor = Utils.getColor(MenuConfig.optionRequestColor)
        optionRequestStyle = Utils.getStyle(MenuConfig.optionRequestStyle)
        option = input(
            f"{optionRequestStyle}{optionRequestColor}{MenuConfig.optionRequest}")
        return option

    def proccessMenu(menuData, optionList):
        while True:
            option = Menu.displayMenu(menuData)
            if option in optionList:
                return option
            else:
                Utils.printWarning('\n* Invalid option, please try again!')