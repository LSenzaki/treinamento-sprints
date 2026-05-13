# Sprint 5 — Segmentação e Análise de Comportamento

**Duração:** 1 semana
**Objetivo:** Entender perfis de comportamento dos clientes para guiar ações futuras (marketing, retenção).

## Pré-requisitos
- Sprint 3 finalizada com métricas RFM disponíveis

## Backlog

### 1. Análise RFM
- [ ] Calcular quartis ou quintis para R, F e M
- [ ] Combinar scores em uma classificação (ex: 555 = melhor cliente)
- [ ] Nomear segmentos derivados (ex: "Campeões", "Em risco", "Hibernando")

### 2. Coortes
- [ ] Definir coortes por mês de primeira compra
- [ ] Calcular retenção mês a mês
- [ ] Visualizar em heatmap

### 3. Clusterização
- [ ] Selecionar features (RFM + idade + categoria preferida)
- [ ] Normalizar features
- [ ] Aplicar K-means (escolher k via silhueta ou elbow)
- [ ] Interpretar e nomear clusters

### 4. Clientes em risco
- [ ] Definir critério de churn (ex: sem compra há > X dias)
- [ ] Listar clientes em risco e seu valor histórico
- [ ] Sugerir ações de retenção

### 5. Relatório
- [ ] Consolidar perfis em um documento
- [ ] Quantificar tamanho e valor de cada segmento

## Definition of Done

- Notebook com análise RFM, coortes e clusterização
- Relatório `docs/segmentacao-clientes.md` com os perfis nomeados
- Tabela com classificação de cada cliente disponível para consumo posterior

## Riscos e atenções

- Identificação de cliente herdada da Sprint 3 — segmentação só é tão boa quanto o ID
- Clusterização é exploratória; não force interpretação se os clusters não fizerem sentido
