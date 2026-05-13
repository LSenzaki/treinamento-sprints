# Sprint 1 — Análise Exploratória (EDA)

**Duração:** 1 semana
**Objetivo:** Entender o dataset bruto antes de qualquer tratamento. Sair com um documento que descreva o que existe, o que falta e o que pode ser descartado.

## Backlog

### 1. Declaração das Colunas
- [ ] Nomear cada coluna de acordo com seu significado
- [ ] Identificar o tipo (texto, número, data, etc.)
- [ ] Documentar o contexto de cada coluna para o domínio de farmácias

### 2. Cobertura do Arquivo
- [ ] Identificar o período que o arquivo engloba (dias, meses, anos?)
- [ ] Levantar insights iniciais (ex: média de vendas por dia, consistência temporal)

### 3. Filiais
- [ ] Listar quantas filiais existem
- [ ] Comparar volume/perfil entre filiais
- [ ] Decidir se a análise deve ser por filial ou agregada — justificar

### 4. Inconsistência de Dados
- [ ] Verificar consistência geral (datas inválidas, valores negativos)
- [ ] Identificar nulos e ausentes por coluna
- [ ] Avaliar cardinalidade dos campos categóricos

### 5. Relevância das Colunas
- [ ] Avaliar se todas as colunas são úteis para os objetivos do projeto
- [ ] Justificar exclusões propostas

## Definition of Done

- Documento de EDA escrito (markdown ou notebook) cobrindo todos os itens acima
- Tabela com nome, tipo e descrição de cada coluna
- Lista de problemas encontrados (input para a Sprint 2)
- Decisão registrada sobre análise por filial vs. agregada

## Riscos e atenções

- Dataset tem ~8.4M linhas; cuidado com `pandas.read_csv` sem `chunksize` ou tipos
- Arquivo usa `;` como separador e tem BOM no header
