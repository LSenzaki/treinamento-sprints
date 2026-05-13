# Sprint 6 — Modelagem Preditiva + Entrega Final

**Duração:** 1 semana
**Objetivo:** Construir um modelo preditivo simples e fechar o projeto com uma apresentação consolidada.

## Pré-requisitos
- Sprints 3 e 4 finalizadas (features e visões disponíveis)

## Backlog

### 1. Definição do problema
- [ ] Escolher o alvo: previsão de vendas diárias por filial
- [ ] Definir horizonte (ex: 30 dias) e granularidade
- [ ] Separar treino/validação por data (sem vazamento temporal)

### 2. Baseline
- [ ] Média móvel simples (7 e 30 dias)
- [ ] Naïve sazonal (mesmo dia da semana anterior)
- [ ] Calcular métricas: MAE, MAPE, RMSE

### 3. Modelo principal
- [ ] Escolher: Prophet, regressão linear com features temporais, ou árvore (LightGBM)
- [ ] Treinar e validar
- [ ] Comparar com o baseline

### 4. Apresentação final
- [ ] Slide com objetivo do projeto
- [ ] Resumo de cada sprint e principais aprendizados
- [ ] Resultados-chave (insights + métricas do modelo)
- [ ] Próximos passos sugeridos

### 5. Retrospectiva do projeto inteiro
- [ ] O que funcionou bem na construção das sprints?
- [ ] O que mudaria no planejamento?
- [ ] Como foi a estimativa vs. realidade?

## Definition of Done

- Notebook do modelo versionado, com métricas reportadas
- Comparação clara modelo vs. baseline
- Slides ou documento final consolidado
- Retrospectiva do projeto registrada

## Riscos e atenções

- Não tentar usar modelo muito sofisticado se o baseline já resolve bem
- Documentar limitações e quando o modelo NÃO deve ser usado
