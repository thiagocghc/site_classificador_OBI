import openai
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import json
import unicodedata
import re

# =========================
# Funções auxiliares
# =========================
def _strip_accents(s: str) -> str:
    """Remove acentos de uma string."""
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

# =========================
# Configuração inicial
# =========================
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("A chave da API da OpenAI não foi encontrada. Verifique seu arquivo .env ou variáveis de ambiente.")

client = openai.OpenAI(api_key=api_key)

# Mensagem de sistema simplificada (já que usamos response_format JSON)
SYSTEM_MESSAGE = (
    "Você é um especialista em classificar questões da OBI em três categorias específicas: ORDENAÇÃO, AGRUPAMENTO e OUTROS.\n\n"
    "Siga este raciocínio passo a passo antes de classificar:\n"
    "1. O objetivo principal da questão é definir uma sequência, posição ou arranjo específico? Isso inclui ordem explícita (1º, 2º, etc.) ou implícita (antes/depois, vizinhança, restrições de posição)? → Classifique como ORDENAÇÃO.\n"
    "2. A questão foca na formação de subconjuntos ou seleção de elementos, sem considerar a ordem entre eles? → Classifique como AGRUPAMENTO.\n"
    "3. A questão não se encaixa nas duas anteriores e envolve principalmente o cálculo de valores, tempo, quantidade ou total com base em dados, lógica, fórmulas, estruturas como grafos, tabelas ou explicações de algoritmos? → Classifique como OUTROS.\n\n"
    "IMPORTANTE:\n"
    "- Sempre que possível, prefira classificar como ORDENAÇÃO ou AGRUPAMENTO.\n"
    "- Só use OUTROS quando for impossível enquadrar a questão claramente como ORDENAÇÃO ou AGRUPAMENTO.\n"
    "- Evite usar OUTROS para questões que envolvam posicionamento, ordem de execução ou composição de grupos.\n\n"
    "DICAS:\n"
    "- Quando a resposta for uma lista de posições específicas, ou envolver restrições de ordem ou vizinhança → provavelmente é ORDENAÇÃO.\n"
    "- Quando a resposta for a formação de um grupo, sem qualquer relevância para a ordem → provavelmente é AGRUPAMENTO.\n"
    "- Quando a resposta for um número, uma explicação baseada em propriedades matemáticas, simulação de algoritmo ou estrutura de dados → provavelmente é OUTROS.\n\n"
    "Sua tarefa: analisar o texto e responder SOMENTE com um JSON válido, no formato:\n"
    "{\"classificacao\": \"ordenação\"}\n\n"
    "Respeite exatamente uma das três classes: ordenação, agrupamento ou outros."
)

PROMPT_TEMPLATE = """
EXEMPLOS DE CLASSIFICAÇÃO COM RACIOCÍNIO:

### ORDENAÇÃO:
Enunciado: Três funcionárias, Ana, Bia e Clara, trabalham em três andares diferentes de um prédio (1º, 2º e 3º).
Questão: Se Ana não está no 3º andar e Clara não está no 2º, quais são as distribuições possíveis?
Análise: A questão exige determinar a posição de cada pessoa. Isso é uma relação clara de ordem.
Classificação Final: ordenação

Enunciado: O DJ vai tocar 8 músicas em uma ordem específica.
Questão: Qual das listas abaixo representa uma sequência possível das músicas?
Análise: A sequência de execução é essencial. Foco total na ordem.
Classificação Final: ordenação

Enunciado: João, Maria e Pedro vão se sentar lado a lado. João não pode sentar ao lado de Maria.
Questão: Qual das alternativas mostra uma sequência válida?
Análise: Embora envolva restrições, a questão exige definir a ordem de posicionamento. Ordem implícita.
Classificação Final: ordenação

Enunciado: Cinco alunos vão se sentar em uma fileira. A deve sentar antes de B, e C não pode ficar ao lado de D.
Questão: Qual sequência atende às condições?
Análise: Mesmo com regras, o objetivo é definir posições. Isso caracteriza uma ordenação.
Classificação Final: ordenação

---

### AGRUPAMENTO:
Enunciado: Para um combo de pizzas, o cliente escolhe 4 entre 7 sabores disponíveis.
Questão: Qual das alternativas representa um grupo completo de sabores?
Análise: O objetivo é formar um grupo. A ordem dos sabores não interfere na resposta.
Classificação Final: agrupamento

Enunciado: Nove pessoas receberam convites para uma festa, e algumas restrições definem quem pode ir junto.
Questão: Qual grupo de convidados atende às condições dadas?
Análise: A questão pede para selecionar quem pode compor o grupo, sem ordem.
Classificação Final: agrupamento

Enunciado: Em uma viagem, apenas 4 entre 8 amigos podem ir, respeitando algumas regras.
Questão: Qual grupo pode ser formado?
Análise: O foco está na seleção do grupo. Ordem não importa.
Classificação Final: agrupamento

---

### OUTROS:
Enunciado: Uma palavra é chamada de palíndromo quando sua sequência de letras é a mesma, tanto lida da esquerda para a direita quanto da direita para a esquerda. Exemplos de palíndromos incluem “ovo”, “osso” e “sopapos”.
Questão: Analise as alternativas apresentadas e explique como identificar qual delas não é um palíndromo.
Análise: A questão exige análise de propriedades linguísticas, não ordenação ou agrupamento.
Classificação Final: outros

Enunciado: Em computação, um algoritmo é uma sequência finita e definida de passos para realizar uma tarefa. O exemplo apresentado descreve um algoritmo para calcular o valor de b, a partir de instruções sequenciais e condicionais.
Questão: Analise o algoritmo descrito e explique como determinar o valor final de b impresso ao término da execução.
Análise: O foco é cálculo de valor com base em lógica e execução de instruções.
Classificação Final: outros

Enunciado: Um torneio com 128 jogadores elimina um por rodada.
Questão: Quantas rodadas são necessárias até restar um vencedor?
Análise: Requer aplicação de fórmula matemática. Trata-se de cálculo.
Classificação Final: outros

Enunciado: Em computação, um grafo é formado por vértices e arestas, e pode ser usado para representar, por exemplo, as divisas entre estados de um país: cada vértice representa um estado e uma aresta indica que dois estados possuem divisa geográfica.
Questão: Analise a figura apresentada e explique como identificar, entre os mapas disponíveis, qual deles corresponde às divisas entre estados representadas pelo grafo à esquerda.
Análise: Interpretação de estruturas gráficas. Não envolve ordem ou grupos.
Classificação Final: outros

---

### EXEMPLOS AMBÍGUOS RESOLVIDOS:

Enunciado: Três irmãos vão compartilhar tarefas domésticas, mas nenhum pode repetir uma tarefa. Algumas combinações são inválidas.
Questão: Qual das distribuições atende às regras?
Análise: Apesar de parecer formação de grupo, o foco está em alocar cada um a uma função distinta. Isso implica ordem.
Classificação Final: ordenação

Enunciado: Dez candidatos participaram de um teste, e apenas 4 serão aprovados, respeitando regras de compatibilidade entre eles.
Questão: Qual grupo pode ser selecionado?
Análise: O foco é selecionar um subconjunto de candidatos. A ordem não altera o resultado.
Classificação Final: agrupamento

Enunciado: Um supermercado vende 5 tipos de frutas. Um cliente compra uma combinação de 3 frutas.
Questão: Quantas combinações diferentes ele pode fazer?
Análise: A resposta é um número, baseado em uma fórmula de combinação. Trata-se de um cálculo.
Classificação Final: outros

---

Agora, classifique a seguinte questão:

Texto: {texto}

**Siga o raciocínio passo a passo e analise o objetivo principal da questão.**
Classifique a questão no formato JSON:
{"classificacao": "<ordenação|agrupamento|outros>"}
"""

# =========================
# FastAPI App
# =========================
app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestaoRequest(BaseModel):
    texto: str

@app.post("/classificar")
def classificar(req: QuestaoRequest):
    print("--- NOVA REQUISIÇÃO ---")
    print(f"Texto recebido: {req.texto[:100]}...")

    safe_template = PROMPT_TEMPLATE.replace("{", "{{").replace("}", "}}").replace("{{texto}}", "{texto}")
    formatted_prompt = safe_template.format(texto=req.texto)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": formatted_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0,
            max_tokens=1500
        )

        response_content = response.choices[0].message.content
        print(f"Resposta bruta da OpenAI: {response_content}")

        data = json.loads(response_content)
        classificacao_raw = str(data.get("classificacao", "")).lower()
        classificacao = classificacao_raw

        print(f"Classificação final: {classificacao}")
        return {"classificacao": classificacao}

    except Exception as e:
        print("!!!!!!!! ERRO !!!!!!!!")
        print(f"Ocorreu um erro: {e}")
        print("!!!!!!!!!!!!!!!!!!!!!!")
        return {"erro": str(e)}