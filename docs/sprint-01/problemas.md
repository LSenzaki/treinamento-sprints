# Problemas e Inconsistências — Sprint 1

Lista de problemas encontrados que servem de entrada para a **Sprint 2**.

## Nulos por coluna

| Coluna | Nulos | % |
|---|---:|---:|
| `filial` | 0 | 0.00% |
| `cidade` | 0 | 0.00% |
| `status_venda` | 0 | 0.00% |
| `data_hora` | 0 | 0.00% |
| `cliente_nome` | 0 | 0.00% |
| `cliente_nascimento` | 1 | 0.00% |
| `cliente_genero` | 0 | 0.00% |
| `produto_descricao` | 0 | 0.00% |
| `produto_ean` | 101 | 0.00% |
| `quantidade` | 0 | 0.00% |
| `valor` | 0 | 0.00% |
| `categoria` | 0 | 0.00% |
| `controle` | 0 | 0.00% |

## Status de venda

| Status | Linhas | % |
|---|---:|---:|
| FECHADO | 7,883,870 | 93.19% |
| EXCLUIDO | 416,795 | 4.93% |
| CANCELADO | 146,365 | 1.73% |
| INUTILIZADO | 7,474 | 0.09% |
| PENDENTE | 5,566 | 0.07% |
| ABERTO | 4 | 0.00% |

## Quantidade e valor

| Métrica | quantidade | valor |
|---|---:|---:|
| min | 0.5 | 0.0 |
| max | 7908.0 | 713346.4 |
| soma | 12,162,103.11 | R$ 276,879,138.28 |
| negativos | 0 | 0 |
| zeros | 0 | 23 |

## Duplicidades
- Linhas com chave composta `(filial, data_hora, cliente_nome, ean, qtd, valor)` repetida: **55,810**
  - Pode indicar erro de carga ou múltiplas unidades do mesmo item na mesma venda.

## Cardinalidade
- Filial: 17
- Cidade: 2
- Status: 6
- Gênero: 3
- Categoria: 23
- Controle: 3
- Cliente (primeiro nome): 4,361
- Produto (descrição): 75,529
- EAN: 80,650

## Datas de nascimento
- Mínima: `1899-12-30 00:00:00`
- Máxima: `2025-11-06 00:00:00`
  - ⚠️ Há nascimentos antes de 1900 — provavelmente erro.

## Propostas de tratamento (Sprint 2)
1. **Nulos**: tratar caso a caso (ver tabela acima). Cliente sem nome → marcar como `ANONIMO`.
2. **Status `CANCELADO`**: separar em coluna `is_cancelada` e por padrão excluir das análises de faturamento.
3. **Valores negativos**: investigar — podem ser devoluções; manter mas sinalizar.
4. **Nascimentos absurdos**: descartar ou imputar como nulo.
5. **Duplicidades**: agrupar por chave composta + somar quantidade (regra a confirmar).
6. **Padronização textual**: aplicar UPPER + trim em nomes de produto e cidade.
