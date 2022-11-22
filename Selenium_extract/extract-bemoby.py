from dataclasses import replace
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import openpyxl
from sqlalchemy import tablesample
import time


# Configura o WebDriver para salvar o arquivo de download em outra folder que não a padrão (C:/Download)
ChromeOptions = webdriver.ChromeOptions()

ChromeOptions.add_experimental_option("prefs", {
                                      "download.default_directory": "G:\\.shortcut-targets-by-id\\123fwjtei4poCJz8cDNInJIlvjYLvMhSR\\01. Planejamento\\27. GAB\Base_para_carga"})

browser = webdriver.Chrome(options=ChromeOptions)


# Seleciona a data de hoje;
hj = pd.to_datetime("today").strftime("%d/%m"+"/20"+"%y")

# Abre o site da BeMoby
browser.get("https://admin.bemoby.com/login.jsf?logout=true")
time.sleep(2)
print("Headless Initialized")

# Procura o campo de Username e Preenche com as credenciais;
browser.find_element(
    "xpath", '//*[@id="username"]').send_keys("renato.aragon@pessoalize.com")
time.sleep(2)


# Procura o campo de Password e Preenche com as credenciais;
browser.find_element(
    "xpath", '//*[@id="password"]').send_keys("Bemoby123@")
time.sleep(2)

# Clica no Botão de login;
browser.find_element(
    "xpath", '//*[@id="btn-submit"]').send_keys(Keys.ENTER)
time.sleep(2)
print("Login Sucefull")

# Clica em "Relatórios";
browser.find_element(
    "xpath", '//*[@id="dtLj_idt123"]').send_keys(Keys.ENTER)
time.sleep(2)
print("Relatório Ok")

# Clica em Call Center
browser.find_element(
    "xpath", '//*[@id="dtLj_idt128"]').send_keys(Keys.ENTER)
time.sleep(2)
print("Callcenter Ok")

# Clica em Atendimentos
browser.find_element(
    "xpath", '//*[@id="mnuCallCenterCallDetailReport"]/a').send_keys(Keys.ENTER)
time.sleep(2)
print("Atendimentos Ok")

# Seleciona o campo de data inicial da extração e da um "CTRL + a";
browser.find_element(
    "xpath", '//*[@id="frmCallCenterCallDetailReport:startCreateDate"]').send_keys(Keys.CONTROL + "a")
time.sleep(2)
print("CTRL+A Ok")

# Insere a nova data inicial de captura do relatório;
browser.find_element(
    "xpath", '//*[@id="frmCallCenterCallDetailReport:startCreateDate"]').send_keys("01/11/2022")
time.sleep(2)
print("Data Inicial Ok")

# Insere a data final de captura do relatório;
browser.find_element(
    "xpath", '//*[@id="frmCallCenterCallDetailReport:endCreateDate"]').send_keys(hj)
time.sleep(2)
print("Data Final Ok")

# Clica em "Pesquisa";
browser.find_element(
    "xpath", '//*[@id="frmCallCenterCallDetailReport:btnSearch"]').send_keys(Keys.ENTER)
time.sleep(10)
print("Searching...")

# Clica em "Exportar";
browser.find_element(
    "xpath", '//*[@id="frmCallCenterCallDetailReport:pnlTableResult"]/div[1]/div/div/div/button').send_keys(Keys.ENTER)
time.sleep(10)
print("Founding...")

# Clica em "CSV";
browser.find_element(
    "xpath", '//*[@id="frmCallCenterCallDetailReport:j_idt775"]').send_keys(Keys.ENTER)
time.sleep(2)
print("Finding File Format...")

# Clica em "Exportar";
browser.find_element(
    "xpath", '//*[@id="frmCallCenterCallDetailReport:mdlCsvExportConfig"]/div/div/div[3]/a[2]').send_keys(Keys.ENTER)
print("Exporting...")
