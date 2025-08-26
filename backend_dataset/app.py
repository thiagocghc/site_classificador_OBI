# Importa as bibliotecas necessárias
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

# Inicializa a aplicação Flask
app = Flask(__name__)
# Habilita o CORS para permitir que o React (rodando em outro domínio/porta) acesse esta API
CORS(app)

# Carrega o dataset CSV para um DataFrame do Pandas assim que o servidor inicia
try:
    df_questoes = pd.read_csv('./backend_dataset/questoes_well_rotuladas.csv')
    # Converte todos os dados para string para evitar problemas de tipo no JSON
    df_questoes = df_questoes.astype(str) 
except FileNotFoundError:
    print("Erro: O arquivo 'questoes_well_rotuladas.csv' não foi encontrado.")
    df_questoes = pd.DataFrame() # Cria um DataFrame vazio se o arquivo não existir

# --- API Endpoints ---

# Endpoint para obter os dados filtrados das questões
@app.route('/api/questoes', methods=['GET'])
def get_questoes():
    # Cria uma cópia do dataframe original para não alterar os dados carregados
    df_filtrado = df_questoes.copy()

    # Pega os parâmetros de filtro da URL (ex: /api/questoes?ano=2003&classe=ordenação)
    ano = request.args.get('ano')
    fase = request.args.get('fase')
    nivel = request.args.get('nivel')
    classe = request.args.get('classe')

    # Aplica os filtros se eles foram fornecidos
    if ano:
        df_filtrado = df_filtrado[df_filtrado['ano'] == ano]
    if fase:
        df_filtrado = df_filtrado[df_filtrado['fase'] == fase]
    if nivel:
        df_filtrado = df_filtrado[df_filtrado['nivel'] == nivel]
    if classe:
        df_filtrado = df_filtrado[df_filtrado['classe'] == classe]

    # Converte o DataFrame filtrado para um formato de dicionário (JSON) e retorna
    resultados = df_filtrado.to_dict(orient='records')
    return jsonify(resultados)

# Endpoint para obter as opções de filtros (os valores únicos de cada coluna)
@app.route('/api/filtros', methods=['GET'])
def get_filtros():
    if not df_questoes.empty:
        opcoes = {
            'ano': sorted(df_questoes['ano'].unique().tolist(), reverse=True),
            'fase': sorted(df_questoes['fase'].unique().tolist()),
            'nivel': sorted(df_questoes['nivel'].unique().tolist()),
            'classe': sorted(df_questoes['classe'].unique().tolist())
        }
        return jsonify(opcoes)
    return jsonify({}) # Retorna objeto vazio se o dataframe não foi carregado

# Inicia o servidor quando o script é executado
if __name__ == '__main__':
    # O debug=True faz o servidor reiniciar automaticamente quando você altera o código
    app.run(debug=True, port=5000)