# Dicionário de Colunas — `dataset_vendas.csv`

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
