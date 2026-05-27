# Padronizacao Textual - Sprint 2

Objetivo: eliminar duplicidades semanticas em colunas categoricas causadas por variacoes de capitalizacao, espacos extras e acentuacao.

## Colunas alvo

- `produto_descricao`
- `cidade`
- `filial`
- `categoria_produto`

## Regra aplicada (em `clean.py:normalize_text`)

Sequencia aplicada a cada valor nao-nulo das colunas alvo:

1. `strip()` nas pontas
2. Colapso de espacos internos: `' '.join(text.split())` (multiplos espacos -> um unico)
3. `upper()` para uniformizar capitalizacao
4. Remocao de acentos via `unicodedata.normalize('NFKD', ...)` + filtro de combining chars

Exemplos do efeito:

| Original                      | Normalizado              |
|---|---|
| `  Dipirona  500MG `          | `DIPIRONA 500MG`         |
| `Dipirona 500mg`              | `DIPIRONA 500MG`         |
| `São Paulo`                   | `SAO PAULO`              |
| `Fcia Lider Filial 1`         | `FCIA LIDER FILIAL 1`    |
| `analgésico`                  | `ANALGESICO`             |

## Etapa no `clean.py`

Aplicada apos o filtro de status e antes da escrita da linha de saida. Para cada linha que entra na saida, conta-se em `stats.text_normalized_changed[col]` quantas vezes o valor pos-normalizacao difere do valor bruto, e os conjuntos de valores unicos pre/pos sao agregados em `unique_counts`.

## Comparacao antes/depois - valores unicos

Numeros extraidos de `clean_log.json` apos execucao em `dataset_vendas.csv` completo (8.460.074 linhas brutas, 7.883.870 com `status_venda = FECHADO`).

| coluna | unicos antes | unicos depois | reducao | linhas com texto alterado |
|---|---:|---:|---:|---:|
| produto_descricao | 75.529 | 75.003 | 526 (0,70%) | 55.937 |
| cidade            | 2      | 2      | 0           | 0       |
| filial            | 17     | 17     | 0           | 125.134 |
| categoria_produto | 23     | 23     | 0           | 0       |

### Leitura dos resultados

- **`produto_descricao`** — colapso real: 526 descricoes diferentes apenas por case/espaco/acento foram unificadas. Confirma que existia duplicidade semantica antes (~0,7%). Resto da duplicidade (descricoes diferentes para o mesmo SKU) so cai com a dimensao de produto na Sprint 3.
- **`cidade`** e **`categoria_produto`** — dominio textual ja consistente no bruto, sem alteracoes. A regra continua aplicada como salvaguarda preventiva caso novos dados venham com inconsistencias.
- **`filial`** — 125.134 linhas tiveram texto alterado (provavelmente espacos extras/case), mas o numero de unicos nao caiu: nenhum par de filiais "logicamente iguais" estava no dataset com grafias diferentes. A normalizacao deixou todas as 17 filiais na grafia canonica.

### Smoke test sintetico

Para validar que a regra realmente colapsa duplicidades, `scripts/smoke_test.py` gera um CSV minusculo com variacoes propositais (case, espacos, acentos) e roda o pipeline. Resultado observado:

| coluna | antes | depois |
|---|---:|---:|
| produto_descricao | 6 | 2 |
| cidade            | 7 | 2 |
| filial            | 4 | 1 |
| categoria_produto | 6 | 2 |

(execute `python scripts/smoke_test.py` para reproduzir)

## Decisoes registradas

- **Nao removemos** simbolos/pontuacao dentro do texto (ex.: numeros, `/`, `%`) — apenas case, espacos e acentos. Variacoes legitimas de SKU (dosagem, apresentacao) sao preservadas.
- A normalizacao acontece apenas nas colunas listadas. `nome_cliente` segue hash anonimizado em `cliente_id`; outras colunas categoricas (`genero_cliente`, `status_venda`, `tipo_controle`) tem dominio fechado tratado com tokens fixos.
- O par `produto_descricao` x `ean_produto` ainda pode ter duplicidade semantica fora do alcance dessa regra (descricoes diferentes para o mesmo EAN). Isso sera atacado na construcao da dimensao de produto na Sprint 3 (ver `docs/sprint-01/colunas_finais.md`).
