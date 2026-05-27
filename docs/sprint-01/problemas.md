# Problemas de Qualidade - dataset_vendas.csv

Resumo rápido das métricas usadas: linhas lidas = 8.460.074

| Indicador | Valor |
|---|---:|
| Linhas | 8.460.074 |
| Datas inválidas | 0 |
| Quantidades negativas | 0 |
| Valores negativos | 0 |
| Missing EAN (coluna 9) | 101 (0.001194%) |
| Qtde min / max | 0.5 / 7.908 |
| Valor min / max | R$ 0,00 / R$ 713.346,40 |
| Status encontrados | FECHADO, EXCLUIDO, CANCELADO, INUTILIZADO, PENDENTE, ABERTO |

## Lista de problemas detectados

1. Falta de EAN (coluna 9)
- Descrição: 101 linhas sem EAN (~0.0012% do arquivo).
- Impacto: impede identificação única de produto para joins, agregações por SKU e grupo de preço; pode causar perda em análises por produto.
- Tratamento proposto: tentar inferir EAN a partir de `produto_descricao` (lookup/manual); preencher como `NULL` e marcar/filtrar registros sem EAN em análises por SKU; registrar para coleta/limpeza na Sprint 2.

2. Outliers de quantidade
- Descrição: quantidade varia de 0.5 até 7.908 unidades; existem valores muito altos (ex.: 7.908).
- Impacto: médias e KPIs por venda ficam fortemente enviesados; pode indicar vendas por caixa, pacotes, ajustes ou erros de importação.
- Tratamento proposto: investigar os top N registros por `quantidade` e `valor` (correlações com `produto_descricao` e filiais com '(TRANS)'). Tratar em três frentes: (a) separar transações de transferência/atacado; (b) corrigir erros de importação; (c) aplicar winsorize/cap para modelagem, mantendo cópia dos dados brutos.

3. Outliers de valor
- Descrição: valores unitários/linha chegam até R$ 713.346,40; existência de linhas com R$ > 100k.
- Impacto: afeta somas, médias e modelos de regressão; pode representar vendas corporativas, notas consolidadas, devoluções com sinal negativo (não observadas) ou erros.
- Tratamento proposto: inspecionar as maiores linhas de `valor` e checar se `quantidade * unit_price` faz sentido; separar e documentar casos legítimos (ex: venda de equipamento) e remover/ajustar erros.

4. Status múltiplos e necessidade de padronização
- Descrição: status presentes: `'FECHADO'` (93.19%), `'EXCLUIDO'` (4.93%), `'CANCELADO'` (1.73%), `'INUTILIZADO'`, `'PENDENTE'`, `'ABERTO'`.
- Impacto: análises de vendas devem considerar apenas vendas efetivas; registros com outros status podem inflar contagens se não filtrados.
- Tratamento proposto: definir mapa de statuses (ex.: `FECHADO` -> `realizada`; `CANCELADO|EXCLUIDO|INUTILIZADO` -> `descartada`; `PENDENTE|ABERTO` -> `pendente`). Para análise de vendas usar apenas `realizada` por padrão, manter os demais para auditoria e análise operacional.

5. Alta cardinalidade em descrições e códigos
- Descrição: `produto_descricao` ~75k valores únicos; `ean_produto` ~80k; `data_hora_venda` ~4.7M timestamps únicos.
- Impacto: agrupamentos por produto/texto são custosos e arriscam ruído (descrições levemente diferentes representam o mesmo SKU).
- Tratamento proposto: construir dimensão de produtos (`product_id`) normalizando EAN+descrição (limpeza de texto, remoção de variações de apresentação), agrupar por famílias (categoria_produto) para análises de alto nível.

6. Quantidades fracionárias (ex.: 0.5)
- Descrição: existem quantidades não inteiras (mínimo 0.5).
- Impacto: pode ser válido (medida, peso, fracionamento) ou indicar inconsistência na unidade medida.
- Tratamento proposto: mapear por `categoria_produto`/`produto_descricao` se fracionamento é esperado; padronizar unidades ou criar flag `fracionado` e converter para unidade padronizada quando possível.

7. Filiais com sufixo '(TRANS)' e lojas com volume muito baixo
- Descrição: existem filiais marcadas como `(TRANS)` e filiais com volumes extremamente baixos (ex.: `L A CONVENIENCIA` com 398 registros).
- Impacto: registros de transferência/convênio podem não representar venda final ao cliente e devem ser tratados separadamente.
- Tratamento proposto: identificar e separar `filial` com `(TRANS)` ou outras tags operacionais; considerar exclusão destas linhas do KPI de vendas no varejo ou tratá-las como operação distinta.

## Próximos passos (input para Sprint 2)
- Implementar script de amostragem para inspecionar top-100 valores de `valor` e `quantidade` e validar a origem (produto, filial, status).
- Normalizar `produto_descricao` e criar dimensão de produto com `ean_produto` como chave primária sempre que disponível.
- Criar rotina de padronização de `status` e aplicar filtro `FECHADO` para análises de vendas.
- Documentar regras finais de inclusão/exclusão (transfers, convênios, devoluções) e executar a limpeza incremental.

***

Arquivo gerado automaticamente pela análise de qualidade — use como checklist para a Sprint 2.
