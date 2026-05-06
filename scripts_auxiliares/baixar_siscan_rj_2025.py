#!/usr/bin/env python3
"""Baixa dados SISCAN 2025 do DATASUS e filtra registros do RJ."""

from __future__ import annotations

import argparse
import ftplib
import os
from pathlib import Path
from typing import Iterable


FTP_HOST = "ftp.datasus.gov.br"
FTP_DIR = "/dissemin/publicos/SISCAN/SISCAN"
ANO_PADRAO = 2025
UF_RJ_CODIGO = "33"
UF_RJ_SIGLA = "RJ"

ARQUIVOS_2025 = {
    "cito_colo": "SISCAN_CITO_COLO_2025.csv",
    "cito_colo_pacnt": "SISCAN_CITO_COLO_PACNT_2025.csv",
    "cito_mama": "SISCAN_CITO_MAMA_2025.csv",
    "cito_mama_pacnt": "SISCAN_CITO_MAMA_PACNT_2025.csv",
    "histo_colo": "SISCAN_HISTO_COLO_2025.csv",
    "histo_colo_pacnt": "SISCAN_HISTO_COLO_PACNT_2025.csv",
    "histo_mama": "SISCAN_HISTO_MAMA_2025.csv",
    "histo_mama_pacnt": "SISCAN_HISTO_MAMA_PACNT_2025.csv",
    "mamografia": "SISCAN_MAMOGRAFIA_2025.csv",
    "mamografia_pacnt": "SISCAN_MAMOGRAFIA_PACNT_2025.csv",
}


def abrir_ftp() -> ftplib.FTP:
    ftp = ftplib.FTP(FTP_HOST, timeout=120)
    ftp.login()
    ftp.cwd(FTP_DIR)
    ftp.voidcmd("TYPE I")
    return ftp


def tamanho_remoto(ftp: ftplib.FTP, nome_arquivo: str) -> int:
    tamanho = ftp.size(nome_arquivo)
    if tamanho is None:
        raise RuntimeError(f"Nao foi possivel obter tamanho remoto: {nome_arquivo}")
    return tamanho


def baixar_arquivo(ftp: ftplib.FTP, nome_arquivo: str, destino: Path, sobrescrever: bool) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    esperado = tamanho_remoto(ftp, nome_arquivo)

    if destino.exists() and destino.stat().st_size == esperado and not sobrescrever:
        print(f"[download] OK existente: {destino} ({esperado:,} bytes)")
        return

    temporario = destino.with_suffix(destino.suffix + ".part")
    if temporario.exists():
        temporario.unlink()

    print(f"[download] Baixando {nome_arquivo} -> {destino}")
    with temporario.open("wb") as fp:
        ftp.retrbinary(f"RETR {nome_arquivo}", fp.write, blocksize=1024 * 1024)

    obtido = temporario.stat().st_size
    if obtido != esperado:
        raise RuntimeError(
            f"Download incompleto de {nome_arquivo}: {obtido:,} bytes; esperado {esperado:,}"
        )

    os.replace(temporario, destino)


def colunas_uf(colunas: Iterable[str]) -> list[str]:
    candidatas_residencia = [
        "SG_UF_RESIDENCIA",
        "CO_UF_RESIDENCIA",
    ]
    candidatas_fallback = [
        "SG_UF_UNIDADE_SAUDE",
        "CO_UF_UNIDADE_SAUDE",
        "SG_UF_PREST_SERVICO",
        "CO_UF_PREST_SERVICO",
    ]
    existentes = [coluna for coluna in candidatas_residencia if coluna in colunas]
    if not existentes:
        existentes = [coluna for coluna in candidatas_fallback if coluna in colunas]
    if not existentes:
        raise ValueError(
            "Nao encontrei coluna de UF esperada. Colunas disponiveis: "
            + ", ".join(list(colunas)[:30])
        )
    return existentes


def filtrar_rj(origem: Path, destino: Path, chunksize: int) -> None:
    import pandas as pd

    destino.parent.mkdir(parents=True, exist_ok=True)
    temporario = destino.with_suffix(destino.suffix + ".part")
    if temporario.exists():
        temporario.unlink()

    total_linhas = 0
    total_rj = 0
    escreveu_cabecalho = False

    leitor = pd.read_csv(
        origem,
        sep=";",
        dtype=str,
        chunksize=chunksize,
        encoding="utf-8",
        low_memory=False,
    )

    for pedaco in leitor:
        total_linhas += len(pedaco)
        ufs = colunas_uf(pedaco.columns)
        mascara = pd.Series(False, index=pedaco.index)
        for coluna in ufs:
            valores = pedaco[coluna].astype("string").str.strip().str.upper()
            mascara = mascara | valores.isin({UF_RJ_SIGLA, UF_RJ_CODIGO})

        filtrado = pedaco.loc[mascara]
        total_rj += len(filtrado)
        if not filtrado.empty:
            filtrado.to_csv(
                temporario,
                sep=";",
                index=False,
                mode="a",
                header=not escreveu_cabecalho,
                encoding="utf-8",
            )
            escreveu_cabecalho = True

    if not escreveu_cabecalho:
        # Mantem um CSV valido mesmo se a base nao tiver registros do RJ.
        cabecalho = pd.read_csv(origem, sep=";", dtype=str, nrows=0, encoding="utf-8")
        cabecalho.to_csv(temporario, sep=";", index=False, encoding="utf-8")

    os.replace(temporario, destino)
    print(f"[filtro] {origem.name}: {total_rj:,}/{total_linhas:,} registros -> {destino}")


def selecionar_tipos(tipos: list[str]) -> dict[str, str]:
    if "todos" in tipos:
        return ARQUIVOS_2025

    invalidos = sorted(set(tipos) - set(ARQUIVOS_2025))
    if invalidos:
        opcoes = ", ".join(["todos", *ARQUIVOS_2025])
        raise SystemExit(f"Tipos invalidos: {', '.join(invalidos)}. Opcoes: {opcoes}")

    return {tipo: ARQUIVOS_2025[tipo] for tipo in tipos}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Baixa os arquivos SISCAN 2025 do DATASUS e filtra registros do RJ."
    )
    parser.add_argument("--raw-dir", type=Path, default=Path("dados/raw"))
    parser.add_argument("--out-dir", type=Path, default=Path("dados/rj_2025"))
    parser.add_argument("--chunksize", type=int, default=100_000)
    parser.add_argument("--sobrescrever", action="store_true")
    parser.add_argument("--somente-listar", action="store_true")
    parser.add_argument(
        "--tipos",
        nargs="+",
        default=["todos"],
        help="Tipos a baixar: todos, " + ", ".join(ARQUIVOS_2025),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    selecionados = selecionar_tipos(args.tipos)

    if args.somente_listar:
        for tipo, arquivo in selecionados.items():
            print(f"{tipo}: ftp://{FTP_HOST}{FTP_DIR}/{arquivo}")
        return

    with abrir_ftp() as ftp:
        for tipo, arquivo in selecionados.items():
            bruto = args.raw_dir / arquivo
            filtrado = args.out_dir / arquivo.replace(f"_{ANO_PADRAO}.csv", f"_RJ_{ANO_PADRAO}.csv")
            baixar_arquivo(ftp, arquivo, bruto, args.sobrescrever)
            if filtrado.exists() and not args.sobrescrever:
                print(f"[filtro] OK existente: {filtrado}")
                continue
            filtrar_rj(bruto, filtrado, args.chunksize)


if __name__ == "__main__":
    main()
