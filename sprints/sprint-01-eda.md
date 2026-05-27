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
- [x] Listar quantas filiais existem
- [x] Comparar volume/perfil entre filiais
- [x] Decidir se a análise deve ser por filial ou agregada — justificar

#### Resumo comparativo

Foram identificadas **17 filiais**. A distribuição de volume é bastante desigual: as maiores unidades concentram a maior parte dos registros, enquanto algumas filiais têm volume muito baixo. O ticket médio também varia bastante entre unidades, então a filial funciona melhor como um recorte analítico do que como a principal unidade de análise.

| filial | registros | total_vendas | ticket_medio |
|---|---:|---:|---:|
| FCIA LIDER FILIAL 3 | 2.544.448 | R$ 85.013.580,38 | R$ 33,41 |
| FCIA LIDER FILIAL 1 | 1.961.100 | R$ 76.646.878,35 | R$ 39,08 |
| FCIA LIDER MATRIZ | 666.335 | R$ 22.741.352,43 | R$ 34,13 |
| FCIA LIDER FILIAL 4 | 518.979 | R$ 14.925.175,88 | R$ 28,76 |
| FCIA LIDER FILIAL 7 | 469.975 | R$ 11.228.514,27 | R$ 23,89 |
| FCIA LIDER FILIAL 14 | 104.659 | R$ 4.358.286,38 | R$ 41,64 |
| FARMACIA VIVER PREV FILIAL 8 -  (TRANS) | 105.806 | R$ 2.380.005,30 | R$ 22,49 |
| GUARAPUAVA (TRANS) | 13.715 | R$ 600.935,46 | R$ 43,82 |
| CLEVELANDIA  (TRANS) | 21.951 | R$ 169.776,27 | R$ 7,73 |
| L A CONVENIENCIA  | 398 | R$ 53.415,21 | R$ 134,21 |

#### Decisão

A análise deve ser **agregada no nível da rede**, com a filial usada como dimensão de segmentação e comparação. Isso evita que unidades muito pequenas distorçam a leitura geral e permite comparar desempenho entre lojas apenas quando houver necessidade de detalhamento por unidade.

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
