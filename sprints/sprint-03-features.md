# Sprint 3 — Engenharia de Features e Agregações

**Duração:** 1 semana
**Objetivo:** Criar as tabelas analíticas que vão alimentar dashboards e modelos nas próximas sprints.

## Pré-requisitos
- Sprint 2 finalizada com dataset limpo disponível

## Backlog

### 1. Features de cliente
- [ ] Calcular `idade` a partir da data de nascimento
- [ ] Criar `faixa_etaria` (ex: 0-17, 18-29, 30-44, 45-59, 60+)
- [ ] Identificador único de cliente (avaliar se nome basta ou precisa combinar com nascimento)

### 2. Features temporais
- [ ] Dia da semana, mês, trimestre, ano
- [ ] Flag de fim de semana e feriado
- [ ] Hora do dia / período (manhã, tarde, noite)

### 3. Tabelas agregadas
- [ ] `vendas_por_filial_dia` (filial, data, qtd vendas, faturamento, ticket médio)
- [ ] `vendas_por_produto` (produto, qtd vendida, faturamento, nº de filiais)
- [ ] `vendas_por_cliente` (cliente, recência, frequência, valor)

### 4. Métricas RFM
- [ ] Recência (dias desde a última compra)
- [ ] Frequência (nº de compras no período)
- [ ] Valor monetário (soma do valor gasto)

### 5. Dicionário de dados
- [ ] Documentar cada feature criada: descrição, tipo, regra de cálculo

## Definition of Done

- Tabelas agregadas salvas em parquet
- Dicionário de dados versionado (`docs/data_dictionary.md`)
- Notebook ou script que gera todas as features de forma reproduzível

## Riscos e atenções

- Cuidado com vazamento temporal ao calcular features (definir uma data de corte clara)
- Identificação de cliente pode ter ambiguidades (homônimos)
