# Projeto de Pós-Graduação FIAP IA para Devs

Este repositório contém o trabalho desenvolvido para a Pós-Graduação da FIAP em IA para Devs. O projeto utiliza dados públicos do DATASUS/SISCAN, referentes a exames de mamografia de residentes do Estado do Rio de Janeiro em 2025, para construir um fluxo completo de ciência de dados aplicado a um problema de triagem em saúde.

O trabalho contempla a preparação dos dados, a construção de bases supervisionadas, o treinamento de modelos classificatórios, a comparação de modelos baseline, a otimização de hiperparâmetros com Algoritmos Genéticos e a integração com LLMs como camada de interpretação dos resultados.

## Contexto Geral

A base analisada contém registros de mamografia provenientes do SISCAN. O objetivo técnico do projeto é avaliar modelos capazes de classificar uma variável-alvo derivada de indícios de câncer de mama provável, com atenção especial ao desbalanceamento da classe positiva.

Por se tratar de um contexto de saúde, os resultados devem ser interpretados exclusivamente como apoio estatístico e acadêmico. O projeto não produz diagnóstico médico, não recomenda conduta clínica e não substitui avaliação profissional.

## Fases do Projeto

### Fase 1 - Preparação de dados e modelos baseline

Documentação detalhada: [README-FASE-1.md](README-FASE-1.md)

A Fase 1 compreende as partes 1 a 6:

1. tratamento inicial da base SISCAN/Mamografia;
2. preparação da base para classificação supervisionada;
3. treinamento e avaliação do baseline KNN;
4. treinamento e avaliação do baseline SVM;
5. treinamento e avaliação do baseline Random Forest;
6. treinamento e avaliação do baseline de Regressão Logística.

Essa fase gera as bases finais de treino e teste em `bases/` e registra os primeiros resultados comparativos dos modelos.

### Fase 2 - Otimização e integração com LLMs

Documentação detalhada: [README-FASE-2.md](README-FASE-2.md)

A Fase 2 compreende as partes 7 a 10:

7. tuning de SVM com Algoritmos Genéticos;
8. tuning de Regressão Logística com Algoritmos Genéticos;
9. tuning de Random Forest com Algoritmos Genéticos;
10. integração com LLMs por meio do ChatGPT/API da OpenAI.

Essa fase explora otimização evolutiva de hiperparâmetros e utiliza a LLM apenas para explicar resultados estatísticos de forma segura, auditável e sem emissão de diagnóstico.

## Dados e Artefatos

Principais arquivos de dados:

- `SISCAN_MAMOGRAFIA_RJ_2025.parquet`: base original em formato Parquet utilizada no projeto;
- `SISCAN_MAMOGRAFIA_RJ_2025_tratado.parquet`: base tratada gerada na Parte 1;
- `bases/treino/` e `bases/teste/`: bases preparadas para modelagem;
- `resultados/parte_10_integracao_llms/`: prompts, respostas, validações e tabelas geradas pela integração com LLMs.

## Como Executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute os notebooks na ordem numérica, pois as etapas posteriores dependem dos artefatos gerados nas etapas anteriores:

```text
1_tratamento_dados.ipynb
2_preparacao_classificacao.ipynb
3_knn.ipynb
4_svm.ipynb
5_random_forest.ipynb
6_regressao_logistica.ipynb
7_tuning_ga_svm.ipynb
8_tuning_ga_rl.ipynb
9_tuning_ga_rf.ipynb
10_integracao_llms.ipynb
```

Para executar a Parte 10 com chamada real a uma LLM, configure as variáveis de ambiente:

```bash
export OPENAI_API_KEY="sua-chave"
export OPENAI_MODEL="gpt-5.5"
```

Caso `OPENAI_API_KEY` não esteja configurada, o notebook utilizará um cliente demonstrativo local para validar os prompts e os formatos de saída.

## Observações

- A separação entre treino e teste utiliza estratificação para preservar a proporção da variável-alvo.
- Colunas de resultado, laudo, BI-RADS, recomendações e achados finais são tratadas como leakage e não entram nas features dos modelos.
- As métricas mais relevantes para interpretação do projeto são recall, F1, precision e balanced accuracy, especialmente em razão do desbalanceamento da classe positiva.
- A accuracy isolada não deve ser utilizada como critério principal de qualidade do modelo.
