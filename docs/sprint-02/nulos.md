# Tratamento de Nulos — Sprint 2

Este documento lista a estratégia definida para cada coluna do `dataset_vendas.csv` e o impacto (nº de linhas afetadas) detectado por uma contagem em streaming.

Resumo da contagem (scan streaming):

- Total de linhas processadas: 8.460.073

Contagem de nulos por coluna (ordem original do arquivo):

| coluna | nulos detectados | % do total | estratégia escolhida |
|---|---:|---:|---|
| filial | 0 | 0.00% | Marcar (`UNKNOWN`) + flag `filial_missing` |
| cidade | 0 | 0.00% | Marcar (`UNKNOWN`) + flag `cidade_missing` |
| status_venda | 0 | 0.00% | Marcar (`DESCONHECIDO`) |
| data_hora_venda | 0 | 0.00% | Descartar linhas sem `data_hora_venda` (não são úteis para séries temporais) |
| nome_cliente | 0 | 0.00% | Anonimizar: gerar `cliente_id` hashed; manter flag `cliente_missing` quando ausente |
| data_nascimento_cliente | 1 | 0.00% | Marcar (manter nulo) + flag `data_nascimento_missing` — não imputar idade automaticamente |
| genero_cliente | 0 | 0.00% | Marcar (`DESCONHECIDO`) |
| produto_descricao | 0 | 0.00% | Marcar (`UNKNOWN_PRODUCT`) e normalizar na dimensão `products` |
| ean_produto | 101 | 0.0012% | Marcar (manter nulo/flag `ean_missing`) — tentar lookup na dimensão de produtos na Sprint 2 |
| quantidade | 0 | 0.00% | Imputar padrão `1.0000` quando ausente e registrar `quantidade_imputada` |
| valor | 0 | 0.00% | Imputar `0.00` quando ausente e registrar `valor_imputado` |
| categoria_produto | 0 | 0.00% | Marcar (`SEM_CATEGORIA`) |
| tipo_controle | 0 | 0.00% | Marcar (`SEM_CONTROLE`) |

Observações:

- A contagem foi obtida por leitura em streaming; o primeiro registro do arquivo foi interpretado como linha de dados (o arquivo não possui cabeçalho). Os números apresentados vêm do scan e foram salvos como referência para as próximas tarefas.
- Impacto relevante: `ean_produto` tem 101 registros ausentes — estes exigirão lookup/manual review antes de depender exclusivamente do EAN para junções.
- `data_hora_venda` é crucial para análises temporais; linhas sem essa informação devem ser descartadas.

Próximos passos implementáveis na Sprint 2:

- Executar rotina de anonimização e substituir `nome_cliente` por `cliente_id` hashed (SHA1). Implementado inicialmente em `clean.py` como opção.
- Construir dimensão `products` e tentar preencher os 101 `ean` ausentes via heurísticas/text-matching.
- Rodar `clean.py` em amostra e validar contagens pós-limpeza antes de aplicar em todo o dataset.

Arquivo(s): `scripts/count_nulls.py` (contagem), `clean.py` (implementação do tratamento).
