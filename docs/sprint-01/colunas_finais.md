# Relevância das Colunas — Sprint 1

Decisão sobre quais colunas manter para as próximas sprints.

| Coluna | Manter? | Justificativa |
|---|---|---|
| `filial` | ✅ | Chave primária de segmentação |
| `cidade` | ✅ | Derivável de `filial` mas útil para visões geográficas |
| `status_venda` | ✅ | Necessária para filtrar `CANCELADO` |
| `data_hora` | ✅ | Base para todas as análises temporais |
| `cliente_nome` | ⚠️ | Manter, mas saber que **não é um ID único** (homônimos) |
| `cliente_nascimento` | ✅ | Permite calcular idade — feature importante na Sprint 3 |
| `cliente_genero` | ✅ | Demografia |
| `produto_descricao` | ✅ | Mix de produto |
| `produto_ean` | ✅ | Chave mais confiável que descrição para produto |
| `quantidade` | ✅ | Métrica |
| `valor` | ✅ | Métrica |
| `categoria` | ✅ | Análises agregadas |
| `controle` | ⚠️ | Avaliar utilidade real — alta concentração em um único valor pode torná-la pouco informativa |

## Conclusão
- Não há colunas para remover de saída.
- `controle` deve ser reavaliada após Sprint 2 com base na cardinalidade efetiva.
- `cliente_nome` precisa ser combinada com `cliente_nascimento` para criar um ID estável de cliente na Sprint 3.
