"""
DIREITOS RESERVADOS / RIGHTS RESERVED / DERECHOS RESERVADOS

https://online2pdf.com/pt/converter-pdf-para-txt-com-ocr

Esse robô envia o PDF para o site https://online2pdf.com/pt/converter-pdf-para-txt-com-ocr
    e recupera um arquivo txt com o ocr
    

"""
from __future__ import annotations
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from funcsforspo_l.fpython.functions_for_py import *
from funcsforspo_l.fselenium.functions_selenium import *
from funcsforspo_l.fexceptions.exceptions import FalhaAoRecuperarOcr
from funcsforspo_l.fpdf.base.base import Bot
import json
import os

class PdfToXlsx(Bot):  
    def __init__(self, file_pdf, headless=True) -> None:
        """Init

        Args:
            file_pdf (str): Caminho do arquivo
            dir_exit (str, optional): Local de saída do arquivo TXT. Defaults to 'output'.
            headless (bool, optional): executa como headless. Defaults to True.
        """
        download_files = 'output'
        super().__init__(headless, download_files)
        if isinstance(file_pdf, str):
            self.FILE_PDF = os.path.abspath(file_pdf)
            self.CONVERTER_VARIOS_ARQUIVOS = False
            self.MESCLAR_EM_UMA_LINHA = False
        else:
            print('Envie, uma string como caminho do parâmetro file_pdf')

        
        try:
            print('Acessando o site...')
            self.DRIVER.get('https://online2pdf.com/')
            
            def envia_file():
                print('Enviando o arquivo...')
                self.DRIVER.find_element(By.CSS_SELECTOR, '#input_file0').send_keys(self.FILE_PDF)
                
            def converte_excel():
                print('Convertendo em Excel...')
                espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#selectbox_2 > table > tbody > tr > td:nth-child(1) > div'))
                espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#selectbox_content > div:nth-child(10) span'))
            
            def ativa_ocr():
                print('Ativando o OCR...')
                espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#selectbox_text_4'))
                espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#selectbox_content > div:nth-child(2) span'))
                espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#export_fullocr_box span'))
            
            def clica_em_converter():
                print('Clicando em converter...')
                espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, 'button[onclick="checkServerStatus();"]'))
            
            def aguarda_conversao():
                print('Aguardando conversão...')
                espera_elemento_sair_do_dom(self.WDW180, (By.CSS_SELECTOR, '#progress_window[style="display: block;"]'))
                print('Verificando se baixou...')
                
                verifica_se_baixou_o_arquivo(self._DOWNLOAD_DIR, '.xlsx')

            envia_file()
            converte_excel()
            ativa_ocr()
            clica_em_converter()
            aguarda_conversao()
            
        except Exception as e:
            print('Ocorreu um erro!')
            print(str(e))
            

            
    def recupera_texto(self) -> str:
        try:
            file_txts = arquivos_com_caminho_absoluto_do_arquivo(self._DOWNLOAD_DIR)
            file_txt = file_txts[-1]
            text = None
            with open(file_txt, mode='r', encoding='utf-16-le') as f:
                text = f.read()
            shutil.rmtree(self._DOWNLOAD_DIR)
            return text
        except IndexError:
            raise FalhaAoRecuperarOcr('Ocorreu um erro na recuperação que causou um IndexError, provavelmente não baixou o arquivo.')