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
from tqdm import tqdm
from tqdm import tgrange


# Configura o WebDriver para salvar o arquivo de download em outra folder que não a padrão (C:/Download)
ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_argument("disable-medias-tream")
browser = webdriver.Chrome(options=ChromeOptions)

# Openning the WebSite
openWebsite = browser.get(
    "https://app.tangerino.com.br/Tangerino/pages/baterPonto/")
time.sleep(2)
print("Open WebSite")

# Insert codigoEmpregador
insertCodeEmployee = browser.find_element(
    "xpath", '//*[@id="codigoEmpregador"]').send_keys("B5AXY")
time.sleep(2)


# Insert Password
insertPassword = browser.find_element(
    "xpath", '//*[@id="codigoPin"]').send_keys("6830")
time.sleep(3)

# Clica no Botão de Bater Ponto
clickOnLoginButton = browser.find_element(
    "xpath", '//*[@id="registraPonto"]').click()
time.sleep(2)
print("Ponto batido com sucesso, feio! Pode ir Sextar!")

#pbar = tqdm([openWebsite, insertCodeEmployee, insertPassword])
# for i in pbar:
#    time.sleep(2)
#   pbar.set_description(f'Working on: {i}')
