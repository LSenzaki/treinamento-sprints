# Tratamento de Status — Sprint 2

Objetivo: decidir o que fazer com vendas canceladas e demais status operacionais no dataset.

Contagem de status existentes no arquivo bruto (scan streaming):

| status | contagem | % do total |
|---|---:|---:|
| FECHADO | 7.883.870 | 93,18% |
| EXCLUIDO | 416.795 | 4,93% |
| CANCELADO | 146.365 | 1,73% |
| INUTILIZADO | 7.474 | 0,09% |
| PENDENTE | 5.566 | 0,07% |
| ABERTO | 4 | 0,00% |

Decisão

- Manter apenas `FECHADO` no dataset analítico limpo.
- Separar os demais status como registros operacionais/exception handling, fora das métricas de venda, para evitar inflar faturamento, volume e KPIs.
- Não remover a informação conceitual do domínio: a regra continua explícita em `clean.py` e pode ser reaproveitada em uma trilha de auditoria ou em uma base de exceções, se necessário.

Impacto da decisão

- Linhas mantidas no dataset analítico: 7.883.870.
- Linhas removidas do dataset analítico por status: 576.204.
- Percentual removido: 6,81%.

Justificativa

- `CANCELADO`, `EXCLUIDO`, `INUTILIZADO`, `PENDENTE` e `ABERTO` não representam venda concluída, então não devem entrar em métricas de receita, ticket médio ou volume vendido.
- A presença desses estados é útil para auditoria operacional, mas misturá-los com vendas fechadas distorce qualquer análise de performance comercial.

Regra aplicada em `clean.py`

- Linhas com `status_venda` diferente de `FECHADO` são descartadas da saída principal.
- A validação final garante que todo registro de saída tenha `status_venda == FECHADO`.
