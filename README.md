# Treinamento de Sprints - Projeto Analise de Vendas (Farmacia)

Projeto de treinamento focado em construcao e acompanhamento de sprints, usando como caso pratico a analise de um dataset de vendas de farmacia (`dataset_vendas.csv`, ~8.4M linhas).

O objetivo principal nao e a analise em si, mas praticar:

- Planejamento de sprint (objetivo, backlog, estimativa)
- Definition of Done (DoD)
- Acompanhamento diario
- Sprint Review e Retrospectiva

## Estrutura do repositorio

```text
.
|-- README.md                  # este arquivo
|-- docs/
|   `-- sprint-01/
|       `-- dicionario_colunas.md
|-- sprints/                   # planejamento de cada sprint
|   |-- sprint-01-eda.md
|   |-- sprint-02-limpeza.md
|   |-- sprint-03-features.md
|   |-- sprint-04-descritiva.md
|   |-- sprint-05-segmentacao.md
|   `-- sprint-06-predicao.md
`-- templates/                 # modelos de cerimonias
    |-- daily.md
    |-- review.md
    `-- retrospectiva.md
```

## Visao geral das sprints

| Sprint | Tema | Entrega principal |
|---|---|---|
| 1 | Analise Exploratoria (EDA) | Documento de EDA |
| 2 | Limpeza e Preparacao dos Dados | Dataset tratado + script reproduzivel |
| 3 | Engenharia de Features e Agregacoes | Tabelas analiticas (cliente, produto, filial, tempo) |
| 4 | Analise Descritiva e Visualizacoes | Dashboard com KPIs |
| 5 | Segmentacao e Analise de Comportamento | Perfis de clientes (RFM/coortes) |
| 6 | Modelagem Preditiva + Entrega Final | Previsao de vendas + apresentacao |

## Sobre o dataset

Vendas de uma rede de farmacias com multiplas filiais. Colunas (sem header):

1. Filial (ex: `FCIA LIDER FILIAL 1`)
2. Cidade (ex: `PALOTINA`)
3. Status da venda (ex: `CANCELADO`)
4. Data/hora da venda
5. Nome do cliente
6. Data de nascimento do cliente
7. Genero
8. Descricao do produto
9. Codigo de barras (EAN)
10. Quantidade
11. Valor
12. Categoria do produto (ex: `GENERICOS 2`, `SIMILARES 1`)
13. Tipo de controle (ex: `SEM CONTROLE`)

## Como usar este repositorio

1. No inicio de cada sprint, leia o arquivo `sprints/sprint-XX-*.md` e ajuste o backlog se necessario.
2. Acompanhe o progresso diariamente usando `templates/daily.md` (copie para uma pasta `logs/` se quiser historico).
3. Ao final, faca a Review e a Retrospectiva usando os templates correspondentes.
4. So comece a proxima sprint depois de fechar a anterior.

## Versionamento de dados com DVC

O arquivo `dataset_vendas.csv` e grande demais para ser enviado direto ao GitHub, entao ele passa a ser rastreado via `DVC`.

Arquivos que devem ir para o Git:

- `dataset_vendas.csv.dvc`
- `.dvc/`
- `.dvcignore`
- `.gitignore`

Fluxo basico para clonar e baixar os dados:

```bash
git clone <repo>
cd treinamento-sprints
dvc pull
```

As instrucoes para configurar o remote no Cloudflare R2 estao em `docs/dvc-r2.md`.
