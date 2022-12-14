import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import sqlalchemy
import os
import pyslz


# Load dotenv informations;
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
print("Login...")


# Clica em "Relatórios 1st";
browser.find_element(
    "xpath", '//*[@id="ctl00_TopMenu_Reports"]').send_keys(Keys.ENTER)
time.sleep(5)
print("Relatório Ok")


# Clica em "Relatórios 2nd";
browser.find_element(
    "xpath", '//*[@id="sidebar"]/ul/li/h2[2]/a').send_keys(Keys.ENTER)
time.sleep(5)
print("Relatório menu lateral Ok")


# Clica em "Receptivo";
browser.find_element(
    "xpath", '//*[@id="GroupTelecom"]/ul[5]/li/h2/a').send_keys(Keys.ENTER)
time.sleep(3)
print("Receptivo Ok")


# Clica em "dia";
browser.find_element(
    "xpath", '//*[@id="menu_telecom_inbound"]/li[5]/a').send_keys(Keys.ENTER)
time.sleep(3)
print("dia Ok")

# Seleciona o range de datas a ser inserido e capturado;
today = pd.to_datetime("today").strftime("%d/%m/" + "20"+"%y")
day_first = pd.to_datetime("today").strftime("01/%m/" + "20"+"%y")

print(type(today))

# Insere a nova data inicial de captura do relatório;
browser.find_element(
    "xpath", '//*[@id="PageContent_search1_StartDate"]').send_keys(day_first)
time.sleep(2)
print("Data inicial Ok")


# Insere a nova data final de captura do relatório;
browser.find_element(
    "xpath", '//*[@id="PageContent_search1_EndDate"]').send_keys(today)
time.sleep(2)
print("Data final Ok")


# Clica em "Template";
browser.find_element(
    "xpath", '//*[@id="PageContent_search1_DDTemplate"]').send_keys(Keys.ENTER)
time.sleep(5)
print("template Ok")


# find id of option in dropdown menu;
relatorio = browser.find_element(By.ID, 'PageContent_search1_DDTemplate')
drop = Select(relatorio)

# select by visible text dropdon menu;
drop.select_by_visible_text("SELECT_DROPDOWNMENU_OPTION")
time.sleep(2)


# Clica em "HTML";
browser.find_element(
    "xpath", '//*[@id="PageContent_search1_btn_html"]').send_keys(Keys.ENTER)
time.sleep(5)
print("file donwloading")

handles = browser.window_handles
print(handles)
for i in handles:
    browser.switch_to.window(i)
    print(browser.title)
time.sleep(3)
browser.maximize_window()
time.sleep(5)
get_url = browser.current_url
print(get_url)

time.sleep(5)

# Lendo a tabela HTML via Pandas através da função "match", excluindo
# as colunas de "% DE ABANDONADAS"e "% DE ATENDIDAS" e renomeando as
# colunas para coincidir a entrada no DW;

df_table = pd.read_html(browser.page_source,
                        match='TABLE_PARAMETER_FOR_FIND', header=0)[0]
df_table = df_table.head(
    df_table.shape[0] - 1).drop(['% DE ABANDONADAS', '% DE ATENDIDAS'], axis=1)
df_table.columns = ['DATA_COLUMN', 'COLUMN_1', 'COLUMN_2', 'COLUMN_3',
                    'COLUMN_4', 'COLUMN_5', 'COLUMN_6', 'COLUMN_7', 'COLUMN_8',
                    'COLUMN_9', 'COLUMN_10']
df_table['COLUMN_4'] = df_table.COLUMN_4.str.replace(',', '.')
df_table['COLUMN_4'] = df_table.COLUMN_4.str.replace('%', '')
df_table.insert(11, 'hash', df_table['DATA_COLUMN'].str.replace('/', ''))
df_table.info()
print(df_table)


# Abrindo conexão com o banco de dados e inserindo as informações de acesso
# Retirar '' da url: url+'DATABASE_NAME'
url = PostgresURL
engine = sqlalchemy.create_engine('url'+'DATABASE_NAME')
pyslz.postgres_upsert(df_table, PostgresURL, 'DATABASE_NAME',
                      'TABLE_NAME', 'HASH_COLUMN')
print("Done!")
