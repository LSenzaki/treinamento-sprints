# Sprint 2 — Limpeza e Preparação

**Duração:** 1 semana
**Objetivo:** Transformar o CSV bruto em um dataset confiável e reproduzível, pronto para análise.

## Pré-requisitos
- Sprint 1 finalizada com lista de problemas mapeados

## Backlog

### 1. Tratamento de nulos
- [ ] Decidir estratégia por coluna (imputar, descartar linha, marcar como "desconhecido")
- [ ] Documentar a decisão e o impacto (quantas linhas afetadas)

### 2. Padronização de tipos
- [ ] Datas para `datetime`
- [ ] Valores monetários com vírgula → ponto, tipo `float`
- [ ] Resolver encoding/BOM no cabeçalho

### 3. Tratamento de status
- [ ] Decidir o que fazer com vendas `CANCELADO` (manter? separar? remover?)
- [ ] Verificar outros status existentes

### 4. Deduplicação e outliers
- [ ] Identificar linhas duplicadas
- [ ] Tratar quantidades e preços negativos ou absurdos
- [ ] Definir regra para outliers (descartar vs. winsorizar)

### 5. Padronização textual
- [x] Nome de produto (maiúsculas/minúsculas, espaços extras) — `normalize_text` em `clean.py`
- [x] Cidades e filiais (consistência de grafia) — idem
- [x] Categoria do produto — idem
- [x] Comparação antes/depois documentada em `docs/sprint-02/padronizacao_textual.md`

### 6. Script reproduzível
- [x] `clean.py` recebe CSV bruto e gera CSV (+ parquet opcional) limpo
- [x] Log JSON estruturado (`clean_log.json`) com contagens por etapa
- [x] README atualizado com instruções de execução

## Definition of Done

- Script `clean.py` reproduzível e versionado
- Dataset limpo salvo (CSV ou parquet)
- Log de transformações com contagem de linhas afetadas em cada etapa
- README atualizado com instruções de execução

## Riscos e atenções

- Não jogar fora dados sem antes documentar a regra
- Verificar se o tratamento mantém a comparabilidade entre filiais
