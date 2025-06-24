import re
import os
import pandas as pd
from io import StringIO

# SITE PARA EXTRAÇÃO DO CSV: https://www.yahii.com.br/dolardiario.html

texto_original = '''
COLE AQUI SEU TEXTO
'''

# Expressão regular para capturar data, compra e venda
linhas = []
padrao_data = re.compile(r"(\d{2}/\d{2}/\d{4})\s+([\d.,]+)\s+([\d.,]+)")

for linha in texto_original.splitlines():
    match = padrao_data.search(linha)
    if match:
        data, compra, venda = match.groups()
        compra = compra.replace('.', '').replace(',', '.')
        venda = venda.replace('.', '').replace(',', '.')
        linhas.append(f"{data};{compra};{venda}")

# Criação do DataFrame com separador ;
df_extraido = pd.read_csv(StringIO('\n'.join(linhas)), sep=';', names=['data', 'valor_compra', 'valor_venda'])

# Conversão da coluna data e extração do mês
df_extraido['data'] = pd.to_datetime(df_extraido['data'], format='%d/%m/%Y', errors='coerce')
df_extraido = df_extraido.dropna(subset=['data'])
df_extraido['mes'] = df_extraido['data'].dt.month

# Reorganiza as colunas
df_resultado = df_extraido[['data', 'valor_compra', 'valor_venda']]

# Exporta para CSV no mesmo diretório
caminho_csv = os.path.join(os.getcwd(), 'cotacoes_EURO_DOLAR.csv')
df_resultado.to_csv(caminho_csv, sep=';', index=False)

print(f"✅ Arquivo CSV gerado com sucesso: {caminho_csv}")