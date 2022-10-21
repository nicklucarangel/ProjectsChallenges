from dataclasses import replace
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import openpyxl
from sqlalchemy import tablesample

browser = webdriver.Chrome()


moedas = ['Dólar', 'Euro']
print(moedas)


# Cotação com laço for


cotacoes = []

for moeda in moedas:
    browser.get("http://www.google.com")
    browser.find_element(
        "xpath", '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(f"Cotação {moeda}")
    browser.find_element(
        "xpath", '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
    cotacaoglobal = browser.find_element(
        "xpath", '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
    cotacoes.append(cotacaoglobal)


dictionary = dict(zip(moedas, cotacoes))
print(dictionary)
print(dictionary['Euro'])


# Cotação Ouro

browser.get("https://www.melhorcambio.com/ouro-hoje")
cotacao_ouro = browser.find_element(
    "xpath", '//*[@id="comercial"]').get_attribute('value')
cotacao_ouro = cotacao_ouro.replace(",", ".")
cotacaoouro = {"Ouro": cotacao_ouro}

browser.quit()

dictionary.update(cotacaoouro)
print(dictionary)

# Carregar a Tabela de Valores
produtos = pd.read_excel(
    "C:\\Users\\nicolas.rangel\\.vscode\\ProjectsChallenges\\Selenium_extract\\Produtos.xlsx")


# Atualizar coluna cotação
# Na coluna "Moedas" == "XYZ", "ALTERA"
Dic_keys = list(dictionary.keys())

for coins in Dic_keys:
    produtos.loc[produtos["Moeda"] == coins,
                 "Cotação"] = float(dictionary[coins])


# Atualizar preço de Compra (preço original*cotação)
produtos["Preço de Compra"] = produtos["Preço Original"] * produtos["Cotação"]
print("Preço de Compra Atualizado")
print(produtos)

# Atualizar preço de Venda (preço original*cotação)
produtos["Preço de Venda"] = produtos["Preço de Compra"] * produtos["Margem"]
print("Preço de Venda Atualizado")
print(produtos)


# Exportar para xcel

produtos.to_excel("Tabela atualizada.xlsx", index=False)
