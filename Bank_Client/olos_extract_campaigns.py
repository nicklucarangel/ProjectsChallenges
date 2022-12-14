from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
import sqlalchemy
import datetime

# Configura o WebDriver para salvar o arquivo de download em outra folder
# que a padrão (C:/Download) -> utilizar se quisermos salvar o arquivo
# em excel por algum motivo

ChromeOptions = webdriver.ChromeOptions()
path = "G:\\.shortcut-targets-by-id\\123fwjtei4poCJz8cDNInJIlvjYLvMhSR\\01. Planejamento\\29. Agi voz\\teste_olos"

files = []

res = os.listdir(path)
for i in res:
    if ".csv" in i and "crdownload" not in i:
        files.append(i)
arquivos_inicial = len(files)
ChromeOptions.add_experimental_option("prefs", {
    "download.default_directory": path})

# Configura o Chrome para rodar no background
ChromeOptions.add_argument("--headless")
browser = webdriver.Chrome(options=ChromeOptions)


# Abre o site da BeMoby
print("Opening Website")
browser.get("https://olos-prd.agibank.com.br:8443/Olos/Login.aspx")
browser.maximize_window()
pWindow = browser.current_window_handle

print("Entering credentials")
# Procura o campo de Username e Preenche com as credenciais;
browser.find_element(
    "xpath", '//*[@id="UserTxt"]').send_keys("pessoalize.ruana")
time.sleep(2)

# Procura o campo de Password e Preenche com as credenciais;
browser.find_element(
    "xpath", '//*[@id="Password"]').send_keys("olos")
time.sleep(2)

# Clica no Botão de login;
browser.find_element(
    "xpath", '//*[@id="BtnOK"]').send_keys(Keys.ENTER)
time.sleep(4)
print("Login...")

# Clica em "Atendimentos";
browser.find_element(
    "xpath", '//*//*[@id="ctl00_PageMenu_LinkButton1"]').send_keys(Keys.ENTER)
time.sleep(10)
print("Click on 'Atendimentos'")

# Expande a visualização do navegador -> Se estiver rodando no BG,
# verifica se não altera ao retirarmos

handles = browser.window_handles
for i in handles:
    browser.switch_to.window(i)
time.sleep(3)
browser.maximize_window()
time.sleep(5)
get_url = browser.current_url

# Altera a página visão global pela página campaign-general, abre uma nova
# aba com as campanhas e inicia o soup do HTML da página
get_url = get_url.replace('visao-global', 'campaign-general')
print("Opening campaign page")
browser.get(get_url)
time.sleep(10)
html = browser.page_source
soup = BeautifulSoup(html, features='html.parser')

# Captura os Headers
print("Capturing Headers")
headers = []
for item in soup.find("div").find("thead").find_next("thead"):
    for dt in item.findAll('th'):
        headers.append(dt.text)
print(headers)
print()

# Encontra as linhas que iremos capturar

rows_list = ['odd row 0', 'row-1', 'odd row-2', 'row-3', 'odd row-4',
             'row-5', 'odd row-6', 'row-7']

df = pd.DataFrame()

# Captura os valores das linhas
print("Capturing Row Values")
values = []
rows = []
columns = ["Id", "Name", "Logados", "Livres", "Trabalhando", "Em Pausa",
           "Nivel de Serviço", "Fila Atual", "Tempo Max. Espera",
           "Chamdas Recebidas", "Total", "Sem Contato", "Agendamentos",
           "Recusas", "Sucesso", "Total", "Abandonadas", "Desviadas",
           "Rejeitadas"]

print("Creating Dataframe")
for i in rows_list:
    values = []
    for item in soup.find("div").find("tbody").find_next("tbody").findAll('tr', {'class': i}):
        for dt in item.findAll('td', {'rowspan': "1"}):
            values.append((dt.text))
        rows = [values]
    df = df.append(pd.DataFrame(rows,
                                columns=columns), ignore_index=True)
print(df)
print()


# Reajusta as colunas e aplica as correções necessárias


df.columns = ['id', 'ag_nome', 'ag_Logados', 'ag_livres', 'ag_trabalhando',
              'ag_em_pausa', 'nivel_servico', 'fila_atual', 'temp_max_fila',
              'chamadas_recebidas', 'transf_total', 'transf_sem_Contato',
              'transf_agendados', 'transf_recusas', 'transf_sucesso',
              'nao_entrantes_total', 'abandonadas', 'desviadas', 'rejeitadas']

df['dt_insert'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
df['nivel_servico'] = df.nivel_servico.str.replace('%', '')
df['abandonadas'] = df.abandonadas.str.replace('\([^()]*\)', '', regex=True)
df['desviadas'] = df.desviadas.str.replace('\([^()]*\)', '', regex=True)
df['rejeitadas'] = df.rejeitadas.str.replace('\([^()]*\)', '', regex=True)

# Abre a conexão com o Bando de Dados
print("Opening Database Connection")
url = "postgresql://postgres:NlZCVwwpTpKwvH3@postgres.codxfeupgo1y.us-east-1.rds.amazonaws.com/"
engine = sqlalchemy.create_engine(url + 'agi')
print("Inserting df on Database")
df.to_sql('agi_parciais', engine, if_exists='replace', index=False)
print("Done!")
