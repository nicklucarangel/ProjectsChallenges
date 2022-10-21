import pandas as pd

df = pd.read_excel(r"C:\Users\nicolas.rangel\Documents\queues_filas.xlsx")

print(df)

df.to_excel('testando.xlsx')
