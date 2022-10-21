import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy

req = requests.get(
    'https://www.worldsurfleague.com/athletes/tour/mct?year=2022')

if req.status_code == 200:
    print('ok')
    content = req.content
    print('passou')
    soup = BeautifulSoup(content, 'html.parser')
    print('passou')
    table = soup.find("table")
    print('passou')
    table_string = str(table)
    print('passou')
    tabelafinal = pd.read_html(table_string)[0]
    print(tabelafinal)
    tabelafinal.to_excel("data.xlsx")
