
precos = [100, 50, 20, 30]

# Função map pega cada valor de uma lista (precos) e fará uma determinada operação
impostos = list(map(lambda x: x * 0.3, precos))
print(impostos)
