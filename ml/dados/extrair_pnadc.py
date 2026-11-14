"""
Extrai da PNAD Contínua 2025 (4º trimestre, módulo TIC) as pessoas de 60 anos
ou mais e as variáveis usadas no modelo do Me Conta.

Pergunta de ML: quais idosos têm mais chance de estar desconectados da internet?

Fonte: IBGE, PNAD Contínua, microdados anuais do 4º trimestre de 2025
(publicação de 02/07/2026). Veja dados/README.md.

Como rodar (a partir da pasta ml/):
    python dados/extrair_pnadc.py

Entradas (em dados/brutos/, fora do Git):
    PNADC_2025_trimestre4_20260702.zip      microdados (largura fixa)
    input_PNADC_trimestre4_20251010.txt     posições das variáveis (SAS)

Saídas (em dados/processados/):
    pnadc2025_tic_60mais.parquet
    pnadc2025_tic_60mais.csv
"""

import argparse
import io
import re
import time
import zipfile
from collections import defaultdict
from pathlib import Path

import pandas as pd

PASTA_DADOS = Path(__file__).resolve().parent      # pasta dados/, onde fica este script
BRUTOS = PASTA_DADOS / "brutos"
PROCESSADOS = PASTA_DADOS / "processados"

IDADE_MINIMA = 60

# Variáveis lidas de cada pessoa de 60+. Os papéis estão em dados/variaveis.md.
VARIAVEIS = [
    # Identificação e desenho amostral
    "Ano", "Trimestre", "UF", "Capital", "RM_RIDE", "UPA", "Estrato",
    "V1008", "V1014", "V2003", "V1028",
    # Localização
    "V1022", "V1023",
    # Pessoa
    "V2005", "V2007", "V2009", "V2010", "V3001", "VD3004", "VD3005",
    "VD4001", "VD4002", "VI5004A",
    # Domicílio
    "V2001", "VD2003", "VD2004", "VDI5008", "VDI5009",
    "S01021", "S01028", "S01029", "S01030C", "S01030D",
    # TIC da pessoa
    "S07001", "S07001A", "S07005A", "S07005B2", "S07006", "S07007",
    "S07008A", "S07009",
]

# Variáveis numéricas (as demais são códigos de categoria).
NUMERICAS = {"V1028", "V2009", "V2001", "VD2003", "VD3005", "VDI5008", "S01021"}

# Usadas para montar as contagens do domicílio a partir de TODOS os moradores.
VARS_DOMICILIO = ["UPA", "V1008", "V1014", "V2009", "S07001"]


def ler_layout(caminho_input):
    """Lê o input SAS do IBGE e devolve {variável: (início, fim)} em índices Python."""
    padrao = re.compile(r"@(\d+)\s+(\S+)\s+\$?(\d+)\.")
    layout = {}
    with open(caminho_input, encoding="utf-8", errors="replace") as f:
        for linha in f:
            m = padrao.match(linha.strip())
            if m:
                inicio, nome, tamanho = int(m.group(1)), m.group(2), int(m.group(3))
                layout[nome] = (inicio - 1, inicio - 1 + tamanho)
    faltando = [v for v in VARIAVEIS if v not in layout]
    if faltando:
        raise ValueError(f"Variáveis não encontradas no input: {faltando}")
    return layout


def abrir_microdados(caminho_zip):
    """Abre o .txt de dentro do .zip sem descompactar no disco."""
    z = zipfile.ZipFile(caminho_zip)
    txts = [n for n in z.namelist() if n.lower().endswith(".txt")]
    if len(txts) != 1:
        raise ValueError(f"Esperava um .txt dentro do zip, achei: {txts}")
    print(f"Lendo {txts[0]} de dentro de {Path(caminho_zip).name}")
    return io.TextIOWrapper(z.open(txts[0]), encoding="latin-1")


def para_numero(texto, nome):
    """Converte o texto de uma posição fixa em número (espaços = ausente)."""
    texto = texto.strip()
    if not texto:
        return None
    if nome == "V1028" and "." not in texto:
        return int(texto) / 1e8  # peso com 8 casas decimais implícitas
    return float(texto)


def extrair(caminho_zip, layout):
    pos = {v: layout[v] for v in VARIAVEIS}
    pos_dom = {v: layout[v] for v in VARS_DOMICILIO}

    # Contagens por domicílio, com todos os moradores (não só os idosos).
    dom = defaultdict(lambda: {"n_10mais": 0, "n_usam": 0, "n_jovens": 0, "n_jovens_usam": 0})
    idosos = []
    inicio = time.time()

    with abrir_microdados(caminho_zip) as f:
        for i, linha in enumerate(f, start=1):
            d = {v: linha[a:b] for v, (a, b) in pos_dom.items()}
            chave = d["UPA"] + d["V1008"] + d["V1014"]
            idade = int(d["V2009"])
            usa = d["S07001"] == "1"

            c = dom[chave]
            if idade >= 10:
                c["n_10mais"] += 1
                c["n_usam"] += usa
            if 10 <= idade <= 29:
                c["n_jovens"] += 1
                c["n_jovens_usam"] += usa

            if idade >= IDADE_MINIMA:
                reg = {}
                for v, (a, b) in pos.items():
                    bruto = linha[a:b]
                    if v in NUMERICAS:
                        reg[v] = para_numero(bruto, v)
                    else:
                        reg[v] = bruto.strip() or None
                reg["chave_domicilio"] = chave
                idosos.append(reg)

            if i % 100_000 == 0:
                print(f"  {i:>9,} linhas lidas · {len(idosos):,} idosos · {time.time() - inicio:.0f}s")

    print(f"Total: {i:,} pessoas lidas, {len(idosos):,} com {IDADE_MINIMA}+ anos")
    df = pd.DataFrame(idosos)
    contagens = pd.DataFrame.from_dict(dom, orient="index")
    contagens.index.name = "chave_domicilio"
    return df.merge(contagens, on="chave_domicilio", how="left")


def derivar(df):
    """Cria o alvo e as variáveis derivadas."""
    # Só fica quem respondeu a pergunta do alvo.
    antes = len(df)
    df = df[df["S07001"].isin(["1", "2"])].copy()
    print(f"Sem resposta em S07001 (removidos): {antes - len(df):,}")

    # Alvo: 1 = não usou a internet nos últimos 3 meses (desconectado).
    df["desconectado"] = (df["S07001"] == "2").astype(int)

    usa = (df["S07001"] == "1").astype(int)
    tem_cel = (df["S07006"] == "1").astype(int)

    # Contagens dos OUTROS moradores (tirando a própria pessoa).
    df["outros_usam_internet"] = df["n_usam"] - usa
    df["tem_outro_usuario_internet"] = (df["outros_usam_internet"] > 0).astype(int)
    df["tem_jovem_10a29"] = (df["n_jovens"] > 0).astype(int)
    df["tem_jovem_que_usa_internet"] = (df["n_jovens_usam"] > 0).astype(int)
    df["outros_com_celular"] = (df["S01021"] - tem_cel).clip(lower=0)

    df["mora_sozinho"] = (df["VD2004"] == "1").astype(int)
    df["urbano"] = (df["V1022"] == "1").astype(int)
    df["faixa_etaria"] = pd.cut(
        df["V2009"], bins=[59, 64, 69, 74, 79, 200],
        labels=["60-64", "65-69", "70-74", "75-79", "80+"],
    )
    df["regiao"] = df["UF"].str[0].map(
        {"1": "Norte", "2": "Nordeste", "3": "Sudeste", "4": "Sul", "5": "Centro-Oeste"}
    )
    # Renda: 99999999 = ignorado.
    df.loc[df["VDI5008"] >= 99_999_999, "VDI5008"] = None

    return df.drop(columns=["n_10mais", "n_usam", "n_jovens", "n_jovens_usam"])


def resumo(df):
    w = df["V1028"]
    pct = (df["desconectado"] * w).sum() / w.sum() * 100
    print("\n=== Resumo ===")
    print(f"Ano(s): {sorted(df['Ano'].unique())} · Trimestre(s): {sorted(df['Trimestre'].unique())}")
    print(f"Idosos na amostra: {len(df):,}")
    print(f"Idosos representados (soma dos pesos): {w.sum() / 1e6:.1f} milhões")
    print(f"Desconectados (ponderado): {pct:.1f}%  ·  (amostra, sem peso): {df['desconectado'].mean() * 100:.1f}%")
    print(f"Desconectados representados: {(df['desconectado'] * w).sum() / 1e6:.1f} milhões")
    print("\n% de valores ausentes por coluna (só as que têm algum):")
    ausentes = df.isna().mean().mul(100).round(1)
    print(ausentes[ausentes > 0].sort_values(ascending=False).to_string())


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--zip", default=BRUTOS / "PNADC_2025_trimestre4_20260702.zip", type=Path)
    p.add_argument("--input", default=BRUTOS / "input_PNADC_trimestre4_20251010.txt", type=Path)
    p.add_argument("--saida", default=PROCESSADOS, type=Path)
    args = p.parse_args()

    layout = ler_layout(args.input)
    df = derivar(extrair(args.zip, layout))
    resumo(df)

    args.saida.mkdir(parents=True, exist_ok=True)
    base = args.saida / "pnadc2025_tic_60mais"
    df.to_parquet(base.with_suffix(".parquet"), index=False)
    df.to_csv(base.with_suffix(".csv"), index=False)
    print(f"\nSalvo em {base}.parquet e .csv")


if __name__ == "__main__":
    main()
