import pandas as pd
import re

# Boa! Já resolve, o problema ai é se vc tiver vários caracteres, por exemplo:

xorigin = pd.Series('as9!#3.0afg38.49g34-$@0')

# Aplicar várias condicionais talvez seja um desafio, então você pode user Expressões regulares, como:

xreplace = xorigin.str.replace('\D+', "", regex=True)
print(xreplace)

xzfill = xreplace.str.zfill(11)
print(xzfill)

xsub = xorigin.map(lambda x: re.sub('\D+', '', x))
print(xsub)

df = pd.DataFrame({'Original': xorigin, 'Regex_replace': xreplace,
                  'Regex_Re.Sub': xsub, 'Preenche_0': xzfill})
df
