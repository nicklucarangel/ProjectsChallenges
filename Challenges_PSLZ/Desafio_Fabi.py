import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
import sqlalchemy
import pandas as pd
import numpy as np
import xlwings as xw


# Abrindo arquivo dotenv
load_dotenv()
PostgresURL = os.getenv("PostgresURL")
print(PostgresURL)

# Abrindo conexão com o DW e realizando a consulta no banco de dados "Agi"
db = 'DATABASE_PAST_HERE'
url = PostgresURL
engine = sqlalchemy.create_engine(url + db)

qry1 = """QRY_1_DIGIT_HERE"""
df1 = pd.read_sql(qry1, engine)


qry2 = """QRY_2_DIGIT_HERE"""
df2 = pd.read_sql(qry2, engine)


# Diretório da File a ser atualizada
path = "X:\\XXXXXXXXXXXXXXXXXXXXXXXXXXXXX\\XXXX\\XXX\\XXXX\\XXXXX.xlsx"

# Usar o dicionário para mapear as Planilhas do arquivo (Path);
sheet_df_mapping = {'WORKSHEET_1_NAME': df1, 'WORKSHEET_2_NAME': df2}

# Abre o Excel no Background;
with xw.App(visible=False) as app:
    wb = app.books.open(path)

    # Lista dos nomes das Planilhas dentro do Path;
    current_sheets = [sheet.name for sheet in wb.sheets]
    print(current_sheets)
    # Iterar sobre o mapeamento de Planilhas existentes
    # Se a Planilha já existir,irá sobrescrever o conteúdo atual
    # Caso não exista, irá criar uma nova;
    # Irá colocar os dados partindo da célula A2;
    for sheet_name in sheet_df_mapping.keys():
        if sheet_name in current_sheets:
            wb.sheets(sheet_name).range(
                'A2').options(index=False,
                              header=False).value = sheet_df_mapping.get(sheet_name)
        else:
            new_sheet = wb.sheets.add(after=wb.sheets.count)
            new_sheet.range('A2').options(
                index=False, header=False).value = sheet_df_mapping.get(sheet_name)
            new_sheet.name = sheet_name
    wb.save()

print("Done")
