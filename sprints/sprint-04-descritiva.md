# Sprint 4 — Análise Descritiva e Dashboard

**Duração:** 1 semana
**Objetivo:** Responder perguntas de negócio com visualizações claras e gerar um dashboard interativo.

## Pré-requisitos
- Sprint 3 finalizada com tabelas agregadas disponíveis

## Backlog

### 1. Perguntas de negócio
- [ ] Quais são os top 10 produtos por volume e por faturamento?
- [ ] Como cada categoria contribui no faturamento total?
- [ ] Existe sazonalidade mensal/semanal? Em quais filiais é mais forte?
- [ ] Como as filiais se comparam entre si (volume, ticket, mix)?
- [ ] Qual o perfil demográfico dos clientes (idade, gênero) por filial?

### 2. Visualizações
- [ ] Série temporal de vendas (diária e mensal)
- [ ] Heatmap dia da semana × hora do dia
- [ ] Top produtos / categorias (barras)
- [ ] Comparativo entre filiais (boxplot ou barras)
- [ ] Distribuição demográfica (pirâmide etária ou histograma)

### 3. Dashboard
- [ ] Escolher ferramenta (Streamlit, Power BI, Looker Studio, Metabase)
- [ ] Estruturar em abas/seções por tema
- [ ] Adicionar filtros por filial, período e categoria

### 4. Insights escritos
- [ ] Documentar 5 a 10 insights relevantes a partir do dashboard
- [ ] Indicar quais merecem aprofundamento nas próximas sprints

## Definition of Done

- Dashboard funcional com pelo menos 5 visões
- Filtros operacionais (filial, período, categoria)
- Documento `docs/insights-sprint-04.md` com os insights
- Print/screenshot das telas principais no repositório

## Riscos e atenções

- Não cair na armadilha de "fazer gráfico bonito" sem responder pergunta
- Cuidado com performance: dataset grande pode travar o dashboard sem agregação prévia
