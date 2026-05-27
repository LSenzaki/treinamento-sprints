 # Colunas finais — manter ou remover

 Objetivo: decidir o que deve seguir para as próximas sprints (engenharia de features, modelagem e análises).

 Resumo das 13 colunas originais (decisão):

 | coluna | decisão | justificativa |
 |---|---|---|
 | filial | Manter | Unidade analítica importante — usado para comparar desempenho entre lojas; alta prioridade em análises operacionais. |
 | cidade | Manter | Útil para análises territoriais e agrupamento quando filial não for desejada. |
 | status_venda | Manter | Necessário para filtrar apenas vendas efetivas (`FECHADO`) e para auditoria. |
 | data_hora_venda | Manter | Essencial para séries temporais, sazonalidade e agregações por dia/mês. |
 | nome_cliente | Remover/Anonymizar | Nome em texto livre é PII e tem alta cardinalidade; substituir por `cliente_id` (hash) ou manter apenas para auditoria em tabela separada. |
 | data_nascimento_cliente | Manter | Permite calcular idade/faixa etária — relevante para segmentação. |
 | genero_cliente | Manter | Variável demográfica útil para segmentação e análises RFM/coortes. |
 | produto_descricao | Manter (mover para dimensão) | Alta cardinalidade e ruído; manter na dimensão de produtos normalizada (`product_id`) e usar `ean_produto`/`product_id` nas tabelas analíticas. |
 | ean_produto | Manter | Chave padrão para identificar SKU; preferir como chave para junções após limpeza. |
 | quantidade | Manter | Métrica fundamental; investigar fracionamento (0.5) e padronizar unidade. |
 | valor | Manter | Métrica financeira central; investigar outliers e registros consolidados. |
 | categoria_produto | Manter | Útil para agregações e redução de dimensionalidade; manter como feature. |
 | tipo_controle | Manter | Importante para análise de produtos regulados vs. sem controle; manter. |

 Colunas candidatas a remoção ou transformação

 - `nome_cliente`: não manter o nome em tabelas analíticas. Ação recomendada: gerar `cliente_id = sha1(lower(trim(nome_cliente)))` (ou usar um id já existente) e remover o campo `nome_cliente` das tabelas de consumo/feature store; manter cópia redigida em arquivo seguro apenas para auditoria/PKI.
 - `produto_descricao`: não remover dos dados brutos, mas normalizar e migrar para uma dimensão `products(product_id, ean, descricao_normalizada, categoria)`; nas tabelas fact usar `product_id` (reduz cardinalidade e ruído).

 Validação com EDA

 - A EDA mostrou que `produto_descricao` e `ean_produto` têm alta cardinalidade (~75-80k), justificando a dimensão de produto.
 - Há 101 linhas sem EAN — esses devem ser tratados/lookup antes de confiar apenas em `ean_produto`.
 - Status tem vários valores; por padrão usar apenas `FECHADO` para métricas de venda realizadas.
 - Existem outliers de `quantidade` e `valor` (ex.: quantidade até 7.908, valor até R$ 713k) — manter `quantidade`/`valor` mas criar regras de validação/flags e amostra/inspeção na Sprint 2.

 Recomendações de implementação (Sprint 2)

 - Criar rotina de anonimização para clientes e substituir `nome_cliente` por `cliente_id` na fact table.
 - Construir dimensão `products` a partir de `ean_produto` + `produto_descricao` com processos de normalização (regex para dose/presentação, lower/strip, remover caracteres especiais).
 - Padronizar `quantidade` (unidade) e adicionar flag `is_fractional` quando aplicável.
 - Criar `sales_fact` com colunas minimalistas: `sale_id, datetime, filial, product_id, cliente_id, quantidade, valor, status, categoria_produto, tipo_controle`.

 Decisão final: manter 12/13 colunas transformadas — remover o campo `nome_cliente` bruto das tabelas analíticas e substituí-lo por `cliente_id` anonimizado; manter todas as demais colunas (com product dimension para reduzir ruído).

 Arquivo gerado automaticamente a partir da EDA e das análises de qualidade; servir como input para Sprint 2.
