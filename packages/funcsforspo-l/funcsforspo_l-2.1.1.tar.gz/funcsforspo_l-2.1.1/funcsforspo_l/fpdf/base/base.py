from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager
from funcsforspo_l.fpython.functions_for_py import *
from funcsforspo_l.fselenium.functions_selenium import *
from funcsforspo_l.fregex.functions_re import *
from webdriver_manager.core.utils import ChromeType
import pandas as pd
import json
import base64
import os

# -- GLOBAL -- #

# -- GLOBAL -- #


class Bot:    
    def __init__(self, headless, download_files) -> None:
        # --- CHROME OPTIONS --- #
        self.options = ChromeOptions()
        
        try:
            self._DOWNLOAD_DIR =  cria_dir_no_dir_de_trabalho_atual(dir=download_files, print_value=False, criar_diretorio=True)
            limpa_diretorio(self._DOWNLOAD_DIR)
            
            self.SETTINGS_SAVE_AS_PDF = {
                        "recentDestinations": [
                            {
                                "id": "Save as PDF",
                                "origin": "local",
                                "account": ""
                            }
                        ],
                        "selectedDestinationId": "Save as PDF",
                        "version": 2,
                    }


            self.PROFILE = {'printing.print_preview_sticky_settings.appState': json.dumps(self.SETTINGS_SAVE_AS_PDF),
                    "savefile.default_directory":  f"{self._DOWNLOAD_DIR}",
                    "download.default_directory":  f"{self._DOWNLOAD_DIR}",
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": False}            
            self.options.add_experimental_option('prefs', self.PROFILE)
        except:
            pass
        if headless == True:
            self.options.add_argument('--headless')
            
        self.options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        self.options.add_argument('--kiosk-printing')

        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--disable-gpu')
        self.options.add_argument(f"--user-agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3251.0 Safari/537.36")
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--allow-running-insecure-content")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-setuid-sandbox")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-webgl")
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_argument('--disable-software-rasterizer')
        self.options.add_argument('--no-proxy-server')
        self.options.add_argument("--proxy-server='direct://'")
        self.options.add_argument('--proxy-bypass-list=*')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--block-new-web-contents')
        self.options.add_argument('--incognito')
        self.options.add_argument('–disable-notifications')
        self.options.add_argument('--disable-logging')
        self.options.add_argument("--window-size=1920,1080")
        
        self.service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        
        # create DRIVER
        try:
            self.DRIVER = Chrome(service=self.service, options=self.options)
        except SessionNotCreatedException:
            self.service = Service(ChromeDriverManager(cache_valid_range=0).install())
            self.DRIVER = Chrome(service=self.service, options=self.options)


        self.WDW3 = WebDriverWait(self.DRIVER, timeout=3)
        self.WDW5 = WebDriverWait(self.DRIVER, timeout=5)
        self.WDW7 = WebDriverWait(self.DRIVER, timeout=7)
        self.WDW10 = WebDriverWait(self.DRIVER, timeout=10)
        self.WDW30 = WebDriverWait(self.DRIVER, timeout=30)
        self.WDW60 = WebDriverWait(self.DRIVER, timeout=60)
        self.WDW120 = WebDriverWait(self.DRIVER, timeout=120)
        self.WDW180 = WebDriverWait(self.DRIVER, timeout=180)
        self.WDW = self.WDW7

        """
        O código adiciona suporte para o download automático de arquivos em um diretório especificado no Chrome com headless usando o Selenium WebDriver.
        """
        self.DRIVER.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': self._DOWNLOAD_DIR}}
        command_result = self.DRIVER.execute("send_command", params)

        self.DRIVER.maximize_window()
        return self.DRIVER

    def quit_web(self):
        self.DRIVER.quit()
        
        
class BotDownload:    
    def __init__(self, headless, download_files) -> None:
        # --- CHROME OPTIONS --- #
        self.options = ChromeOptions()
        self._DOWNLOAD_DIR = os.path.abspath(download_files)
        cria_dir_no_dir_de_trabalho_atual(dir=download_files, print_value=False, criar_diretorio=True)
        limpa_diretorio(self._DOWNLOAD_DIR)
        
        self.SETTINGS_SAVE_AS_PDF = {
                    "recentDestinations": [
                        {
                            "id": "Save as PDF",
                            "origin": "local",
                            "account": ""
                        }
                    ],
                    "selectedDestinationId": "Save as PDF",
                    "version": 2,
                }


        self.PROFILE = {'printing.print_preview_sticky_settings.appState': json.dumps(self.SETTINGS_SAVE_AS_PDF),
                "savefile.default_directory":  f"{self._DOWNLOAD_DIR}",
                "download.default_directory":  f"{self._DOWNLOAD_DIR}",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": False}            
        self.options.add_experimental_option('prefs', self.PROFILE)

        if headless == True:
            self.options.add_argument('--headless')
            
        self.options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        self.options.add_argument('--kiosk-printing')

        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--disable-gpu')
        self.options.add_argument(f"--user-agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3251.0 Safari/537.36")
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--allow-running-insecure-content")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-setuid-sandbox")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-webgl")
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_argument('--disable-software-rasterizer')
        self.options.add_argument('--no-proxy-server')
        self.options.add_argument("--proxy-server='direct://'")
        self.options.add_argument('--proxy-bypass-list=*')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--block-new-web-contents')
        self.options.add_argument('--incognito')
        self.options.add_argument('–disable-notifications')
        self.options.add_argument('--disable-logging')
        self.options.add_argument("--window-size=1920,1080")
        
        self.service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        
        # create DRIVER
        try:
            self.DRIVER = Chrome(service=self.service, options=self.options)
        except SessionNotCreatedException:
            self.service = Service(ChromeDriverManager(cache_valid_range=0).install())
            self.DRIVER = Chrome(service=self.service, options=self.options)


        self.WDW3 = WebDriverWait(self.DRIVER, timeout=3)
        self.WDW5 = WebDriverWait(self.DRIVER, timeout=5)
        self.WDW7 = WebDriverWait(self.DRIVER, timeout=7)
        self.WDW10 = WebDriverWait(self.DRIVER, timeout=10)
        self.WDW30 = WebDriverWait(self.DRIVER, timeout=30)
        self.WDW60 = WebDriverWait(self.DRIVER, timeout=60)
        self.WDW120 = WebDriverWait(self.DRIVER, timeout=120)
        self.WDW180 = WebDriverWait(self.DRIVER, timeout=180)
        self.WDW = self.WDW7

        """
        O código adiciona suporte para o download automático de arquivos em um diretório especificado no Chrome com headless usando o Selenium WebDriver.
        """
        self.DRIVER.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': self._DOWNLOAD_DIR}}
        command_result = self.DRIVER.execute("send_command", params)

        self.DRIVER.maximize_window()
        
        
        
        return self.DRIVER

    def quit_web(self):
        self.DRIVER.quit()
        
# UTILS #
def faz_log_st(info):
    st.markdown(f'*`{info}`*')
# UTILS #
