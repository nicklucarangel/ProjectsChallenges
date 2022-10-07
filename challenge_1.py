import pandas as pd

df = pd.read_excel(r"C:\Users\nicolas.rangel\Documents\queues_filas.xlsx")

print(df)

df.to_excel('desafio_minha_planilha_Nicolas_Rangel.xlsx', sheet_name='Teste',
            na_rep='#N/A', header=True, index=False)

df.to_excel('desafio_minha_planilha_Nicolas_Rangel.xlsx', sheet_name='Teste',
            na_rep='#N/A', header=True, index=False)
