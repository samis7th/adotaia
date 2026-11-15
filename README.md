# 🐾 AdotaIA: previsão de adoção de animais em abrigos

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/samis7th/adotaia/blob/main/AdotaIA.ipynb)

Projeto Integrador Extensionista da disciplina **Inteligência Artificial e Aprendizado de Máquina**.

- **Instituição beneficiada:** ONG Patinhas do Bem (nome fictício: ainda não há uma ONG parceira definida)

> ⚠️ **Os dados deste projeto são fictícios (sintéticos).** Eles foram gerados por código apenas para
> construir e testar o protótipo. As métricas apresentadas **não** representam o desempenho real do
> modelo em um abrigo.

## O problema
ONGs e abrigos têm poucos recursos para divulgação. Animais adultos, idosos, de porte grande, de pelagem
escura ou tímidos costumam ficar muito tempo sem adoção, e a ONG não consegue identificá-los com
antecedência.

## A solução
A partir das características de um animal, o AdotaIA:
1. estima a **probabilidade de adoção em até 30 dias** (classificação binária supervisionada);
2. classifica a chance em **alta** (≥ 60%), **média** (40% a 60%) ou **baixa** (< 40%);
3. sugere até **3 ações práticas** (castrar, fotos melhores, priorizar nas redes etc.).

## Estrutura dos arquivos
```
adotaia/
├── AdotaIA.ipynb               # notebook principal (Etapas 1 a 5), já executado e com saídas
├── app.py                      # protótipo Gradio para rodar localmente
├── dados/animais_sinteticos.csv    # base sintética (800 animais, gerada pelo notebook)
├── modelo/modelo_adocao.joblib     # melhor pipeline treinado (Regressão Logística)
├── requirements.txt
├── README.md
└── DESCRICAO_ENTREGA.md        # o que já foi feito e o que falta
```

## Como executar

### Opção 1: Google Colab (recomendado)
1. Clique no botão **Abrir no Colab** no topo desta página (ou, no Colab, use **Arquivo → Fazer upload de
   notebook** e escolha `AdotaIA.ipynb`).
2. Clique em **Ambiente de execução → Executar tudo**.
3. O notebook instala o Gradio, gera os dados, treina e avalia os modelos e salva o modelo.
4. A última célula abre a interface e mostra um **link público** (`share=True`). O link é temporário e
   só funciona enquanto o ambiente do Colab estiver ligado.

O notebook não depende de nenhum arquivo externo: ele mesmo gera a base de dados.

### Opção 2: Computador local
Requisitos: Python 3.10 ou superior.

```bash
git clone https://github.com/samis7th/adotaia.git
cd adotaia
pip install -r requirements.txt
python app.py
```

Abra no navegador o endereço mostrado no terminal (normalmente <http://127.0.0.1:7860>).

O `app.py` usa o arquivo `modelo/modelo_adocao.joblib`, que já está na pasta. Para gerar o modelo de novo,
execute o notebook localmente (`jupyter notebook AdotaIA.ipynb`) ou no Colab e baixe a pasta `modelo/`.

> **Dica:** um modelo salvo com uma versão do scikit-learn pode gerar avisos ou erros em outra versão.
> Se treinar no Colab e rodar localmente, confira a versão do Colab com
> `import sklearn; print(sklearn.__version__)` e instale a mesma versão no computador.

## Resultados iniciais (dados sintéticos, 160 animais de teste)

| Modelo | Acurácia | F1 (adotado) | Recall "não adotado" |
|---|---|---|---|
| Árvore de Decisão | 0,588 | 0,663 | 0,397 |
| Random Forest | 0,681 | 0,730 | 0,548 |
| **Regressão Logística** | **0,744** | **0,781** | **0,630** |

A Regressão Logística foi escolhida (maior F1 médio entre as classes). O recall da classe
"não adotado" é a métrica que mais interessa à ONG, porque são esses animais que precisam de atenção extra.

## Tecnologias
Python, pandas, NumPy, scikit-learn (Pipeline, ColumnTransformer, OneHotEncoder, StandardScaler),
matplotlib, seaborn, joblib e Gradio.

## Dados reais (próxima etapa)
Os dados reais virão das planilhas de cadastro e do histórico de adoções da ONG, com autorização formal da
instituição. Dados pessoais dos adotantes (nome, CPF, telefone, endereço) **não serão coletados**, em
respeito à LGPD: apenas as características dos animais e as datas de entrada/adoção. Detalhes na
Etapa 2 do notebook.
