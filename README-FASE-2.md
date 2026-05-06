# Fase 2 - Otimização com Algoritmos Genéticos e Integração com LLMs

Este documento descreve os arquivos referentes às partes 7 a 10 do projeto da Pós-Graduação FIAP IA para Devs.

A Fase 2 utiliza as bases preparadas na Fase 1 para otimizar hiperparâmetros com Algoritmos Genéticos e criar uma camada de interpretação com LLMs. A análise permanece concentrada em um problema de classificação desbalanceada em saúde, priorizando métricas como recall, F1, precision e balanced accuracy.

## Entradas Principais

Os notebooks 7, 8 e 9 utilizam as bases encoded geradas na Parte 2:

```text
bases/treino/x_encoded.parquet
bases/treino/y.parquet
bases/teste/x_encoded.parquet
bases/teste/y.parquet
```

A Parte 10 também pode utilizar:

```text
bases/teste/x.parquet
bases/teste/y.parquet
resultados/parte_10_integracao_llms/
```

## Estrutura Geral dos Algoritmos Genéticos

As partes 7, 8 e 9 seguem uma estrutura comum:

- definição de um cromossomo com hiperparâmetros do modelo;
- criação de população inicial com hot start;
- avaliação por validação cruzada estratificada com 5 folds;
- uso de função de fitness voltada à classe positiva;
- seleção por torneio;
- crossover uniforme;
- mutação por gene;
- elitismo;
- execução de três experimentos com configurações diferentes;
- avaliação final do melhor indivíduo em amostra de teste;
- comparação com o baseline da Fase 1.

Função de fitness utilizada:

```text
fitness = 0.7 * F1 + 0.3 * recall
```

Essa escolha aumenta a importância da recuperação da classe positiva, mantendo o F1 como medida de equilíbrio entre precision e recall.

## Parte 7 - Tuning de SVM com Algoritmos Genéticos

Notebook: `7_tuning_ga_svm.ipynb`

Objetivo: otimizar os hiperparâmetros do SVM linear (`LinearSVC`) por meio de um Algoritmo Genético implementado diretamente no notebook.

Cromossomo:

- `C`;
- `class_weight`;
- `scaler_type`;
- `max_iter`.

Principais atividades:

- leitura e preparação das bases encoded;
- amostragem estratificada;
- avaliação do SVM com validação cruzada;
- definição da função de fitness;
- implementação dos operadores genéticos;
- execução de três experimentos;
- tracking de desempenho por geração;
- avaliação final do SVM otimizado;
- comparação com o baseline SVM da Parte 4;
- conclusão operacional sobre o trade-off entre recall, F1, precision e balanced accuracy.

## Parte 8 - Tuning de Regressão Logística com Algoritmos Genéticos

Notebook: `8_tuning_ga_rl.ipynb`

Objetivo: otimizar os hiperparâmetros da Regressão Logística (`LogisticRegression`) utilizando a mesma estrutura evolutiva aplicada na Parte 7.

Cromossomo:

- `C`;
- `class_weight`;
- `scaler_type`;
- `max_iter`.

Principais atividades:

- leitura e preparação das bases encoded;
- amostragem estratificada;
- avaliação da Regressão Logística com validação cruzada;
- uso da mesma função de fitness da Parte 7;
- execução de três experimentos;
- tracking de fitness, tempo e comportamento da população;
- avaliação final do melhor indivíduo;
- comparação com o baseline de Regressão Logística da Parte 6;
- registro da conclusão no notebook.

## Parte 9 - Tuning de Random Forest com Algoritmos Genéticos

Notebook: `9_tuning_ga_rf.ipynb`

Objetivo: otimizar os hiperparâmetros da Random Forest (`RandomForestClassifier`) utilizando Algoritmo Genético.

Cromossomo:

- `n_estimators`;
- `max_depth`;
- `min_samples_leaf`;
- `class_weight`.

Principais atividades:

- leitura e preparação das bases encoded;
- amostragem estratificada;
- avaliação da Random Forest com validação cruzada;
- uso da função de fitness voltada à classe positiva;
- execução de três experimentos com populações e taxas de mutação diferentes;
- tracking de desempenho por geração;
- avaliação final do melhor indivíduo;
- comparação com o baseline Random Forest da Parte 5;
- conclusão sobre os ganhos e trade-offs do modelo otimizado.

## Parte 10 - Integração com LLMs Usando ChatGPT

Notebook: `10_integracao_llms.ipynb`

Objetivo: integrar uma LLM pré-treinada ao fluxo de modelagem para transformar predições individuais e métricas agregadas em explicações compreensíveis, cautelosas e auditáveis.

A LLM não substitui o classificador e não emite diagnóstico. Ela atua apenas como camada de interpretação dos resultados estatísticos gerados nas partes anteriores.

Principais atividades:

- configuração da integração por variáveis de ambiente;
- definição de prompts de segurança e interpretação;
- encapsulamento de cliente LLM;
- consolidação de métricas dos modelos;
- criação de payload individual sem identificação pessoal;
- geração de explicação individual;
- geração de interpretação agregada;
- validação automática das respostas;
- auditoria das interpretações geradas.

Artefatos da Parte 10:

```text
resultados/parte_10_integracao_llms/
  auditoria_interpretacoes_llm.csv
  metricas_modelos_para_llm.csv
  prompt_agregado.txt
  prompt_individual.txt
  resposta_agregada.md
  resposta_individual.md
  validacao_agregada.json
  validacao_individual.json
```

## Configuração da Parte 10

Para executar com uma chamada real à API da OpenAI:

```bash
export OPENAI_API_KEY="sua-chave"
export OPENAI_MODEL="gpt-5.5"
```

Caso `OPENAI_API_KEY` não esteja configurada, o notebook utilizará um cliente local demonstrativo para validar prompts, formato de saída e auditoria.

## Ordem de Execução da Fase 2

```text
7_tuning_ga_svm.ipynb
8_tuning_ga_rl.ipynb
9_tuning_ga_rf.ipynb
10_integracao_llms.ipynb
```

## Observações da Fase 2

- As partes 7, 8 e 9 dependem das bases geradas na Parte 2.
- Cada notebook de Algoritmo Genético registra o histórico de gerações e o resumo dos experimentos.
- A avaliação final utiliza uma amostra estratificada de teste, separada da validação cruzada usada na fitness.
- Em um contexto de triagem, o aumento de recall pode vir acompanhado de queda de precision; esse trade-off deve ser explicitado.
- A Parte 10 deve comunicar incerteza e evitar diagnóstico, prescrição ou recomendação clínica obrigatória.
