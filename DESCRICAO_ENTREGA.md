# AdotaIA: descrição da entrega (etapa prática)

**Instituição beneficiada:** ONG Patinhas do Bem (nome fictício: ainda não há uma ONG parceira definida)

## O que já foi desenvolvido
- **Base de dados sintética** com 800 animais fictícios (seed fixa, reprodutível). O resultado
  "adotado em até 30 dias" segue uma regra probabilística coerente (função logística com ruído), com
  54% de animais adotados. Os dados são claramente identificados como fictícios.
- **Análise exploratória** com a distribuição do alvo e gráficos de adoção por temperamento, porte,
  pelagem, idade e número de divulgações.
- **Modelo de classificação** com Pipeline (OneHotEncoder + StandardScaler), divisão 80/20 estratificada
  e comparação entre Árvore de Decisão, Random Forest e Regressão Logística. A **Regressão Logística**
  teve o melhor resultado: acurácia de 74,4%, F1 de 0,78 e recall de 63% para os animais não adotados.
- **Importância das variáveis**, mostrando que deficiência, temperamento, porte, idade, divulgações,
  vacinação e qualidade da foto são as características que mais pesam.
- **Testes automáticos de coerência**: um filhote dócil recebe alta chance, um cão idoso tímido recebe
  baixa chance, e as ações da ONG (castrar, vacinar, fotografar, divulgar) aumentam a probabilidade.
- **Protótipo funcional em Gradio**, no notebook (link público no Colab) e no `app.py` (execução local):
  formulário com os dados do animal, probabilidade, faixa de chance e até 3 recomendações práticas.

## O que falta implementar
- **Obter os dados reais da ONG**: autorização formal, exportação das planilhas sem dados pessoais dos
  adotantes (LGPD), limpeza e padronização.
- **Retreinar e melhorar o modelo** com os dados reais: validação cruzada, ajuste de hiperparâmetros
  e ajuste do limiar de decisão para identificar mais animais com risco de não serem adotados.
- **Validar com os voluntários** se as previsões e as recomendações fazem sentido na prática.
- **Publicar o sistema online** (por exemplo, no Hugging Face Spaces) para uso pela ONG.
- **Funcionalidades futuras:** cadastro dos animais no próprio sistema e histórico das previsões e adoções.
