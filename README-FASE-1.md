# Fase 1 - Preparação de Dados e Modelos Baseline

Este documento descreve os arquivos referentes às partes 1 a 6 do projeto da Pós-Graduação FIAP IA para Devs.

A Fase 1 constrói o pipeline inicial do trabalho: tratamento da base SISCAN/Mamografia, definição da variável-alvo, preparação das features, separação entre treino e teste e treinamento de modelos baseline para comparação.

## Fonte de Dados

- Sistema: DATASUS/SISCAN - Mamografia
- Recorte: Rio de Janeiro, 2025
- Formato utilizado nos notebooks: Parquet
- Base original: `SISCAN_MAMOGRAFIA_RJ_2025.parquet`
- Base tratada: `SISCAN_MAMOGRAFIA_RJ_2025_tratado.parquet`

## Parte 1 - Tratamento Inicial

Notebook: `1_tratamento_dados.ipynb`

Objetivo: carregar a base original, avaliar estrutura, dados nulos e consistências básicas, criar variáveis auxiliares e salvar uma versão tratada para as etapas seguintes.

Principais atividades:

- leitura de `SISCAN_MAMOGRAFIA_RJ_2025.parquet`;
- avaliação de dimensões, tipos, uso de memória e estatísticas gerais;
- criação de dicionário operacional das colunas;
- verificação de nulos, strings vazias e colunas sem informação;
- padronização de campos vazios;
- criação de variáveis auxiliares de triagem, rastreamento e BI-RADS;
- gravação da base tratada.

Saída principal:

```text
SISCAN_MAMOGRAFIA_RJ_2025_tratado.parquet
```

## Parte 2 - Preparação Para Classificação

Notebook: `2_preparacao_classificacao.ipynb`

Objetivo: preparar as bases supervisionadas para modelagem, sem treinamento de modelos nesta etapa.

Principais atividades:

- leitura da base tratada;
- definição de features candidatas;
- separação de colunas de leakage e quarentena;
- criação da variável-alvo `TARGET_CANCER_MAMA_PROVAVEL`;
- análise exploratória das features candidatas;
- separação estratificada entre treino e teste;
- tratamento da idade com variáveis numéricas e aplicação de cap;
- aplicação de one-hot encoding após o split;
- exportação das bases finais.

Saídas em `bases/`:

```text
bases/
  treino/
    x.parquet
    x_encoded.parquet
    y.parquet
  teste/
    x.parquet
    x_encoded.parquet
    y.parquet
```

Conteúdo:

- `x.parquet`: features antes do one-hot encoding;
- `x_encoded.parquet`: features após o one-hot encoding;
- `y.parquet`: variável-alvo supervisionada.

## Regras de Leakage

As colunas de resultado, laudo, BI-RADS, recomendações, achados finais e prazos pós-exame são tratadas como leakage e ficam fora de `X_train`, `X_test`, `X_train_encoded` e `X_test_encoded`.

As colunas de avaliação de mama e linfonodos também foram colocadas em quarentena para manter o cenário pré-exame:

- `TP_MAMA_PELE_ESQ`;
- `TP_MAMA_PELE_DIR`;
- `TP_MAMA_ESQ`;
- `TP_MAMA_DIR`;
- `TP_LINFONODO_ESQ`;
- `TP_LINFONODO_DIR`.

Essas colunas somente devem ser utilizadas em outro cenário, por exemplo pós-exame/pré-conduta, se for confirmado que estão disponíveis no momento de uso do modelo.

## Parte 3 - Baseline KNN

Notebook: `3_knn.ipynb`

Objetivo: treinar e avaliar um primeiro classificador KNN utilizando as bases encoded geradas na Parte 2.

Entradas:

```text
bases/treino/x_encoded.parquet
bases/treino/y.parquet
bases/teste/x_encoded.parquet
bases/teste/y.parquet
```

Principais atividades:

- preparação dos dados para KNN;
- comparação entre `CO_IDADE_PACIENTE_CAP` e `CO_IDADE_PACIENTE_NUM`;
- comparação entre `StandardScaler` e `MinMaxScaler`;
- separação estratificada entre treino e validação;
- busca inicial de hiperparâmetros;
- avaliação por accuracy, balanced accuracy, precision, recall, F1 e ROC AUC;
- registro da conclusão no notebook.

## Parte 4 - Baseline SVM

Notebook: `4_svm.ipynb`

Objetivo: treinar e avaliar um baseline SVM linear utilizando `LinearSVC`.

Principais atividades:

- leitura das bases encoded da Parte 2;
- amostragem estratificada para avaliação inicial;
- comparação entre idade com cap e idade numérica;
- comparação entre padronização e normalização;
- tuning com `GridSearchCV`;
- avaliação detalhada do SVM tunado;
- registro da conclusão no notebook.

Resultado validado registrado na documentação anterior:

- melhor `GridSearchCV`: `CO_IDADE_PACIENTE_NUM`, `StandardScaler`, `C=0.1`, `class_weight=balanced`;
- F1 médio no CV: 0,1375;
- accuracy no teste: 0,7361;
- balanced accuracy no teste: 0,6480;
- precision no teste: 0,0871;
- recall no teste: 0,5516;
- F1 no teste: 0,1505;
- ROC AUC no teste: 0,7029.

## Parte 5 - Baseline Random Forest

Notebook: `5_random_forest.ipynb`

Objetivo: treinar e avaliar um baseline Random Forest utilizando `RandomForestClassifier`.

Principais atividades:

- leitura das bases encoded da Parte 2;
- comparação entre idade com cap e idade numérica;
- uso das dummies categóricas como `0/1`;
- ausência de escala, pois Random Forest não depende de distância;
- amostragem estratificada para redução do custo inicial;
- tuning com `GridSearchCV`;
- avaliação detalhada da Random Forest tunada;
- registro da conclusão no notebook.

Resultado validado registrado na documentação anterior:

- melhor `GridSearchCV`: `CO_IDADE_PACIENTE_CAP`, `max_depth=8`, `min_samples_leaf=5`, `n_estimators=200`, `class_weight=balanced_subsample`;
- F1 médio no CV: 0,1572;
- accuracy no teste: 0,8596;
- balanced accuracy no teste: 0,6391;
- precision no teste: 0,1281;
- recall no teste: 0,3982;
- F1 no teste: 0,1938;
- ROC AUC no teste: 0,6892.

## Parte 6 - Baseline Regressão Logística

Notebook: `6_regressao_logistica.ipynb`

Objetivo: treinar e avaliar um baseline de Regressão Logística utilizando `LogisticRegression`.

Principais atividades:

- leitura das bases encoded da Parte 2;
- comparação entre idade com cap e idade numérica sem cap;
- comparação entre `StandardScaler` e `MinMaxScaler`;
- avaliação do impacto de `class_weight='balanced'`;
- tuning com `GridSearchCV`;
- avaliação detalhada da Regressão Logística tunada;
- registro da conclusão no notebook.

A Parte 6 funciona como baseline linear interpretável para comparação com KNN, SVM e Random Forest.

## Ordem de Execução da Fase 1

```text
1_tratamento_dados.ipynb
2_preparacao_classificacao.ipynb
3_knn.ipynb
4_svm.ipynb
5_random_forest.ipynb
6_regressao_logistica.ipynb
```

## Observações da Fase 1

- A Parte 2 é pré-requisito para os notebooks de modelagem.
- KNN, SVM e Regressão Logística são sensíveis à escala e, por isso, comparam estratégias de transformação numérica.
- Random Forest não exige padronização ou normalização.
- As conclusões dos modelos ficam registradas nos próprios notebooks.
- As métricas devem ser interpretadas com foco na classe positiva, pois a variável-alvo é desbalanceada.
