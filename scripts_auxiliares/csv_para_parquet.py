#!/usr/bin/env python3
"""Converte CSVs do SISCAN para Parquet em leitura incremental."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def listar_csvs(entradas: list[Path], recursive: bool) -> list[Path]:
    arquivos: list[Path] = []
    for entrada in entradas:
        if entrada.is_file():
            if entrada.suffix.lower() == ".csv":
                arquivos.append(entrada)
            continue

        if entrada.is_dir():
            padrao = "**/*.csv" if recursive else "*.csv"
            arquivos.extend(sorted(entrada.glob(padrao)))
            continue

        raise FileNotFoundError(f"Entrada nao encontrada: {entrada}")

    return sorted(dict.fromkeys(arquivos))


def caminho_saida(origem: Path, output_dir: Path | None, sufixo: str) -> Path:
    if output_dir is None:
        return origem.with_suffix(sufixo)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / origem.with_suffix(sufixo).name


def validar_parquet(destino: Path, linhas_csv: int | None, colunas_csv: list[str] | None) -> dict[str, object]:
    import pyarrow.parquet as pq

    parquet = pq.ParquetFile(destino)
    colunas_parquet = parquet.schema_arrow.names
    linhas_parquet = parquet.metadata.num_rows

    linhas_ok = linhas_csv is not None and linhas_parquet == linhas_csv
    colunas_ok = colunas_csv is not None and colunas_parquet == colunas_csv
    arquivo_ok = destino.exists() and destino.stat().st_size > 0

    problemas = []
    if not arquivo_ok:
        problemas.append("arquivo parquet nao existe ou esta vazio")
    if not linhas_ok:
        problemas.append(f"linhas divergentes: csv={linhas_csv}, parquet={linhas_parquet}")
    if not colunas_ok:
        problemas.append("colunas divergentes entre CSV e Parquet")

    return {
        "status": "ok" if arquivo_ok and linhas_ok and colunas_ok else "falhou",
        "arquivo_ok": arquivo_ok,
        "linhas_ok": linhas_ok,
        "colunas_ok": colunas_ok,
        "linhas_csv": linhas_csv,
        "linhas_parquet": linhas_parquet,
        "qtd_colunas_csv": len(colunas_csv or []),
        "qtd_colunas_parquet": len(colunas_parquet),
        "colunas_csv": colunas_csv or [],
        "colunas_parquet": colunas_parquet,
        "problemas": problemas,
    }


def ler_metadados_csv(
    origem: Path,
    sep: str,
    encoding: str,
    chunksize: int,
    infer_types: bool,
    empty_as_null: bool,
) -> tuple[int, list[str]]:
    import pandas as pd

    dtype = None if infer_types else str
    keep_default_na = empty_as_null
    na_values = None if empty_as_null else []
    total_linhas = 0
    colunas: list[str] | None = None

    leitor = pd.read_csv(
        origem,
        sep=sep,
        encoding=encoding,
        chunksize=chunksize,
        dtype=dtype,
        keep_default_na=keep_default_na,
        na_values=na_values,
        low_memory=False,
    )
    for pedaco in leitor:
        if colunas is None:
            colunas = list(pedaco.columns)
        total_linhas += len(pedaco)

    if colunas is None:
        vazio = pd.read_csv(origem, sep=sep, encoding=encoding, nrows=0, dtype=dtype)
        colunas = list(vazio.columns)

    return total_linhas, colunas


def converter_csv(
    origem: Path,
    destino: Path,
    sep: str,
    encoding: str,
    chunksize: int,
    compression: str,
    overwrite: bool,
    infer_types: bool,
    empty_as_null: bool,
    validar_existentes: bool,
) -> dict[str, object]:
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    if destino.exists() and not overwrite:
        integridade = {
            "status": "nao_verificada",
            "motivo": "conversao ignorada porque o parquet ja existia",
        }
        linhas = None
        colunas = None
        if validar_existentes:
            linhas, colunas = ler_metadados_csv(
                origem=origem,
                sep=sep,
                encoding=encoding,
                chunksize=chunksize,
                infer_types=infer_types,
                empty_as_null=empty_as_null,
            )
            integridade = validar_parquet(destino, linhas, colunas)

        return {
            "origem": str(origem),
            "destino": str(destino),
            "status": "ignorado",
            "motivo": "arquivo parquet ja existe",
            "linhas": linhas,
            "colunas": colunas,
            "integridade": integridade,
        }

    destino.parent.mkdir(parents=True, exist_ok=True)
    temporario = destino.with_suffix(destino.suffix + ".part")
    if temporario.exists():
        temporario.unlink()

    dtype = None if infer_types else str
    keep_default_na = empty_as_null
    na_values = None if empty_as_null else []

    leitor = pd.read_csv(
        origem,
        sep=sep,
        encoding=encoding,
        chunksize=chunksize,
        dtype=dtype,
        keep_default_na=keep_default_na,
        na_values=na_values,
        low_memory=False,
    )

    writer: pq.ParquetWriter | None = None
    total_linhas = 0
    colunas: list[str] | None = None

    try:
        for pedaco in leitor:
            if colunas is None:
                colunas = list(pedaco.columns)
            total_linhas += len(pedaco)
            tabela = pa.Table.from_pandas(pedaco, preserve_index=False)

            if writer is None:
                writer = pq.ParquetWriter(
                    temporario,
                    tabela.schema,
                    compression=compression,
                )
            writer.write_table(tabela)
    finally:
        if writer is not None:
            writer.close()

    if writer is None:
        vazio = pd.read_csv(origem, sep=sep, encoding=encoding, nrows=0, dtype=dtype)
        tabela = pa.Table.from_pandas(vazio, preserve_index=False)
        pq.write_table(tabela, temporario, compression=compression)
        colunas = list(vazio.columns)

    os.replace(temporario, destino)
    tamanho_origem = origem.stat().st_size
    tamanho_destino = destino.stat().st_size
    integridade = validar_parquet(destino, total_linhas, colunas or [])

    return {
        "origem": str(origem),
        "destino": str(destino),
        "status": "convertido",
        "linhas": total_linhas,
        "colunas": colunas or [],
        "tamanho_csv_bytes": tamanho_origem,
        "tamanho_parquet_bytes": tamanho_destino,
        "compression": compression,
        "infer_types": infer_types,
        "empty_as_null": empty_as_null,
        "integridade": integridade,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Converte um ou mais CSVs para Parquet sem carregar tudo em memoria."
    )
    parser.add_argument(
        "entradas",
        nargs="*",
        type=Path,
        default=[Path("dados/rj_2025")],
        help="Arquivo(s) CSV ou diretorio(s). Padrao: dados/rj_2025",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("dados/parquet"))
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--sep", default=";")
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--chunksize", type=int, default=100_000)
    parser.add_argument("--compression", default="zstd", choices=["zstd", "snappy", "gzip", "brotli", "none"])
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--validar-existentes",
        action="store_true",
        help="Quando o Parquet ja existe e a conversao e ignorada, valida o arquivo existente lendo o CSV para comparar linhas e colunas.",
    )
    parser.add_argument(
        "--infer-types",
        action="store_true",
        help="Permite inferencia de tipos pelo pandas. Por padrao, preserva todas as colunas como texto.",
    )
    parser.add_argument(
        "--empty-as-null",
        action="store_true",
        help="Interpreta campos vazios como nulos. Por padrao, preserva campos vazios como string vazia.",
    )
    parser.add_argument("--relatorio", type=Path, default=Path("dados/parquet/relatorio_conversao.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    compression = None if args.compression == "none" else args.compression
    arquivos = listar_csvs(args.entradas, args.recursive)

    if not arquivos:
        raise SystemExit("Nenhum arquivo CSV encontrado para conversao.")

    resultados = []
    for origem in arquivos:
        destino = caminho_saida(origem, args.output_dir, ".parquet")
        print(f"[conversao] {origem} -> {destino}")
        resultado = converter_csv(
            origem=origem,
            destino=destino,
            sep=args.sep,
            encoding=args.encoding,
            chunksize=args.chunksize,
            compression=compression,
            overwrite=args.overwrite,
            infer_types=args.infer_types,
            empty_as_null=args.empty_as_null,
            validar_existentes=args.validar_existentes,
        )
        resultados.append(resultado)
        status = resultado["status"]
        linhas = resultado.get("linhas")
        integridade = resultado.get("integridade", {})
        integridade_status = integridade.get("status") if isinstance(integridade, dict) else None
        print(f"[conversao] {status}: {destino}" + (f" ({linhas:,} linhas)" if linhas is not None else ""))
        if integridade_status:
            print(f"[integridade] {integridade_status}: {destino}")

    args.relatorio.parent.mkdir(parents=True, exist_ok=True)
    args.relatorio.write_text(
        json.dumps(
            {
                "gerado_em": datetime.now(timezone.utc).isoformat(),
                "arquivos": resultados,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[relatorio] {args.relatorio}")


if __name__ == "__main__":
    main()
