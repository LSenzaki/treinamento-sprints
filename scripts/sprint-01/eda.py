"""EDA do dataset_vendas.csv — Sprint 1.

Lê o CSV em chunks (1.5 GB / ~8.4M linhas) e acumula estatísticas para gerar
os documentos da Sprint 1 em docs/sprint-01/.

Uso:
    python scripts/sprint-01/eda.py /caminho/para/dataset_vendas.csv
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

COL_NAMES = [
    "filial",
    "cidade",
    "status_venda",
    "data_hora",
    "cliente_nome",
    "cliente_nascimento",
    "cliente_genero",
    "produto_descricao",
    "produto_ean",
    "quantidade",
    "valor",
    "categoria",
    "controle",
]

CHUNK_SIZE = 500_000


def main(csv_path: str) -> None:
    csv = Path(csv_path)
    out_dir = Path(__file__).resolve().parents[2] / "docs" / "sprint-01"
    out_dir.mkdir(parents=True, exist_ok=True)

    total_rows = 0
    nulls = Counter()
    status_counts = Counter()
    filial_counts = Counter()
    cidade_counts = Counter()
    genero_counts = Counter()
    categoria_counts = Counter()
    controle_counts = Counter()

    min_date: pd.Timestamp | None = None
    max_date: pd.Timestamp | None = None
    min_nasc: pd.Timestamp | None = None
    max_nasc: pd.Timestamp | None = None

    qtd_stats = {"min": float("inf"), "max": float("-inf"), "sum": 0.0, "neg": 0, "zero": 0}
    val_stats = {"min": float("inf"), "max": float("-inf"), "sum": 0.0, "neg": 0, "zero": 0}

    vendas_por_dia: Counter = Counter()
    vendas_por_filial_dia: dict[str, Counter] = defaultdict(Counter)
    faturamento_por_filial: Counter = Counter()
    qtd_por_filial: Counter = Counter()
    duplicatas_chave: set[tuple] = set()
    dup_count = 0

    distinct_produtos: set[str] = set()
    distinct_clientes: set[str] = set()
    distinct_ean: set[str] = set()

    reader = pd.read_csv(
        csv,
        sep=";",
        header=None,
        names=COL_NAMES,
        encoding="utf-8-sig",
        chunksize=CHUNK_SIZE,
        dtype=str,
        keep_default_na=False,
        na_values=["", "NULL", "null", "NaN"],
    )

    for i, chunk in enumerate(reader, start=1):
        n = len(chunk)
        total_rows += n
        for col in COL_NAMES:
            nulls[col] += chunk[col].isna().sum()

        # parse numéricos
        qtd = pd.to_numeric(chunk["quantidade"].str.replace(",", ".", regex=False), errors="coerce")
        val = pd.to_numeric(chunk["valor"].str.replace(",", ".", regex=False), errors="coerce")

        qtd_stats["min"] = min(qtd_stats["min"], qtd.min(skipna=True))
        qtd_stats["max"] = max(qtd_stats["max"], qtd.max(skipna=True))
        qtd_stats["sum"] += qtd.sum(skipna=True)
        qtd_stats["neg"] += int((qtd < 0).sum())
        qtd_stats["zero"] += int((qtd == 0).sum())

        val_stats["min"] = min(val_stats["min"], val.min(skipna=True))
        val_stats["max"] = max(val_stats["max"], val.max(skipna=True))
        val_stats["sum"] += val.sum(skipna=True)
        val_stats["neg"] += int((val < 0).sum())
        val_stats["zero"] += int((val == 0).sum())

        # parse datas
        dt = pd.to_datetime(chunk["data_hora"], errors="coerce")
        nasc = pd.to_datetime(chunk["cliente_nascimento"], errors="coerce")

        if dt.notna().any():
            mn, mx = dt.min(), dt.max()
            min_date = mn if min_date is None else min(min_date, mn)
            max_date = mx if max_date is None else max(max_date, mx)
        if nasc.notna().any():
            mn, mx = nasc.min(), nasc.max()
            min_nasc = mn if min_nasc is None else min(min_nasc, mn)
            max_nasc = mx if max_nasc is None else max(max_nasc, mx)

        # categóricos
        status_counts.update(chunk["status_venda"].dropna().tolist())
        filial_counts.update(chunk["filial"].dropna().tolist())
        cidade_counts.update(chunk["cidade"].dropna().tolist())
        genero_counts.update(chunk["cliente_genero"].dropna().tolist())
        categoria_counts.update(chunk["categoria"].dropna().tolist())
        controle_counts.update(chunk["controle"].dropna().tolist())

        # agregações por dia / filial
        dia = dt.dt.date.astype(str)
        for d, group_val, group_qtd, group_filial in zip(
            dia, val, qtd, chunk["filial"]
        ):
            if d != "NaT":
                vendas_por_dia[d] += 1
                if isinstance(group_filial, str):
                    vendas_por_filial_dia[group_filial][d] += 1

        for f, v in zip(chunk["filial"], val):
            if isinstance(f, str) and pd.notna(v):
                faturamento_por_filial[f] += float(v)
        for f, q in zip(chunk["filial"], qtd):
            if isinstance(f, str) and pd.notna(q):
                qtd_por_filial[f] += float(q)

        # cardinalidade (com cap pra não estourar memória)
        if len(distinct_produtos) < 5_000_000:
            distinct_produtos.update(chunk["produto_descricao"].dropna().tolist())
        if len(distinct_clientes) < 5_000_000:
            distinct_clientes.update(chunk["cliente_nome"].dropna().tolist())
        if len(distinct_ean) < 5_000_000:
            distinct_ean.update(chunk["produto_ean"].dropna().tolist())

        # duplicatas: chave composta natural
        keys = list(
            zip(
                chunk["filial"],
                chunk["data_hora"],
                chunk["cliente_nome"],
                chunk["produto_ean"],
                chunk["quantidade"],
                chunk["valor"],
            )
        )
        for k in keys:
            if k in duplicatas_chave:
                dup_count += 1
            else:
                duplicatas_chave.add(k)

        print(f"chunk {i}: linhas acumuladas={total_rows:,}", flush=True)

    print("\nGerando documentos...", flush=True)

    # ---------- 1. Dicionário de Colunas ----------
    dicionario = """# Dicionário de Colunas — `dataset_vendas.csv`

> Gerado pela Sprint 1 (EDA). O arquivo **não tem cabeçalho**; os nomes abaixo são
> derivados do significado de cada posição no contexto de farmácias.

| # | Nome | Tipo | Descrição | Exemplo |
|---|------|------|-----------|---------|
| 1 | `filial` | texto | Filial da rede que efetuou a venda | `FCIA LIDER FILIAL 1` |
| 2 | `cidade` | texto | Cidade onde fica a filial | `PALOTINA` |
| 3 | `status_venda` | texto | Status da transação | `CANCELADO`, `FINALIZADO` |
| 4 | `data_hora` | datetime | Data e hora exata da venda (ms) | `2015-03-24 09:05:30.997` |
| 5 | `cliente_nome` | texto | Nome do cliente (primeiro nome) | `OLIVIA` |
| 6 | `cliente_nascimento` | datetime | Data de nascimento do cliente | `1950-04-13 00:00:00.000` |
| 7 | `cliente_genero` | texto | Gênero declarado | `FEMININO`, `MASCULINO` |
| 8 | `produto_descricao` | texto | Descrição comercial do produto | `LOSARTANA POTASSICA 50 MG C/30 CPR` |
| 9 | `produto_ean` | texto | Código de barras (EAN-13) | `7896714273884` |
| 10 | `quantidade` | número | Quantidade vendida na linha | `1.0000` |
| 11 | `valor` | número | Valor total da linha (R$) | `9.00` |
| 12 | `categoria` | texto | Categoria comercial do produto | `GENERICOS 2`, `SIMILARES 1` |
| 13 | `controle` | texto | Tipo de controle do medicamento | `SEM CONTROLE` |

## Notas
- Arquivo usa `;` como separador e tem **BOM** no início (`utf-8-sig`).
- `quantidade` e `valor` podem vir com vírgula decimal — converter antes de operações numéricas.
- `data_hora` está em granularidade de milissegundos.
- Cada linha do CSV representa **um item** de uma venda (não a venda agregada). Vendas podem ter múltiplas linhas com mesmo `filial + data_hora + cliente_nome`.
"""
    (out_dir / "dicionario_colunas.md").write_text(dicionario)

    # ---------- 2. Cobertura ----------
    total_dias_periodo = (max_date - min_date).days + 1 if min_date and max_date else 0
    dias_com_venda = len(vendas_por_dia)
    media_vendas_dia = total_rows / dias_com_venda if dias_com_venda else 0

    cobertura = f"""# Cobertura do Arquivo — Sprint 1

## Volume
- Total de linhas: **{total_rows:,}**
- Total de filiais: **{len(filial_counts)}**
- Total de cidades: **{len(cidade_counts)}**
- Produtos distintos (descrição): **{len(distinct_produtos):,}**
- EANs distintos: **{len(distinct_ean):,}**
- Clientes distintos (por primeiro nome): **{len(distinct_clientes):,}**
  - ⚠️ É *primeiro nome* — provavelmente subestima clientes únicos reais.

## Período
- Data mínima: **{min_date}**
- Data máxima: **{max_date}**
- Dias no período (calendário): **{total_dias_periodo}**
- Dias com pelo menos uma venda: **{dias_com_venda}**
- Cobertura temporal: **{(dias_com_venda / total_dias_periodo * 100 if total_dias_periodo else 0):.1f}%** dos dias

## Média de vendas
- Linhas por dia (média): **{media_vendas_dia:,.0f}**
- Linhas por dia (mediana): **{int(pd.Series(list(vendas_por_dia.values())).median()):,}**

## Top 5 dias com mais vendas
"""
    top_dias = sorted(vendas_por_dia.items(), key=lambda x: -x[1])[:5]
    for d, c in top_dias:
        cobertura += f"- `{d}` — {c:,} linhas\n"

    cobertura += "\n## Insights iniciais\n"
    cobertura += "1. O arquivo cobre vários anos; é viável análise sazonal mensal e anual.\n"
    cobertura += "2. Há **variação relevante** entre dias — a média sozinha esconde picos.\n"
    cobertura += "3. Algumas filiais podem ter períodos sem operação; validar na Sprint 2.\n"

    (out_dir / "cobertura.md").write_text(cobertura)

    # ---------- 3. Filiais ----------
    filiais = "# Análise por Filiais — Sprint 1\n\n"
    filiais += f"Total de filiais: **{len(filial_counts)}**\n\n"
    filiais += "## Volume e faturamento por filial\n\n"
    filiais += "| Filial | Linhas | % | Qtd total | Faturamento (R$) | Ticket médio linha |\n"
    filiais += "|---|---:|---:|---:|---:|---:|\n"
    for f, c in filial_counts.most_common():
        fat = faturamento_por_filial.get(f, 0.0)
        qtd_total = qtd_por_filial.get(f, 0.0)
        ticket = fat / c if c else 0.0
        pct = c / total_rows * 100
        filiais += f"| {f} | {c:,} | {pct:.1f}% | {qtd_total:,.0f} | {fat:,.2f} | {ticket:,.2f} |\n"

    filiais += "\n## Decisão: analisar por filial ou agregado?\n\n"
    if len(filial_counts) == 1:
        filiais += "Existe **apenas uma filial** — análise agregada é equivalente.\n"
    else:
        filiais += (
            "Existem **múltiplas filiais**. Recomenda-se análise **por filial** como padrão,\n"
            "porque cidade, mix de produtos e volume variam entre elas. Visões agregadas\n"
            "devem ser usadas apenas quando o objetivo for o desempenho da rede como um todo.\n"
        )
    (out_dir / "filiais.md").write_text(filiais)

    # ---------- 4. Problemas / Inconsistências ----------
    problemas = "# Problemas e Inconsistências — Sprint 1\n\n"
    problemas += "Lista de problemas encontrados que servem de entrada para a **Sprint 2**.\n\n"

    problemas += "## Nulos por coluna\n\n"
    problemas += "| Coluna | Nulos | % |\n|---|---:|---:|\n"
    for col in COL_NAMES:
        pct = nulls[col] / total_rows * 100 if total_rows else 0
        problemas += f"| `{col}` | {nulls[col]:,} | {pct:.2f}% |\n"

    problemas += "\n## Status de venda\n\n"
    problemas += "| Status | Linhas | % |\n|---|---:|---:|\n"
    for s, c in status_counts.most_common():
        problemas += f"| {s} | {c:,} | {c/total_rows*100:.2f}% |\n"

    problemas += "\n## Quantidade e valor\n\n"
    problemas += "| Métrica | quantidade | valor |\n|---|---:|---:|\n"
    problemas += f"| min | {qtd_stats['min']} | {val_stats['min']} |\n"
    problemas += f"| max | {qtd_stats['max']} | {val_stats['max']} |\n"
    problemas += f"| soma | {qtd_stats['sum']:,.2f} | R$ {val_stats['sum']:,.2f} |\n"
    problemas += f"| negativos | {qtd_stats['neg']:,} | {val_stats['neg']:,} |\n"
    problemas += f"| zeros | {qtd_stats['zero']:,} | {val_stats['zero']:,} |\n"

    problemas += "\n## Duplicidades\n"
    problemas += (
        f"- Linhas com chave composta `(filial, data_hora, cliente_nome, ean, qtd, valor)` "
        f"repetida: **{dup_count:,}**\n"
    )
    problemas += "  - Pode indicar erro de carga ou múltiplas unidades do mesmo item na mesma venda.\n"

    problemas += "\n## Cardinalidade\n"
    problemas += f"- Filial: {len(filial_counts)}\n"
    problemas += f"- Cidade: {len(cidade_counts)}\n"
    problemas += f"- Status: {len(status_counts)}\n"
    problemas += f"- Gênero: {len(genero_counts)}\n"
    problemas += f"- Categoria: {len(categoria_counts)}\n"
    problemas += f"- Controle: {len(controle_counts)}\n"
    problemas += f"- Cliente (primeiro nome): {len(distinct_clientes):,}\n"
    problemas += f"- Produto (descrição): {len(distinct_produtos):,}\n"
    problemas += f"- EAN: {len(distinct_ean):,}\n"

    problemas += "\n## Datas de nascimento\n"
    problemas += f"- Mínima: `{min_nasc}`\n"
    problemas += f"- Máxima: `{max_nasc}`\n"
    if min_nasc and min_nasc.year < 1900:
        problemas += "  - ⚠️ Há nascimentos antes de 1900 — provavelmente erro.\n"

    problemas += "\n## Propostas de tratamento (Sprint 2)\n"
    problemas += "1. **Nulos**: tratar caso a caso (ver tabela acima). Cliente sem nome → marcar como `ANONIMO`.\n"
    problemas += "2. **Status `CANCELADO`**: separar em coluna `is_cancelada` e por padrão excluir das análises de faturamento.\n"
    problemas += "3. **Valores negativos**: investigar — podem ser devoluções; manter mas sinalizar.\n"
    problemas += "4. **Nascimentos absurdos**: descartar ou imputar como nulo.\n"
    problemas += "5. **Duplicidades**: agrupar por chave composta + somar quantidade (regra a confirmar).\n"
    problemas += "6. **Padronização textual**: aplicar UPPER + trim em nomes de produto e cidade.\n"

    (out_dir / "problemas.md").write_text(problemas)

    # ---------- 5. Relevância das colunas ----------
    relevancia = """# Relevância das Colunas — Sprint 1

Decisão sobre quais colunas manter para as próximas sprints.

| Coluna | Manter? | Justificativa |
|---|---|---|
| `filial` | ✅ | Chave primária de segmentação |
| `cidade` | ✅ | Derivável de `filial` mas útil para visões geográficas |
| `status_venda` | ✅ | Necessária para filtrar `CANCELADO` |
| `data_hora` | ✅ | Base para todas as análises temporais |
| `cliente_nome` | ⚠️ | Manter, mas saber que **não é um ID único** (homônimos) |
| `cliente_nascimento` | ✅ | Permite calcular idade — feature importante na Sprint 3 |
| `cliente_genero` | ✅ | Demografia |
| `produto_descricao` | ✅ | Mix de produto |
| `produto_ean` | ✅ | Chave mais confiável que descrição para produto |
| `quantidade` | ✅ | Métrica |
| `valor` | ✅ | Métrica |
| `categoria` | ✅ | Análises agregadas |
| `controle` | ⚠️ | Avaliar utilidade real — alta concentração em um único valor pode torná-la pouco informativa |

## Conclusão
- Não há colunas para remover de saída.
- `controle` deve ser reavaliada após Sprint 2 com base na cardinalidade efetiva.
- `cliente_nome` precisa ser combinada com `cliente_nascimento` para criar um ID estável de cliente na Sprint 3.
"""
    (out_dir / "colunas_finais.md").write_text(relevancia)

    # ---------- README da Sprint 1 ----------
    readme = """# Sprint 1 — Resultados

Documentos gerados pela EDA do `dataset_vendas.csv`.

- [`dicionario_colunas.md`](./dicionario_colunas.md) — nomes, tipos e contexto de cada coluna
- [`cobertura.md`](./cobertura.md) — período, volume e insights iniciais
- [`filiais.md`](./filiais.md) — comparativo entre filiais + decisão de análise
- [`problemas.md`](./problemas.md) — nulos, inconsistências e duplicidades (entrada da Sprint 2)
- [`colunas_finais.md`](./colunas_finais.md) — quais colunas manter

## Como reproduzir
```bash
python scripts/sprint-01/eda.py /caminho/para/dataset_vendas.csv
```
"""
    (out_dir / "README.md").write_text(readme)

    print(f"OK. Arquivos em {out_dir}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("uso: python eda.py /caminho/para/dataset_vendas.csv", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
