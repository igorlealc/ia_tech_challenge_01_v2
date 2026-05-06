# Conversao de CSV para Parquet

Este documento descreve o script `csv_para_parquet.py`, usado para converter os CSVs baixados/filtrados do SISCAN para arquivos Parquet.

Parquet e recomendado para analises repetidas porque ocupa menos espaco, preserva schema de colunas e permite leitura mais rapida do que CSV em pandas, DuckDB, Spark e outras ferramentas analiticas.

## Instalar bibliotecas Python

Comando idempotente para instalar as bibliotecas usadas:

```bash
python3 -m venv .venv-siscan
. .venv-siscan/bin/activate
python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements.txt
```

## Conversao padrao

Por padrao, o script procura CSVs em `dados/rj_2025/` e grava Parquets em `dados/parquet/`:

```bash
python csv_para_parquet.py
```

O script tambem gera um relatorio em:

```text
dados/parquet/relatorio_conversao.json
```

## Converter um arquivo especifico

```bash
python csv_para_parquet.py dados/rj_2025/SISCAN_MAMOGRAFIA_RJ_2025.csv
```

## Converter todos os CSVs de uma pasta

```bash
python csv_para_parquet.py dados/rj_2025 --output-dir dados/parquet
```

## Converter subpastas recursivamente

```bash
python csv_para_parquet.py dados --recursive --output-dir dados/parquet
```

## Sobrescrever Parquets existentes

Por seguranca, o script ignora arquivos Parquet que ja existem. Para refazer a conversao:

```bash
python csv_para_parquet.py --overwrite
```

## Opcoes principais

| Opcao | Padrao | Descricao |
| --- | --- | --- |
| `entradas` | `dados/rj_2025` | Arquivo(s) CSV ou pasta(s) com CSVs. |
| `--output-dir` | `dados/parquet` | Pasta onde os arquivos `.parquet` serao gravados. |
| `--recursive` | desativado | Procura CSVs tambem em subpastas. |
| `--sep` | `;` | Separador do CSV. Os CSVs do SISCAN usam ponto e virgula. |
| `--encoding` | `utf-8` | Encoding de leitura do CSV. |
| `--chunksize` | `100000` | Quantidade de linhas lidas por lote. Aumente se houver memoria disponivel. |
| `--compression` | `zstd` | Compressao do Parquet: `zstd`, `snappy`, `gzip`, `brotli` ou `none`. |
| `--overwrite` | desativado | Recria Parquets existentes. |
| `--validar-existentes` | desativado | Quando um Parquet ja existe e a conversao e ignorada, le o CSV mesmo assim para validar linhas e colunas contra o Parquet existente. |
| `--infer-types` | desativado | Permite que o pandas infira tipos. Por padrao, todas as colunas sao preservadas como texto. |
| `--empty-as-null` | desativado | Interpreta campos vazios como nulos. Por padrao, campos vazios ficam como string vazia. |
| `--relatorio` | `dados/parquet/relatorio_conversao.json` | Caminho do relatorio JSON de conversao. |

## Decisoes importantes

Por padrao, o script le todas as colunas como texto. Isso e proposital para bases DATASUS, porque muitos campos sao codigos e podem ter zeros a esquerda. Use `--infer-types` apenas quando tiver certeza de que a inferencia nao vai alterar codigos.

A compressao padrao e `zstd`, que costuma gerar arquivos menores. Se alguma ferramenta nao abrir esse tipo de compressao, use:

```bash
python csv_para_parquet.py --compression snappy
```

## Validacao

Ao final da execucao, confira o relatorio JSON. Ele registra, para cada arquivo:

- CSV de origem;
- Parquet de destino;
- status da conversao;
- quantidade de linhas convertidas;
- lista de colunas;
- tamanho do CSV e do Parquet em bytes.
- bloco `integridade`, com comparacao entre CSV e Parquet.

O bloco `integridade` informa:

| Campo | Descricao |
| --- | --- |
| `status` | `ok`, `falhou` ou `nao_verificada`. |
| `arquivo_ok` | Confirma se o Parquet existe e tem tamanho maior que zero. |
| `linhas_ok` | Confirma se a quantidade de linhas do Parquet bate com a quantidade lida do CSV. |
| `colunas_ok` | Confirma se nomes e ordem das colunas do Parquet batem com o CSV. |
| `linhas_csv` | Quantidade de linhas lidas do CSV. |
| `linhas_parquet` | Quantidade de linhas registrada nos metadados do Parquet. |
| `qtd_colunas_csv` | Quantidade de colunas no CSV. |
| `qtd_colunas_parquet` | Quantidade de colunas no Parquet. |
| `colunas_csv` | Lista de colunas do CSV. |
| `colunas_parquet` | Lista de colunas do Parquet. |
| `problemas` | Lista de divergencias encontradas. Fica vazia quando `status` e `ok`. |

Para validar tambem arquivos Parquet que ja existiam antes da execucao:

```bash
python csv_para_parquet.py dados/rj_2025 --output-dir dados/parquet --validar-existentes
```
