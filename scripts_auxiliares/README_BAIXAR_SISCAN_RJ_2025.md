# Obtencao dos Dados SISCAN 2025 - RJ

Este material contem um script para baixar do FTP publico do DATASUS os arquivos CSV nacionais do SISCAN de 2025 e gerar copias filtradas para o estado do Rio de Janeiro.

Fonte dos dados:

```text
ftp://ftp.datasus.gov.br/dissemin/publicos/SISCAN/SISCAN/
```

## Instalar bibliotecas Python

Comando idempotente para instalar as bibliotecas usadas pelo script:

```bash
python3 -m venv .venv-siscan
. .venv-siscan/bin/activate
python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements.txt
```

## Baixar e filtrar os dados

```bash
python baixar_siscan_rj_2025.py
```

Por padrao, o script:

- baixa os CSVs originais para `dados/raw/`;
- filtra os registros de residentes do RJ, usando `SG_UF_RESIDENCIA = RJ` ou `CO_UF_RESIDENCIA = 33`;
- salva os CSVs filtrados em `dados/rj_2025/`;
- nao baixa novamente arquivos brutos que ja existam com o mesmo tamanho;
- nao recria arquivos filtrados ja existentes, exceto com `--sobrescrever`.

## Tipos de dados disponiveis

Use a opcao `--tipos` para baixar um ou mais conjuntos especificos. Sem essa opcao, o script usa `todos`.

| Tipo | Descricao |
| --- | --- |
| `todos` | Baixa e filtra todos os conjuntos listados abaixo. |
| `cito_colo` | Exames citopatologicos de colo do utero, por local de residencia. |
| `cito_colo_pacnt` | Exames citopatologicos de colo do utero, por paciente. |
| `cito_mama` | Exames citopatologicos de mama, por local de residencia. |
| `cito_mama_pacnt` | Exames citopatologicos de mama, por paciente. |
| `histo_colo` | Exames histopatologicos de colo do utero, por local de residencia. |
| `histo_colo_pacnt` | Exames histopatologicos de colo do utero, por paciente. |
| `histo_mama` | Exames histopatologicos de mama, por local de residencia. |
| `histo_mama_pacnt` | Exames histopatologicos de mama, por paciente. |
| `mamografia` | Exames de mamografia, por local de residencia. |
| `mamografia_pacnt` | Exames de mamografia, por paciente. |

## Tipo indicado para triagem de cancer de mama

Para estudar triagem/rastreamento de cancer de mama, o tipo mais indicado e `mamografia`.

Motivo: esse conjunto representa os exames de mamografia e contem variaveis diretamente ligadas ao rastreamento e ao resultado da triagem, como `TP_MAMOGRAFIA_RASTREAMENT`, `CO_IND_CLINICA`, `CO_BIRADS`, `CO_RECOMENDACAO`, `TP_RECOMENDACAO_ESQUERDA`, `TP_RECOMENDACAO_DIREITA`, idade, sexo, municipio/UF de residencia e mes/ano de competencia.

Use `mamografia_pacnt` quando a analise precisar acompanhar pacientes anonimizados via `CO_PACIENTE`, mas observe que esse tipo tem menos colunas de achados detalhados. Os tipos `histo_mama` e `cito_mama` sao mais adequados para analises diagnosticas/complementares, nao para medir diretamente a triagem por mamografia.

## Comandos uteis

Listar os arquivos que seriam baixados:

```bash
python baixar_siscan_rj_2025.py --somente-listar
```

Baixar apenas mamografia:

```bash
python baixar_siscan_rj_2025.py --tipos mamografia
```

Baixar mais de um tipo especifico:

```bash
python baixar_siscan_rj_2025.py --tipos mamografia cito_mama histo_mama
```

Refazer downloads e filtros:

```bash
python baixar_siscan_rj_2025.py --sobrescrever
```

Alterar diretorios de entrada e saida:

```bash
python baixar_siscan_rj_2025.py --raw-dir dados_brutos --out-dir dados_filtrados_rj
```

Observacao: alguns arquivos nacionais de 2025 sao grandes. Se a conexao cair, execute o mesmo comando novamente; arquivos completos serao reaproveitados.

## Colunas por tipo

As colunas abaixo foram lidas dos cabecalhos dos arquivos CSV de 2025 no FTP do DATASUS. As descricoes sao um dicionario operacional para orientar a analise; para codigos categoricos, consulte a documentacao/tabulacoes oficiais do SISCAN quando precisar dos rotulos de cada valor.

<details>
<summary><code>cito_colo</code> - 84 colunas</summary>

| Coluna | O que representa |
| --- | --- |
| `CO_SEQ_SISCAN_CITO_COLO_RESID` | Identificador sequencial do registro de citopatologico de colo, por residencia. |
| `CO_UF_UNIDADE_SAUDE` | Codigo da UF da unidade de saude. |
| `CO_UF_RESIDENCIA` | Codigo da UF de residencia da pessoa atendida. |
| `CO_UF_PREST_SERVICO` | Codigo da UF do prestador de servico. |
| `CO_MUN_UNIDADE_SAUDE` | Codigo IBGE do municipio da unidade de saude. |
| `CO_MUN_RESIDENCIA` | Codigo IBGE do municipio de residencia da pessoa atendida. |
| `CO_MUN_PREST_SERVICO` | Codigo IBGE do municipio do prestador de servico. |
| `CO_UNIDADE_SAUDE` | Codigo da unidade de saude. |
| `CO_PREST_SERVICO` | Codigo do prestador de servico. |
| `CO_ANO_LIBERACAO` | Ano de liberacao do exame/laudo. |
| `CO_ANO_MES_LIBERACAO` | Ano e mes de liberacao do exame/laudo. |
| `CO_RACA_COR` | Codigo de raca/cor da pessoa atendida. |
| `CO_ETNIA` | Codigo de etnia, quando informado. |
| `CO_IDADE_PACIENTE` | Idade da pessoa atendida. |
| `CO_ESCOLARIDADE` | Codigo de escolaridade. |
| `TP_RESP_EXAME_PREVENTIVO_REALI` | Resposta sobre realizacao previa de exame preventivo. |
| `CO_PERIODO_PREVENTIVO` | Periodo desde o ultimo exame preventivo. |
| `ST_SINAL_SUGESTIVO_DST` | Indicador/status de sinal sugestivo DST. |
| `ST_DENTRO_LIMITE_NORMALIDADE` | Indicador/status de dentro limite normalidade. |
| `TP_AVALIACAO_AMOSTRA` | Classificacao da avaliacao da amostra. |
| `TP_ATIPIA_CELULAR_ESCAMOS` | Tipo ou classificacao de atipia celular escamosa. |
| `TP_ATIPIA_CELULAR_GLANDUL` | Tipo ou classificacao de atipia celular glandular. |
| `TP_CEL_ORIG_INF_SIGN_INDE` | Tipo ou classificacao de celula origem informacao significado indeterminado. |
| `ST_OUTRA_NEOPLASIA_MALIGNA` | Indicador/status de outra neoplasia maligna. |
| `ST_CELULA_ENDOMETRIAL_PRESENTE` | Indicador/status de celula endometrial presente. |
| `CO_INTERVALO_COLETA` | Intervalo entre etapas de coleta. |
| `CO_INTERVALO_EXAME` | Intervalo ate a realizacao do exame. |
| `CO_TEMPO_EXAME` | Faixa/codigo do tempo ate a realizacao do exame. |
| `ST_REPRESENTATI_ZONA_TRANSFORM` | Indicador/status de representatividade zona transformacao. |
| `ST_SCREENING_REALIZADO` | Indicador/status de screening realizado. |
| `TP_MOTIVO_EXAME` | Motivo declarado para o exame. |
| `NU_AMOSTRA_REJEITADA` | Numero, valor ou indicador de amostra rejeitada. |
| `CO_REJ_AUSENCIA` | Codigo de rejeicao ausencia. |
| `CO_REJ_LAMINA` | Codigo de rejeicao lamina. |
| `CO_REJ_CAUSA_ALHEIA` | Codigo de rejeicao causa alheia. |
| `CO_REJ_OUT_CAUSAS` | Codigo de rejeicao out causas. |
| `NU_AMOSTRA_SATISFATORIA` | Numero, valor ou indicador de amostra satisfatoria. |
| `CO_INS_MAT_CELULAR` | Codigo de insatisfatoriedade material celular. |
| `CO_INS_SANGUE` | Codigo de insatisfatoriedade sangue. |
| `CO_INS_PIOCITOS` | Codigo de insatisfatoriedade piocitos. |
| `CO_INS_ARTEF_DES` | Codigo de insatisfatoriedade artefatos dessecamento. |
| `CO_INS_CONTAM_EXTERNOS` | Codigo de insatisfatoriedade contaminantes externos. |
| `CO_INS_INTENSA_SUPER` | Codigo de insatisfatoriedade intensa superposicao. |
| `CO_INS_OUTROS` | Codigo de insatisfatoriedade outros. |
| `CO_ALT_CEL_INFLAMACAO` | Codigo de alteracao celula inflamacao. |
| `CO_ALT_CEL_METAPLASIA` | Codigo de alteracao celula metaplasia. |
| `CO_ALT_CEL_REPARACAO` | Codigo de alteracao celula reparacao. |
| `CO_ALT_CEL_ATROFIA` | Codigo de alteracao celula atrofia. |
| `CO_ALT_CEL_RADIACAO` | Codigo de alteracao celula radiacao. |
| `CO_ALT_CEL_OUT` | Codigo de alteracao celula out. |
| `CO_MIC_LACTOBACILLUS` | Codigo de micro lactobacillus. |
| `CO_MIC_COCOS` | Codigo de micro cocos. |
| `CO_MIC_SUGEST_CHLAMYDIA` | Codigo de micro sugestivo chlamydia. |
| `CO_MIC_ACTINOMYCES` | Codigo de micro actinomyces. |
| `CO_MIC_CANDIDA` | Codigo de micro candida. |
| `CO_MIC_TRICHOMONAS` | Codigo de micro trichomonas. |
| `CO_MIC_EFEITO_CITOPATICO` | Codigo de micro efeito citopatico. |
| `CO_MIC_BACILOS_SUPRA` | Codigo de micro bacilos supracitoplasmaticos. |
| `CO_MIC_OUTROS_BACILOS` | Codigo de micro outros bacilos. |
| `CO_MIC_OUTROS` | Codigo de micro outros. |
| `CO_EPIT_ESCAMOSO` | Codigo de epitelio escamoso. |
| `CO_EPIT_GLANDULAR` | Codigo de epitelio glandular. |
| `CO_EPIT_METAPLAS` | Codigo de epitelio metaplasico. |
| `NU_CA_ESCAMOSA_P_NAO_NEOPLAST` | Numero, valor ou indicador de celulas alteradas escamosa papilifera nao neoplastica. |
| `NU_CA_ESCAMOSA_N_AF_LESAO_AG` | Numero, valor ou indicador de celulas alteradas escamosa n a favor lesao alto grau. |
| `NU_CA_GLANDULAR_NAO_NEOPL` | Numero, valor ou indicador de celulas alteradas glandular nao neopl. |
| `NU_CA_GLANDULA_N_AF_LESAO_AG` | Numero, valor ou indicador de celulas alteradas glandula n a favor lesao alto grau. |
| `NU_CA_ORIGEM_IND_NAO_NEOPLAST` | Numero, valor ou indicador de celulas alteradas origem indeterminado nao neoplastica. |
| `NU_CA_IND_NAO_LESAO` | Numero, valor ou indicador de celulas alteradas indeterminado nao lesao. |
| `NU_LESAO_IE_BAIXO_GRAU` | Numero, valor ou indicador de lesao ie baixo grau. |
| `NU_LESAO_IE_ALTO_GRAU` | Numero, valor ou indicador de lesao ie alto grau. |
| `NU_LES_IE_ALTO_GRAU_N_MIC_INV` | Numero, valor ou indicador de lesao ie alto grau n micro invasor. |
| `NU_CARC_EPIDERM_INV` | Numero, valor ou indicador de carcinoma epidermoide invasor. |
| `NU_ADENOCAR_INS_SITU` | Numero, valor ou indicador de adenocarcinoma insatisfatoriedade in situ. |
| `NU_ADENOCAR_INVASOR` | Numero, valor ou indicador de adenocarcinoma invasor. |
| `NU_OUTRAS_NEOPLASIAS` | Numero, valor ou indicador de outras neoplasias. |
| `NU_LIMITE_NORMALIDADE` | Numero, valor ou indicador de limite normalidade. |
| `TP_CEL_ESCAM_SIGN_INDETER` | Tipo ou classificacao de celula escam significado indeter. |
| `TP_CEL_GLAND_SIGNIF_INDET` | Tipo ou classificacao de celula gland signif indeterminado. |
| `NU_EXAME_ALTERADO` | Numero, valor ou indicador de exame alterado. |
| `CO_LAUDO_CITOPATOLOGICO` | Codigo do laudo citopatologico. |
| `CO_ANO_RESULTADO` | Ano do resultado do exame. |
| `CO_ANO_MES_RESULTADO` | Ano e mes do resultado do exame. |
| `SG_SEXO` | Sexo da pessoa atendida. |

</details>

<details>
<summary><code>cito_colo_pacnt</code> - 86 colunas</summary>

| Coluna | O que representa |
| --- | --- |
| `CO_SEQ_SISCAN_CITO_COLO_PACNT` | Identificador sequencial do registro de citopatologico de colo, por paciente. |
| `CO_UF_UNIDADE_SAUDE` | Codigo da UF da unidade de saude. |
| `CO_UF_RESIDENCIA` | Codigo da UF de residencia da pessoa atendida. |
| `CO_UF_PREST_SERVICO` | Codigo da UF do prestador de servico. |
| `CO_MUN_UNIDADE_SAUDE` | Codigo IBGE do municipio da unidade de saude. |
| `CO_MUN_RESIDENCIA` | Codigo IBGE do municipio de residencia da pessoa atendida. |
| `CO_MUN_PREST_SERVICO` | Codigo IBGE do municipio do prestador de servico. |
| `CO_UNIDADE_SAUDE` | Codigo da unidade de saude. |
| `CO_PREST_SERVICO` | Codigo do prestador de servico. |
| `CO_ANO_LIBERACAO` | Ano de liberacao do exame/laudo. |
| `CO_ANO_MES_LIBERACAO` | Ano e mes de liberacao do exame/laudo. |
| `CO_RACA_COR` | Codigo de raca/cor da pessoa atendida. |
| `CO_ETNIA` | Codigo de etnia, quando informado. |
| `CO_IDADE_PACIENTE` | Idade da pessoa atendida. |
| `CO_ESCOLARIDADE` | Codigo de escolaridade. |
| `TP_RESP_EXAME_PREVENTIVO_REALI` | Resposta sobre realizacao previa de exame preventivo. |
| `CO_PERIODO_PREVENTIVO` | Periodo desde o ultimo exame preventivo. |
| `ST_SINAL_SUGESTIVO_DST` | Indicador/status de sinal sugestivo DST. |
| `ST_DENTRO_LIMITE_NORMALIDADE` | Indicador/status de dentro limite normalidade. |
| `TP_AVALIACAO_AMOSTRA` | Classificacao da avaliacao da amostra. |
| `TP_ATIPIA_CELULAR_ESCAMOS` | Tipo ou classificacao de atipia celular escamosa. |
| `TP_ATIPIA_CELULAR_GLANDUL` | Tipo ou classificacao de atipia celular glandular. |
| `TP_CEL_ORIG_INF_SIGN_INDE` | Tipo ou classificacao de celula origem informacao significado indeterminado. |
| `ST_OUTRA_NEOPLASIA_MALIGNA` | Indicador/status de outra neoplasia maligna. |
| `ST_CELULA_ENDOMETRIAL_PRESENTE` | Indicador/status de celula endometrial presente. |
| `CO_INTERVALO_COLETA` | Intervalo entre etapas de coleta. |
| `CO_INTERVALO_EXAME` | Intervalo ate a realizacao do exame. |
| `CO_TEMPO_EXAME` | Faixa/codigo do tempo ate a realizacao do exame. |
| `ST_REPRESENTATI_ZONA_TRANSFORM` | Indicador/status de representatividade zona transformacao. |
| `ST_SCREENING_REALIZADO` | Indicador/status de screening realizado. |
| `TP_MOTIVO_EXAME` | Motivo declarado para o exame. |
| `CO_PACIENTE` | Identificador anonimizado de paciente. |
| `NU_AMOSTRA_REJEITADA` | Numero, valor ou indicador de amostra rejeitada. |
| `CO_REJ_AUSENCIA` | Codigo de rejeicao ausencia. |
| `CO_REJ_LAMINA` | Codigo de rejeicao lamina. |
| `CO_REJ_CAUSA_ALHEIA` | Codigo de rejeicao causa alheia. |
| `CO_REJ_OUT_CAUSAS` | Codigo de rejeicao out causas. |
| `NU_AMOSTRA_SATISFATORIA` | Numero, valor ou indicador de amostra satisfatoria. |
| `CO_INS_MAT_CELULAR` | Codigo de insatisfatoriedade material celular. |
| `CO_INS_SANGUE` | Codigo de insatisfatoriedade sangue. |
| `CO_INS_PIOCITOS` | Codigo de insatisfatoriedade piocitos. |
| `CO_INS_ARTEF_DES` | Codigo de insatisfatoriedade artefatos dessecamento. |
| `CO_INS_CONTAM_EXTERNOS` | Codigo de insatisfatoriedade contaminantes externos. |
| `CO_INS_INTENSA_SUPER` | Codigo de insatisfatoriedade intensa superposicao. |
| `CO_INS_OUTROS` | Codigo de insatisfatoriedade outros. |
| `CO_ALT_CEL_INFLAMACAO` | Codigo de alteracao celula inflamacao. |
| `CO_ALT_CEL_METAPLASIA` | Codigo de alteracao celula metaplasia. |
| `CO_ALT_CEL_REPARACAO` | Codigo de alteracao celula reparacao. |
| `CO_ALT_CEL_ATROFIA` | Codigo de alteracao celula atrofia. |
| `CO_ALT_CEL_RADIACAO` | Codigo de alteracao celula radiacao. |
| `CO_ALT_CEL_OUT` | Codigo de alteracao celula out. |
| `CO_MIC_LACTOBACILLUS` | Codigo de micro lactobacillus. |
| `CO_MIC_COCOS` | Codigo de micro cocos. |
| `CO_MIC_SUGEST_CHLAMYDIA` | Codigo de micro sugestivo chlamydia. |
| `CO_MIC_ACTINOMYCES` | Codigo de micro actinomyces. |
| `CO_MIC_CANDIDA` | Codigo de micro candida. |
| `CO_MIC_TRICHOMONAS` | Codigo de micro trichomonas. |
| `CO_MIC_EFEITO_CITOPATICO` | Codigo de micro efeito citopatico. |
| `CO_MIC_BACILOS_SUPRA` | Codigo de micro bacilos supracitoplasmaticos. |
| `CO_MIC_OUTROS_BACILOS` | Codigo de micro outros bacilos. |
| `CO_MIC_OUTROS` | Codigo de micro outros. |
| `CO_EPIT_ESCAMOSO` | Codigo de epitelio escamoso. |
| `CO_EPIT_GLANDULAR` | Codigo de epitelio glandular. |
| `CO_EPIT_METAPLAS` | Codigo de epitelio metaplasico. |
| `NU_CA_ESCAMOSA_P_NAO_NEOPLAST` | Numero, valor ou indicador de celulas alteradas escamosa papilifera nao neoplastica. |
| `NU_CA_ESCAMOSA_N_AF_LESAO_AG` | Numero, valor ou indicador de celulas alteradas escamosa n a favor lesao alto grau. |
| `NU_CA_GLANDULAR_NAO_NEOPL` | Numero, valor ou indicador de celulas alteradas glandular nao neopl. |
| `NU_CA_GLANDULA_N_AF_LESAO_AG` | Numero, valor ou indicador de celulas alteradas glandula n a favor lesao alto grau. |
| `NU_CA_ORIGEM_IND_NAO_NEOPLAST` | Numero, valor ou indicador de celulas alteradas origem indeterminado nao neoplastica. |
| `NU_CA_IND_NAO_LESAO` | Numero, valor ou indicador de celulas alteradas indeterminado nao lesao. |
| `NU_LESAO_IE_BAIXO_GRAU` | Numero, valor ou indicador de lesao ie baixo grau. |
| `NU_LESAO_IE_ALTO_GRAU` | Numero, valor ou indicador de lesao ie alto grau. |
| `NU_LES_IE_ALTO_GRAU_N_MIC_INV` | Numero, valor ou indicador de lesao ie alto grau n micro invasor. |
| `NU_CARC_EPIDERM_INV` | Numero, valor ou indicador de carcinoma epidermoide invasor. |
| `NU_ADENOCAR_INS_SITU` | Numero, valor ou indicador de adenocarcinoma insatisfatoriedade in situ. |
| `NU_ADENOCAR_INVASOR` | Numero, valor ou indicador de adenocarcinoma invasor. |
| `NU_OUTRAS_NEOPLASIAS` | Numero, valor ou indicador de outras neoplasias. |
| `NU_LIMITE_NORMALIDADE` | Numero, valor ou indicador de limite normalidade. |
| `TP_CEL_ESCAM_SIGN_INDETER` | Tipo ou classificacao de celula escam significado indeter. |
| `TP_CEL_GLAND_SIGNIF_INDET` | Tipo ou classificacao de celula gland signif indeterminado. |
| `TP_INSPECAO_COLO` | Resultado/classificacao da inspecao do colo. |
| `CO_ANO_RESULTADO` | Ano do resultado do exame. |
| `CO_ANO_MES_RESULTADO` | Ano e mes do resultado do exame. |
| `CO_LAUDO_CITOPATOLOGICO` | Codigo do laudo citopatologico. |
| `IDADE` | Idade da pessoa atendida. |
| `SG_SEXO` | Sexo da pessoa atendida. |

</details>

<details>
<summary><code>cito_mama</code> - 50 colunas</summary>

| Coluna | O que representa |
| --- | --- |
| `CO_SEQ_SISCAN_CITO_MAMA_RESID` | Identificador sequencial do registro de citopatologico de mama, por residencia. |
| `CO_UF_RESIDENCIA` | Codigo da UF de residencia da pessoa atendida. |
| `CO_MUN_RESIDENCIA` | Codigo IBGE do municipio de residencia da pessoa atendida. |
| `NU_ANO_COMPETENCIA` | Ano de competencia do registro. |
| `NU_ANO_MES_COMPETENCIA` | Ano e mes de competencia do registro. |
| `CO_RACA_COR` | Codigo de raca/cor da pessoa atendida. |
| `SG_SEXO` | Sexo da pessoa atendida. |
| `CO_FAIXA_ETARIA_PACIENTE` | Codigo da faixa etaria da pessoa atendida. |
| `CO_ESCOLARIDADE` | Codigo de escolaridade. |
| `CO_INTERVALO_COLETA` | Intervalo entre etapas de coleta. |
| `CO_INTERVALO_EXAME` | Intervalo ate a realizacao do exame. |
| `CO_TEMPO_EXAME` | Faixa/codigo do tempo ate a realizacao do exame. |
| `CO_RISCO_ELEVADO` | Codigo de risco elevado para cancer de mama. |
| `TP_DESCARGA_PAPILAR` | Classificacao de descarga papilar. |
| `TP_NODULO` | Classificacao sobre presenca/caracteristica de nodulo. |
| `TP_LATERALIDADE_MAMA` | Lateralidade da mama avaliada. |
| `TP_MATERIAL` | Tipo de material coletado. |
| `TP_ADEQUABILIDAD_MATERIAL` | Classificacao da adequabilidade do material coletado. |
| `TP_RESULTA_PUNCAO_ASPIRATIVA` | Resultado da puncao aspirativa. |
| `NU_PAAF_B_MASTITE` | Numero, valor ou indicador de PAAF b mastite. |
| `NU_PAAF_B_ABC_SUBARE` | Numero, valor ou indicador de PAAF b abscesso subareolar. |
| `NU_PAAF_B_FIBROAD` | Numero, valor ou indicador de PAAF b fibroadenoma. |
| `NU_PAAF_B_NECR_GORDUR` | Numero, valor ou indicador de PAAF b necrose gordur. |
| `NU_PAAF_B_COM_FIB_MAM` | Numero, valor ou indicador de PAAF b com fib mam. |
| `NU_PAAF_B_L_E_P` | Numero, valor ou indicador de PAAF b lesao epitelial papilifera. |
| `NU_PAAF_B_OUTRAS` | Numero, valor ou indicador de PAAF b outras. |
| `NU_PAAF_M_IND_TUMPA` | Numero, valor ou indicador de PAAF m indeterminado tumor palpavel. |
| `NU_PAAF_M_IND_TUMF` | Numero, valor ou indicador de PAAF m indeterminado tumor fixo. |
| `NU_PAAF_M_IND_OUTROS` | Numero, valor ou indicador de PAAF m indeterminado outros. |
| `NU_PAAF_SUS_L_E_P` | Numero, valor ou indicador de PAAF suspeito lesao epitelial papilifera. |
| `NU_PAAF_SUSM_OUTROS` | Numero, valor ou indicador de PAAF suspeito malignidade outros. |
| `NU_PAAF_P_M_CARC_DUC` | Numero, valor ou indicador de PAAF papilifera m carcinoma ductal. |
| `NU_PAAF_P_M_CARC_LOB` | Numero, valor ou indicador de PAAF papilifera m carcinoma lobular. |
| `NU_PAAF_P_M_OUTROS` | Numero, valor ou indicador de PAAF papilifera m outros. |
| `NU_QDESC_MAT_ACELULAR` | Numero, valor ou indicador de qualidade/descricao material acelular. |
| `NU_QDESC_NEG_MALIG` | Numero, valor ou indicador de qualidade/descricao negativo malignidade. |
| `NU_QDESC_MALIG_INDT` | Numero, valor ou indicador de qualidade/descricao malignidade indt. |
| `NU_QDESC_POS_MALIG` | Numero, valor ou indicador de qualidade/descricao pos malignidade. |
| `NU_QDESC_LES_PAPIL` | Numero, valor ou indicador de qualidade/descricao lesao papil. |
| `NU_QDESC_PROC_INFL` | Numero, valor ou indicador de qualidade/descricao procedimento inflamatorio. |
| `QT_EXAME` | Quantidade de exames agregados no registro. |
| `TP_PROC_BENI_NEGA_MALI_COMPATI` | Tipo ou classificacao de procedimento beni nega mali compati. |
| `TP_PADR_CITO_MALIG_INDET` | Tipo ou classificacao de padrao citologia malignidade indeterminado. |
| `TP_PADR_CITO_SUSP_MALIG` | Tipo ou classificacao de padrao citologia suspeito malignidade. |
| `TP_PADR_CITO_POSI_MALIG` | Tipo ou classificacao de padrao citologia posi malignidade. |
| `TP_PADRAO_CITOPATOL_AMOST` | Tipo ou classificacao de padrao citopatologico amostra. |
| `CO_TEM_NODULO` | Codigo indicador de presenca de nodulo. |
| `CO_ANO_RESULTADO` | Ano do resultado do exame. |
| `CO_ANO_MES_RESULTADO` | Ano e mes do resultado do exame. |
| `SG_UF_RESIDENCIA` | Sigla da UF de residencia da pessoa atendida. |

</details>

<details>
<summary><code>cito_mama_pacnt</code> - 29 colunas</summary>

| Coluna | O que representa |
| --- | --- |
| `CO_SEQ_SISCAN_CITO_MAMA_PACNT` | Identificador sequencial do registro de citopatologico de mama, por paciente. |
| `CO_UF_RESIDENCIA` | Codigo da UF de residencia da pessoa atendida. |
| `CO_MUN_RESIDENCIA` | Codigo IBGE do municipio de residencia da pessoa atendida. |
| `NU_ANO_COMPETENCIA` | Ano de competencia do registro. |
| `NU_ANO_MES_COMPETENCIA` | Ano e mes de competencia do registro. |
| `CO_RACA_COR` | Codigo de raca/cor da pessoa atendida. |
| `SG_SEXO` | Sexo da pessoa atendida. |
| `CO_FAIXA_ETARIA_PACIENTE` | Codigo da faixa etaria da pessoa atendida. |
| `CO_ESCOLARIDADE` | Codigo de escolaridade. |
| `CO_INTERVALO_COLETA` | Intervalo entre etapas de coleta. |
| `CO_INTERVALO_EXAME` | Intervalo ate a realizacao do exame. |
| `CO_TEMPO_EXAME` | Faixa/codigo do tempo ate a realizacao do exame. |
| `CO_RISCO_ELEVADO` | Codigo de risco elevado para cancer de mama. |
| `TP_DESCARGA_PAPILAR` | Classificacao de descarga papilar. |
| `TP_NODULO` | Classificacao sobre presenca/caracteristica de nodulo. |
| `TP_LATERALIDADE_MAMA` | Lateralidade da mama avaliada. |
| `TP_MATERIAL` | Tipo de material coletado. |
| `TP_ADEQUABILIDAD_MATERIAL` | Classificacao da adequabilidade do material coletado. |
| `TP_RESULTA_PUNCAO_ASPIRATIVA` | Resultado da puncao aspirativa. |
| `TP_PROC_BENI_NEGA_MALI_COMPATI` | Tipo ou classificacao de procedimento beni nega mali compati. |
| `TP_PADR_CITO_MALIG_INDET` | Tipo ou classificacao de padrao citologia malignidade indeterminado. |
| `TP_PADR_CITO_SUSP_MALIG` | Tipo ou classificacao de padrao citologia suspeito malignidade. |
| `TP_PADR_CITO_POSI_MALIG` | Tipo ou classificacao de padrao citologia posi malignidade. |
| `TP_PADRAO_CITOPATOL_AMOST` | Tipo ou classificacao de padrao citopatologico amostra. |
| `CO_PACIENTE` | Identificador anonimizado de paciente. |
| `TP_LAUDO_CITOP` | Tipo/codigo do laudo citopatologico. |
| `CO_TEM_NODULO` | Codigo indicador de presenca de nodulo. |
| `CO_ANO_RESULTADO` | Ano do resultado do exame. |
| `SG_UF_RESIDENCIA` | Sigla da UF de residencia da pessoa atendida. |

</details>

<details>
<summary><code>histo_colo</code> - 59 colunas</summary>

| Coluna | O que representa |
| --- | --- |
| `CO_SEQ_SISCAN_HISTO_COLO_RESID` | Identificador sequencial do registro histopatologico de colo, por residencia. |
| `CO_UF_RESIDENCIA` | Codigo da UF de residencia da pessoa atendida. |
| `CO_MUN_RESIDENCIA` | Codigo IBGE do municipio de residencia da pessoa atendida. |
| `CO_ANO_COMPETENCIA` | Ano de competencia do registro. |
| `CO_ANO_MES_COMPETENCIA` | Ano e mes de competencia do registro. |
| `CO_RACA_COR` | Codigo de raca/cor da pessoa atendida. |
| `CO_FAIXA_ETARIA` | Codigo da faixa etaria. |
| `CO_ESCOLARIDADE` | Codigo de escolaridade. |
| `TP_ENCAMINHAMENTO` | Tipo de encaminhamento. |
| `TP_PROCEDIMENTO` | Tipo de procedimento realizado. |
| `TP_ACHADO_COLPOSCOPICO` | Tipo de achado colposcopico. |
| `TP_GRAU_DIFERENCIACAO` | Grau de diferenciacao histologica. |
| `TP_MARGEM_CIRURGICA` | Situacao/classificacao da margem cirurgica. |
| `TP_ATIPIA_CELULAR_ESCAMOS` | Tipo ou classificacao de atipia celular escamosa. |
| `TP_ATIPIA_CELULAR_GLANDUL` | Tipo ou classificacao de atipia celular glandular. |
| `TP_CEL_ORIG_INF_SIGN_INDE` | Tipo ou classificacao de celula origem informacao significado indeterminado. |
| `ST_OUTRA_NEOPLASIA_MALIGNA` | Indicador/status de outra neoplasia maligna. |
| `TP_AVALIACAO_AMOSTRA` | Classificacao da avaliacao da amostra. |
| `CO_INTERVALO_COLETA` | Intervalo entre etapas de coleta. |
| `CO_INTERVALO_EXAME` | Intervalo ate a realizacao do exame. |
| `CO_TEMPO_EXAME` | Faixa/codigo do tempo ate a realizacao do exame. |
| `NU_AC_ANORMAL_C_ALT_MENOR` | Numero, valor ou indicador de achado colposcopico anormal c alteracao menor. |
| `NU_AC_ANORMAL_C_ALT_MAIOR` | Numero, valor ou indicador de achado colposcopico anormal c alteracao maior. |
| `NU_AC_ANORMAL_C_SUGEST_CANCER` | Numero, valor ou indicador de achado colposcopico anormal c sugestivo cancer. |
| `NU_AC_ANORMAL_C_MISCELANIA` | Numero, valor ou indicador de achado colposcopico anormal c miscelanea. |
| `NU_ZT_SATIF_TP_I` | Numero, valor ou indicador de zona de transformacao satisfatoria tipo i. |
| `NU_ZT_SATIF_TP_II` | Numero, valor ou indicador de zona de transformacao satisfatoria tipo II. |
| `NU_ZT_SATIF_TP_III` | Numero, valor ou indicador de zona de transformacao satisfatoria tipo III. |
| `NU_ZT_SATIF_IND` | Numero, valor ou indicador de zona de transformacao satisfatoria indeterminado. |
| `NU_PROC_BIOPSIA` | Numero, valor ou indicador de procedimento biopsia. |
| `NU_PROC_EXERESE_VER_E_TRATAR` | Numero, valor ou indicador de procedimento exerese ver epitelial tratar. |
| `NU_PROC_EXERESE_POS_BIOPSIA` | Numero, valor ou indicador de procedimento exerese pos biopsia. |
| `NU_PROC_EXERESE_CONIZACAO` | Numero, valor ou indicador de procedimento exerese conizacao. |
| `NU_PROC_EXERESE_OUTROS` | Numero, valor ou indicador de procedimento exerese outros. |
| `NU_LES_BEN_METAPLASIA_ESC` | Numero, valor ou indicador de lesao benigna metaplasia esc. |
| `NU_LES_BEN_POLIPO_ENDOCERVICAL` | Numero, valor ou indicador de lesao benigna polipo endocervical. |
| `NU_LES_BEN_CERVICITE_CRON` | Numero, valor ou indicador de lesao benigna cervicite cronica. |
| `NU_LES_BEN_ALTO_CITO_COMPA` | Numero, valor ou indicador de lesao benigna alto citologia compativel. |
| `NU_NEOPLASICO_NIC_I` | Numero, valor ou indicador de neoplasico NIC i. |
| `NU_NEOPLASICO_NIC_II` | Numero, valor ou indicador de neoplasico NIC II. |
| `NU_NEOPLASICO_NIC_III` | Numero, valor ou indicador de neoplasico NIC III. |
| `NU_NEO_CARC_EPID_MICRO_INVASIV` | Numero, valor ou indicador de neo carcinoma epid micro invasivo. |
| `NU_NEO_CARC_EPID_INVASIVO` | Numero, valor ou indicador de neo carcinoma epid invasivo. |
| `NU_NEO_CARC_EPID_IMPOSSIVEL` | Numero, valor ou indicador de neo carcinoma epid impossivel. |
| `NU_NEO_ADENO_IN_SITU` | Numero, valor ou indicador de neo adenocarcinoma in in situ. |
| `NU_NEO_ADENO_INVASOR` | Numero, valor ou indicador de neo adenocarcinoma invasor. |
| `NU_OUTRAS_NEOPL_MALIG` | Numero, valor ou indicador de outras neopl malignidade. |
| `TP_ZONA_TRANSF_ADEQUABILIDADE` | Adequabilidade da zona de transformacao. |
| `TP_LESAO_CARAT_NEOP_PREN_AD` | Caracterizacao de lesao neoplasica/pre-neoplasica glandular. |
| `NU_RES_EXAMES_NEO_PRENEO` | Numero, valor ou indicador de resultado exames neo pre-neoplasico. |
| `TP_LESAO_CARAT_NEOP_PRENEO` | Caracterizacao de lesao neoplasica/pre-neoplasica. |
| `TP_CEL_ESCAM_SIGN_INDETER` | Tipo ou classificacao de celula escam significado indeter. |
| `TP_CEL_GLAND_SIGNIF_INDET` | Tipo ou classificacao de celula gland signif indeterminado. |
| `CO_ANO_RESULTADO` | Ano do resultado do exame. |
| `CO_ANO_MES_RESULTADO` | Ano e mes do resultado do exame. |
| `TP_PROCEDIMENTO_CIR` | Tipo de procedimento cirurgico. |
| `CO_RES_NEOPL_OUTRAS` | Codigo de resultado neopl outras. |
| `SG_UF_RESIDENCIA` | Sigla da UF de residencia da pessoa atendida. |
| `SG_SEXO` | Sexo da pessoa atendida. |

</details>

<details>
<summary><code>histo_colo_pacnt</code> - 32 colunas</summary>

| Coluna | O que representa |
| --- | --- |
| `CO_SEQ_SISCAN_HISTO_COLO_PACNT` | Identificador sequencial do registro histopatologico de colo, por paciente. |
| `CO_UF_RESIDENCIA` | Codigo da UF de residencia da pessoa atendida. |
| `CO_MUN_RESIDENCIA` | Codigo IBGE do municipio de residencia da pessoa atendida. |
| `NU_ANO_COMPETENCIA` | Ano de competencia do registro. |
| `NU_ANO_MES_COMPETENCIA` | Ano e mes de competencia do registro. |
| `CO_RACA_COR` | Codigo de raca/cor da pessoa atendida. |
| `CO_IDADE_PACIENTE` | Idade da pessoa atendida. |
| `CO_ESCOLARIDADE` | Codigo de escolaridade. |
| `TP_ENCAMINHAMENTO` | Tipo de encaminhamento. |
| `TP_PROCEDIMENTO` | Tipo de procedimento realizado. |
| `TP_ACHADO_COLPOSCOPICO` | Tipo de achado colposcopico. |
| `TP_GRAU_DIFERENCIACAO` | Grau de diferenciacao histologica. |
| `TP_MARGEM_CIRURGICA` | Situacao/classificacao da margem cirurgica. |
| `TP_ATIPIA_CELULAR_ESCAMOS` | Tipo ou classificacao de atipia celular escamosa. |
| `TP_ATIPIA_CELULAR_GLANDUL` | Tipo ou classificacao de atipia celular glandular. |
| `TP_CEL_ORIG_INF_SIGN_INDE` | Tipo ou classificacao de celula origem informacao significado indeterminado. |
| `ST_OUTRA_NEOPLASIA_MALIGNA` | Indicador/status de outra neoplasia maligna. |
| `TP_AVALIACAO_AMOSTRA` | Classificacao da avaliacao da amostra. |
| `CO_INTERVALO_COLETA` | Intervalo entre etapas de coleta. |
| `CO_INTERVALO_EXAME` | Intervalo ate a realizacao do exame. |
| `CO_TEMPO_EXAME` | Faixa/codigo do tempo ate a realizacao do exame. |
| `TP_ZONA_TRANSF_ADEQUABILIDADE` | Adequabilidade da zona de transformacao. |
| `TP_LESAO_CARAT_NEOP_PREN_AD` | Caracterizacao de lesao neoplasica/pre-neoplasica glandular. |
| `TP_LESAO_CARAT_NEOP_PRENEO` | Caracterizacao de lesao neoplasica/pre-neoplasica. |
| `TP_CEL_ESCAM_SIGN_INDETER` | Tipo ou classificacao de celula escam significado indeter. |
| `TP_CEL_GLAND_SIGNIF_INDET` | Tipo ou classificacao de celula gland signif indeterminado. |
| `CO_PACIENTE` | Identificador anonimizado de paciente. |
| `NU_ANO_RESULTADO` | Ano do resultado do exame. |
| `CO_ANO_MES_RESULTADO` | Ano e mes do resultado do exame. |
| `NU_LAUDO_HISTOP` | Codigo/numero do laudo histopatologico. |
| `SG_UF_RESIDENCIA` | Sigla da UF de residencia da pessoa atendida. |
| `SG_SEXO` | Sexo da pessoa atendida. |

</details>

<details>
<summary><code>histo_mama</code> - 46 colunas</summary>

| Coluna | O que representa |
| --- | --- |
| `CO_SEQ_SISCAN_HISTO_MAMA_RESID` | Identificador sequencial do registro histopatologico de mama, por residencia. |
| `CO_UF_RESIDENCIA` | Codigo da UF de residencia da pessoa atendida. |
| `CO_MUN_RESIDENCIA` | Codigo IBGE do municipio de residencia da pessoa atendida. |
| `NU_ANO_COMPETENCIA` | Ano de competencia do registro. |
| `NU_ANO_MES_COMPETENCIA` | Ano e mes de competencia do registro. |
| `CO_RACA_COR` | Codigo de raca/cor da pessoa atendida. |
| `CO_IDADE_PACIENTE` | Idade da pessoa atendida. |
| `CO_ESCOLARIDADE` | Codigo de escolaridade. |
| `CO_INTERVALO_COLETA` | Intervalo entre etapas de coleta. |
| `CO_INTERVALO_EXAME` | Intervalo ate a realizacao do exame. |
| `CO_TEMPO_EXAME` | Faixa/codigo do tempo ate a realizacao do exame. |
| `TP_RISCO_ELEVADO` | Tipo/indicador de risco elevado para cancer de mama. |
| `TP_EXAME_HISTOPATOLOGICO` | Tipo de exame histopatologico. |
| `TP_DETECCAO_LESAO` | Forma de deteccao da lesao. |
| `TP_LATERALIDADE_LESAO` | Lateralidade da lesao avaliada. |
| `TP_TAMANHO_LESAO` | Classificacao do tamanho da lesao. |
| `TP_LINFONODO_AXILAR_PALPAVEL` | Tipo ou classificacao de linfonodo axilar palpavel. |
| `TP_MATER_ENVIA_PROCEDENTE` | Tipo/origem do material enviado. |
| `TP_PROCEDIMENTO_CIRURGICO` | Tipo de procedimento cirurgico. |
| `TP_ADEQUABILIDAD_MATERIAL` | Classificacao da adequabilidade do material coletado. |
| `ST_MICROCALCIFICACAO` | Indicador/status de microcalcificacao. |
| `TP_LESAO` | Tipo de lesao. |
| `TP_LESAO_CARAT_NEOPL_MALI` | Caracterizacao da lesao como neoplasica maligna. |
| `TP_GRAU_HISTOLOGICO` | Grau histologico. |
| `TP_MARGEM_CIRURGICA` | Situacao/classificacao da margem cirurgica. |
| `NU_HIPERPLAS_DUCTAL_SEM_ATIP` | Numero, valor ou indicador de hiperplasia ductal sem atipia. |
| `NU_HIPERPLAS_DUCTAL_COM_ATIP` | Numero, valor ou indicador de hiperplasia ductal com atipia. |
| `NU_HIPERPLAS_LOBULAR_COM_ATIP` | Numero, valor ou indicador de hiperplasia lobular com atipia. |
| `NU_ADENOSE_SOE` | Numero, valor ou indicador de adenose SOE. |
| `NU_LESAO_ESCLEROSANTE_RADIAL` | Numero, valor ou indicador de lesao esclerosante radial. |
| `NU_CONDICAO_FIBROCISTICA` | Numero, valor ou indicador de condicao fibrocistica. |
| `NU_FIBROADENOMA` | Numero, valor ou indicador de fibroadenoma. |
| `NU_PAPILOMA_SOLITARIO` | Numero, valor ou indicador de papiloma solitario. |
| `NU_PAPILOMA_MULTIPLO` | Numero, valor ou indicador de papiloma multiplo. |
| `NU_PAPILOMATOSE_FLORIDA_DO_MAM` | Numero, valor ou indicador de papilomatose florida do mam. |
| `NU_MASTITE` | Numero, valor ou indicador de mastite. |
| `NU_OUTROS` | Numero, valor ou indicador de outros. |
| `SG_SEXO` | Sexo da pessoa atendida. |
| `CO_ANO_RESULTADO` | Ano do resultado do exame. |
| `CO_ANO_MES_RESULTADO` | Ano e mes do resultado do exame. |
| `TP_DIAGNOSTICO_IMAGEM` | Tipo/classificacao do diagnostico por imagem. |
| `TP_RECEPTOR_HORMONAL_ESTROG` | Resultado/classificacao do receptor hormonal de estrogenio. |
| `TP_RECEPTOR_HORMONAL_PROGES` | Resultado/classificacao do receptor hormonal de progesterona. |
| `ST_OUTRO_ESTUDO_IMUNOLO_HISTOQ` | Indicador/status de outro estudo imuno histoquimico. |
| `TP_TAMANHO_TUMOR` | Classificacao do tamanho do tumor. |
| `SG_UF_RESIDENCIA` | Sigla da UF de residencia da pessoa atendida. |

</details>

<details>
<summary><code>histo_mama_pacnt</code> - 32 colunas</summary>

| Coluna | O que representa |
| --- | --- |
| `CO_SEQ_SISCAN_HISTO_MAMA_PACNT` | Identificador sequencial do registro histopatologico de mama, por paciente. |
| `CO_UF_RESIDENCIA` | Codigo da UF de residencia da pessoa atendida. |
| `CO_MUN_RESIDENCIA` | Codigo IBGE do municipio de residencia da pessoa atendida. |
| `NU_ANO_COMPETENCIA` | Ano de competencia do registro. |
| `NU_ANO_MES_COMPETENCIA` | Ano e mes de competencia do registro. |
| `CO_RACA_COR` | Codigo de raca/cor da pessoa atendida. |
| `CO_IDADE_PACIENTE` | Idade da pessoa atendida. |
| `CO_ESCOLARIDADE` | Codigo de escolaridade. |
| `CO_INTERVALO_COLETA` | Intervalo entre etapas de coleta. |
| `CO_INTERVALO_EXAME` | Intervalo ate a realizacao do exame. |
| `CO_TEMPO_EXAME` | Faixa/codigo do tempo ate a realizacao do exame. |
| `TP_RISCO_ELEVADO` | Tipo/indicador de risco elevado para cancer de mama. |
| `TP_EXAME_HISTOPATOLOGICO` | Tipo de exame histopatologico. |
| `TP_DETECCAO_LESAO` | Forma de deteccao da lesao. |
| `TP_LATERALIDADE_LESAO` | Lateralidade da lesao avaliada. |
| `TP_TAMANHO_LESAO` | Classificacao do tamanho da lesao. |
| `TP_LINFONODO_AXILAR_PALPAVEL` | Tipo ou classificacao de linfonodo axilar palpavel. |
| `TP_MATER_ENVIA_PROCEDENTE` | Tipo/origem do material enviado. |
| `TP_PROCEDIMENTO_CIRURGICO` | Tipo de procedimento cirurgico. |
| `TP_ADEQUABILIDAD_MATERIAL` | Classificacao da adequabilidade do material coletado. |
| `ST_MICROCALCIFICACAO` | Indicador/status de microcalcificacao. |
| `TP_LESAO` | Tipo de lesao. |
| `TP_LESAO_CARAT_NEOPL_MALI` | Caracterizacao da lesao como neoplasica maligna. |
| `TP_GRAU_HISTOLOGICO` | Grau histologico. |
| `TP_MARGEM_CIRURGICA` | Situacao/classificacao da margem cirurgica. |
| `CO_PACIENTE` | Identificador anonimizado de paciente. |
| `SG_SEXO` | Sexo da pessoa atendida. |
| `TP_DIAGNOSTICO_IMAGEM` | Tipo/classificacao do diagnostico por imagem. |
| `TP_TAMANHO_TUMOR` | Classificacao do tamanho do tumor. |
| `CO_ANO_RESULTADO` | Ano do resultado do exame. |
| `TP_LAUDO_HISTOPATOLOGICO` | Tipo/codigo do laudo histopatologico. |
| `SG_UF_RESIDENCIA` | Sigla da UF de residencia da pessoa atendida. |

</details>

<details>
<summary><code>mamografia</code> - 82 colunas</summary>

| Coluna | O que representa |
| --- | --- |
| `CO_SEQ_SISCAN_MAMOGRAFIA_RESID` | Identificador sequencial do registro de mamografia, por residencia. |
| `CO_UF_UNIDADE_SAUDE` | Codigo da UF da unidade de saude. |
| `CO_UF_RESIDENCIA` | Codigo da UF de residencia da pessoa atendida. |
| `CO_UF_PREST_SERVICO` | Codigo da UF do prestador de servico. |
| `CO_MUN_UNIDADE_SAUDE` | Codigo IBGE do municipio da unidade de saude. |
| `CO_MUN_RESIDENCIA` | Codigo IBGE do municipio de residencia da pessoa atendida. |
| `CO_MUN_PREST_SERVICO` | Codigo IBGE do municipio do prestador de servico. |
| `CO_UNIDADE_SAUDE` | Codigo da unidade de saude. |
| `CO_PREST_SERVICO` | Codigo do prestador de servico. |
| `NU_ANO_COMPETENCIA` | Ano de competencia do registro. |
| `NU_ANO_MES_COMPETENCIA` | Ano e mes de competencia do registro. |
| `CO_RACA_COR` | Codigo de raca/cor da pessoa atendida. |
| `CO_ETNIA` | Codigo de etnia, quando informado. |
| `CO_IDADE_PACIENTE` | Idade da pessoa atendida. |
| `CO_ESCOLARIDADE` | Codigo de escolaridade. |
| `TP_RESP_APRES_RISC_ELEV_CANCER` | Resposta sobre risco elevado para cancer de mama. |
| `TP_RESP_ANT_MAMA_EXA_PROF_SAUD` | Resposta sobre exame profissional anterior das mamas. |
| `TP_RESP_FEZ_MAMOGRA_ALGUMA_VEZ` | Resposta sobre ja ter feito mamografia anteriormente. |
| `CO_IND_CLINICA` | Codigo da indicacao clinica da mamografia. |
| `TP_MAMOGRAFIA_RASTREAMENT` | Indica se a mamografia e de rastreamento/triagem. |
| `TP_MAMA_PELE_ESQ` | Classificacao de alteracoes de pele na mama esquerda. |
| `TP_MAMA_PELE_DIR` | Classificacao de alteracoes de pele na mama direita. |
| `TP_MAMA_ESQ` | Classificacao dos achados clinicos/imagem da mama esquerda. |
| `TP_MAMA_DIR` | Classificacao dos achados clinicos/imagem da mama direita. |
| `TP_LINFONODO_ESQ` | Classificacao de linfonodo axilar do lado esquerdo. |
| `TP_LINFONODO_DIR` | Classificacao de linfonodo axilar do lado direito. |
| `TP_RECOMENDACAO_ESQUERDA` | Recomendacao para a mama esquerda. |
| `TP_RECOMENDACAO_DIREITA` | Recomendacao para a mama direita. |
| `CO_RECOMENDACAO` | Codigo da recomendacao final associada ao exame. |
| `NU_CONTROLE_CATEGORIA3` | Indicador/quantidade de controle de achado BI-RADS categoria 3. |
| `NU_LES_DIAG_CANCER` | Indicador/quantidade de lesao com diagnostico de cancer. |
| `NU_DIAG_AVAL_QT` | Indicador/quantidade relacionada a avaliacao diagnostica. |
| `NU_REV_MAMOGRAFIA` | Indicador/quantidade de revisao de mamografia. |
| `NU_LES_BIOSPIA_PAAF` | Indicador/quantidade de lesao encaminhada a biopsia/PAAF. |
| `NU_NAO_FEZ_CIRURGIAS` | Numero, valor ou indicador de nao fez cirurgias. |
| `NU_FEZ_CIRURGIA_ESQ` | Numero, valor ou indicador de fez cirurgia esquerda. |
| `NU_FEZ_CIRURGIA_DIR` | Numero, valor ou indicador de fez cirurgia direita. |
| `NU_NODULO_DENS_GORD_ME` | Indicador/quantidade de nodulo de densidade gordurosa na mama esquerda. |
| `NU_NODULO_CALCIFIC_ME` | Indicador/quantidade de nodulo calcificado na mama esquerda. |
| `NU_NODULO_DEN_HETEROG_ME` | Indicador/quantidade de nodulo de densidade heterogenea na mama esquerda. |
| `NU_CALC_VASCULARES_ME` | Indicador/quantidade de calcificacoes vasculares na mama esquerda. |
| `NU_CALC_TIPICA_BENIG_ME` | Indicador/quantidade de calcificacao tipicamente benigna na mama esquerda. |
| `NU_LINFON_INTRAMAM_ME` | Indicador/quantidade de linfonodo intramamario na mama esquerda. |
| `NU_DIS_ARQ_POR_CIR_ME` | Indicador/quantidade de distorcao arquitetural por cirurgia na mama esquerda. |
| `NU_IMPLANT_SEM_SIN_RUPTU_ME` | Indicador/quantidade de implante sem sinal de ruptura na mama esquerda. |
| `NU_IMP_COM_SIN_RUPTU_ME` | Indicador/quantidade de implante com sinal de ruptura na mama esquerda. |
| `NU_CISTO_OLEOSO_ME` | Indicador/quantidade de cisto oleoso na mama esquerda. |
| `NU_GINECOMASTIA_ME` | Indicador/quantidade de ginecomastia na mama esquerda. |
| `NU_ECTASIA_DUCTAL_ME` | Indicador/quantidade de ectasia ductal na mama esquerda. |
| `NU_NODULO_DENS_GORD_MD` | Indicador/quantidade de nodulo de densidade gordurosa na mama direita. |
| `NU_NODULO_CALCIFIC_MD` | Indicador/quantidade de nodulo calcificado na mama direita. |
| `NU_NODULO_DEN_HETEROG_MD` | Indicador/quantidade de nodulo de densidade heterogenea na mama direita. |
| `NU_CALC_VASCULARES_MD` | Indicador/quantidade de calcificacoes vasculares na mama direita. |
| `NU_CALC_TIPICA_BENIG_MD` | Indicador/quantidade de calcificacao tipicamente benigna na mama direita. |
| `NU_LINFON_INTRAMAM_MD` | Indicador/quantidade de linfonodo intramamario na mama direita. |
| `NU_DIS_ARQ_POR_CIR_MD` | Indicador/quantidade de distorcao arquitetural por cirurgia na mama direita. |
| `NU_IMPLANT_SEM_SIN_RUPTU_MD` | Indicador/quantidade de implante sem sinal de ruptura na mama direita. |
| `NU_IMP_COM_SIN_RUPTU_MD` | Indicador/quantidade de implante com sinal de ruptura na mama direita. |
| `NU_CISTO_OLEOSO_MD` | Indicador/quantidade de cisto oleoso na mama direita. |
| `NU_GINECOMASTIA_MD` | Indicador/quantidade de ginecomastia na mama direita. |
| `NU_ECTASIA_DUCTAL_MD` | Indicador/quantidade de ectasia ductal na mama direita. |
| `SG_SEXO` | Sexo da pessoa atendida. |
| `CO_TEMPO_EXAME` | Faixa/codigo do tempo ate a realizacao do exame. |
| `CO_INTERVALO_RESULTADO` | Intervalo ate a liberacao/registro do resultado. |
| `CO_INTERVALO_SOLICITACAO` | Intervalo relacionado a solicitacao do exame. |
| `CO_TAMANHO_NOD_ESQ` | Codigo do tamanho do nodulo na mama esquerda. |
| `CO_TAMANHO_NOD_DIR` | Codigo do tamanho do nodulo na mama direita. |
| `NU_DIAG_ACHADOS` | Indicador/quantidade de achados diagnosticos. |
| `CO_TEMPO_MAMO_ANTERIOR` | Tempo desde a mamografia anterior. |
| `CO_BIRADS` | Categoria BI-RADS informada na mamografia. |
| `NU_TAMANHO_NODULO` | Tamanho do nodulo informado no exame. |
| `ST_ASSIMETRIA_FOCAL` | Indicador/status de assimetria focal. |
| `ST_ASSIMETRIA_DIFUSA` | Indicador/status de assimetria difusa. |
| `ST_DISTORCAO_FOCAL` | Indicador/status de distorcao focal. |
| `ST_AREA_DENSA` | Indicador/status de area densa. |
| `ST_ACHADO_BENIGNO` | Indicador/status de achado benigno. |
| `ST_TEM_NODULO` | Indicador de presenca de nodulo. |
| `TP_NODULO_CAROCO_MAMA` | Tipo/caracteristica de nodulo ou caroco na mama. |
| `ST_TEM_MICROCALCIFICACAO` | Indicador de presenca de microcalcificacao. |
| `CO_ANO_RESULTADO` | Ano do resultado do exame. |
| `CO_ANO_MES_RESULTADO` | Ano e mes do resultado do exame. |
| `SG_UF_RESIDENCIA` | Sigla da UF de residencia da pessoa atendida. |

</details>

<details>
<summary><code>mamografia_pacnt</code> - 35 colunas</summary>

| Coluna | O que representa |
| --- | --- |
| `CO_SEQ_SISCAN_MAMOGRAFIA_PACNT` | Identificador sequencial do registro de mamografia, por paciente. |
| `CO_UF_RESIDENCIA` | Codigo da UF de residencia da pessoa atendida. |
| `CO_MUN_RESIDENCIA` | Codigo IBGE do municipio de residencia da pessoa atendida. |
| `NU_ANO_COMPETENCIA` | Ano de competencia do registro. |
| `NU_ANO_MES_COMPETENCIA` | Ano e mes de competencia do registro. |
| `CO_RACA_COR` | Codigo de raca/cor da pessoa atendida. |
| `CO_FAIXA_ETARIA_PACIENTE` | Codigo da faixa etaria da pessoa atendida. |
| `CO_ESCOLARIDADE` | Codigo de escolaridade. |
| `TP_RESP_APRES_RISC_ELEV_CANCER` | Resposta sobre risco elevado para cancer de mama. |
| `TP_RESP_ANT_MAMA_EXA_PROF_SAUD` | Resposta sobre exame profissional anterior das mamas. |
| `TP_RESP_FEZ_MAMOGRA_ALGUMA_VEZ` | Resposta sobre ja ter feito mamografia anteriormente. |
| `CO_IND_CLINICA` | Codigo da indicacao clinica da mamografia. |
| `TP_MAMOGRAFIA_RASTREAMENT` | Indica se a mamografia e de rastreamento/triagem. |
| `TP_MAMA_PELE_ESQ` | Classificacao de alteracoes de pele na mama esquerda. |
| `TP_MAMA_PELE_DIR` | Classificacao de alteracoes de pele na mama direita. |
| `TP_MAMA_ESQ` | Classificacao dos achados clinicos/imagem da mama esquerda. |
| `TP_MAMA_DIR` | Classificacao dos achados clinicos/imagem da mama direita. |
| `TP_LINFONODO_ESQ` | Classificacao de linfonodo axilar do lado esquerdo. |
| `TP_LINFONODO_DIR` | Classificacao de linfonodo axilar do lado direito. |
| `TP_RECOMENDACAO_ESQUERDA` | Recomendacao para a mama esquerda. |
| `TP_RECOMENDACAO_DIREITA` | Recomendacao para a mama direita. |
| `CO_RECOMENDACAO` | Codigo da recomendacao final associada ao exame. |
| `SG_SEXO` | Sexo da pessoa atendida. |
| `CO_TEMPO_EXAME` | Faixa/codigo do tempo ate a realizacao do exame. |
| `CO_INTERVALO_RESULTADO` | Intervalo ate a liberacao/registro do resultado. |
| `CO_INTERVALO_SOLICITACAO` | Intervalo relacionado a solicitacao do exame. |
| `CO_PACIENTE` | Identificador anonimizado de paciente. |
| `CO_TEMPO_MAMO_ANTERIOR` | Tempo desde a mamografia anterior. |
| `NU_TAMANHO_NODULO` | Tamanho do nodulo informado no exame. |
| `CO_ANO_RESULTADO` | Ano do resultado do exame. |
| `CO_ANO_MES_RESULTADO` | Ano e mes do resultado do exame. |
| `TP_NODULO_CAROCO_MAMA` | Tipo/caracteristica de nodulo ou caroco na mama. |
| `CO_LAUDO` | Codigo do laudo da mamografia. |
| `REQ` | Identificador/codigo de requisicao do exame. |
| `SG_UF_RESIDENCIA` | Sigla da UF de residencia da pessoa atendida. |

</details>
