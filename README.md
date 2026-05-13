# Treinamento de Sprints — Projeto Análise de Vendas (Farmácia)

Projeto de treinamento focado em **construção e acompanhamento de sprints**, usando como caso prático a análise de um dataset de vendas de farmácia (`dataset_vendas.csv`, ~8.4M linhas).

O objetivo principal **não é a análise em si**, mas praticar:

- Planejamento de sprint (objetivo, backlog, estimativa)
- Definition of Done (DoD)
- Acompanhamento diário
- Sprint Review e Retrospectiva

## Estrutura do repositório

```
.
├── README.md                  # este arquivo
├── sprints/                   # planejamento de cada sprint
│   ├── sprint-01-eda.md
│   ├── sprint-02-limpeza.md
│   ├── sprint-03-features.md
│   ├── sprint-04-descritiva.md
│   ├── sprint-05-segmentacao.md
│   └── sprint-06-predicao.md
└── templates/                 # modelos de cerimônias
    ├── daily.md
    ├── review.md
    └── retrospectiva.md
```

## Visão geral das sprints

| Sprint | Tema | Entrega principal |
|---|---|---|
| 1 | Análise Exploratória (EDA) | Documento de EDA |
| 2 | Limpeza e Preparação dos Dados | Dataset tratado + script reproduzível |
| 3 | Engenharia de Features e Agregações | Tabelas analíticas (cliente, produto, filial, tempo) |
| 4 | Análise Descritiva e Visualizações | Dashboard com KPIs |
| 5 | Segmentação e Análise de Comportamento | Perfis de clientes (RFM/coortes) |
| 6 | Modelagem Preditiva + Entrega Final | Previsão de vendas + apresentação |

## Sobre o dataset

Vendas de uma rede de farmácias com múltiplas filiais. Colunas (sem header):

1. Filial (ex: `FCIA LIDER FILIAL 1`)
2. Cidade (ex: `PALOTINA`)
3. Status da venda (ex: `CANCELADO`)
4. Data/hora da venda
5. Nome do cliente
6. Data de nascimento do cliente
7. Gênero
8. Descrição do produto
9. Código de barras (EAN)
10. Quantidade
11. Valor
12. Categoria do produto (ex: `GENERICOS 2`, `SIMILARES 1`)
13. Tipo de controle (ex: `SEM CONTROLE`)

## Como usar este repositório

1. No início de cada sprint, leia o arquivo `sprints/sprint-XX-*.md` e ajuste o backlog se necessário.
2. Acompanhe o progresso diariamente usando `templates/daily.md` (copie para uma pasta `logs/` se quiser histórico).
3. Ao final, faça a Review e a Retrospectiva usando os templates correspondentes.
4. Só comece a próxima sprint depois de fechar a anterior.
