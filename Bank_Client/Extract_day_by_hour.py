import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import sqlalchemy
import os
import datetime
import pyslz
from dotenv import load_dotenv


# Load dotenv informations
load_dotenv()
PostgresURL = os.getenv("YOUR_DOTENV_POSTGRESURL")
print(PostgresURL)


# Configura o WebDriver para salvar o arquivo de download em outra
# folder que não a padrão (C:/Download)
ChromeOptions = webdriver.ChromeOptions()
path = "G:\\XXXXXXX\\XXXXXXXX\\XXXXXXXXX\\XXXXXXXXX\\XXXXXXXXXX"
ChromeOptions.add_experimental_option(
    "prefs", {"download.default_directory": path})

# Configura o Webdriver para rodar no Backend;
ChromeOptions.add_argument("--headless")
browser = webdriver.Chrome(options=ChromeOptions)

# Abrindo o navegador e inserindo a URL desejada;
browser.get("Insert_Website_Here")
browser.maximize_window()
pWindow = browser.current_window_handle
print("Headless Initialized")


# Procura o campo de Username e Preenche com as credenciais;
browser.find_element(
    "xpath", '//*[@id="UserTxt"]').send_keys("Insert_username_here")
time.sleep(2)
# Procura o campo de Password e Preenche com as credenciais;
browser.find_element(
    "xpath", '//*[@id="Password"]').send_keys("Insert_password_here")
time.sleep(2)
# Clica no Botão de login;
browser.find_element(
    "xpath", '//*[@id="BtnOK"]').send_keys(Keys.ENTER)
time.sleep(5)
# Clica em "Relatórios";
browser.find_element(
    "xpath", '//*[@id="ctl00_TopMenu_Reports"]').send_keys(Keys.ENTER)
time.sleep(5)
# Clica em "Relatórios";
browser.find_element(
    "xpath", '//*[@id="sidebar"]/ul/li/h2[2]/a').send_keys(Keys.ENTER)
time.sleep(5)
# Clica em "Receptivo";
browser.find_element(
    "xpath", '//*[@id="GroupTelecom"]/ul[5]/li/h2/a').send_keys(Keys.ENTER)
time.sleep(3)

# Abre a nova página de Campaing in Hour;
browser.get(
    'https://olos-prd.agibank.com.br:8443/reports/inbound/CampaignHourIn.aspx')
time.sleep(3)

# Seleciona a data de hoje e o primeiro dia do mês;
today = pd.to_datetime("today").strftime("%d/%m/" + "20"+"%y")
day_first = pd.to_datetime("today").strftime("01/%m/" + "20"+"%y")


# Insere a nova data inicial de captura do relatório;
browser.find_element(
    "xpath", '//*[@id="PageContent_search1_StartDate"]').send_keys(today)
time.sleep(2)
# Clica em "Template";
browser.find_element(
    "xpath", '//*[@id="PageContent_search1_DDTemplate"]').send_keys(Keys.ENTER)
time.sleep(5)
# find id of option in dropdown menu
relatorio = browser.find_element(By.ID, 'PageContent_search1_DDTemplate')
drop = Select(relatorio)
# select by visible text dropdon menu
drop.select_by_visible_text("Pessoalize_Planejamento")
time.sleep(2)
# Clica em "HTML";
browser.find_element(
    "xpath", '//*[@id="PageContent_search1_btn_html"]').send_keys(Keys.ENTER)
time.sleep(5)
handles = browser.window_handles
for i in handles:
    browser.switch_to.window(i)
    print(browser.title)
time.sleep(3)
browser.maximize_window()
time.sleep(5)
get_url = browser.current_url
time.sleep(5)


# Localizando e lendo a tabela HTML via Pandas, excluindo as colunas de % de
# Abandonadas e % de atendidas, renomeando as colunas para coincidir a
# entrada no DW e inserindo as colunas hash e data;

df_table = pd.read_html(browser.page_source,
                        match='TABLE_PARAMETER_FOR_FIND', header=0)[0]
df_table = df_table.head(
    df_table.shape[0] - 1)
df_table = df_table.drop(['% DE ABANDONADAS', '% DE ATENDIDAS'], axis=1)
df_table.columns = ['HOUR', 'TOTAL_CALLS', 'ATEND', 'ABAND',
                    'NS', 'ATEND_SLA', 'STAT_SUC', 'TMA',
                    'TMF', 'AWT', 'TME']
df_table['NS'] = df_table.NS.str.replace(',', '.')
df_table['NS'] = df_table.NS.str.replace('%', '')

# Insere a coluna data na posição 0 do Dataframe;
df_table.insert(
    0, 'DATA', datetime.datetime.now())
print(df_table)

# Insere a coluna hash na última posição do Dataframe;
df_table.insert(12, 'HASH', datetime.datetime.now().strftime(
    "%d%m" + "20"+"%y") + df_table['HOUR'].str[:2])

print(df_table)

# Abrindo conexão com o banco de dados e inserindo as informações
# Retirar '' da url: url+'DATABASE_NAME'
url = PostgresURL
print(url)
engine = sqlalchemy.create_engine('url'+'DATABASE_NAME')
pyslz.postgres_upsert(df_table, PostgresURL,
                      'DATABASE_NAME', 'TABLE_NAME', 'HASH_COLUMN')
print("Done!")
