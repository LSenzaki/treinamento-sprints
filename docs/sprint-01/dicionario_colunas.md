# Dicionário de Colunas - dataset_vendas.csv

O arquivo `dataset_vendas.csv` não tem cabeçalho. A tabela abaixo nomeia as 13 colunas na ordem em que aparecem no arquivo.

| nome | tipo | descrição | exemplo |
|---|---|---|---|
| filial | texto categórico | Nome da filial ou unidade da rede de farmácias onde a venda foi registrada. | FCIA LIDER FILIAL 1 |
| cidade | texto categórico | Cidade onde a filial está localizada. | PALOTINA |
| status_venda | texto categórico | Situação do registro da venda, indicando se a operação foi concluída, cancelada ou outro estado operacional. | CANCELADO |
| data_hora_venda | data/hora | Data e hora em que a venda foi realizada. | 2015-03-24 09:05:30.997 |
| nome_cliente | texto | Nome do cliente associado à compra. | OLIVIA |
| data_nascimento_cliente | data | Data de nascimento do cliente, útil para análises de faixa etária. | 1950-04-13 00:00:00.000 |
| genero_cliente | texto categórico | Gênero informado no cadastro do cliente. | FEMININO |
| produto_descricao | texto | Descrição comercial do item vendido, normalmente com nome, dose e apresentação. | LOSARTANA POTASSICA 50 MG C/30 CPR |
| ean_produto | texto numérico | Código de barras/EAN do produto, usado para identificação única do item. | 7896714273884 |
| quantidade | número decimal | Quantidade de unidades vendidas no registro. | 1.0000 |
| valor | número decimal | Valor monetário associado ao item vendido, normalmente o total da linha. | 9.00 |
| categoria_produto | texto categórico | Classe comercial do produto, como referência, similar, genérico ou outras categorias da rede. | GENERICOS 2 |
| tipo_controle | texto categórico | Tipo de controle regulatório do produto, indicando se é controlado ou sem controle especial. | SEM CONTROLE |

## Observações

- Os exemplos foram extraídos das primeiras linhas do arquivo.
- As colunas `quantidade` e `valor` aparecem no arquivo com formato decimal, mesmo quando representam contagens ou valores monetários.
- `ean_produto` foi tratado como texto numérico para preservar zeros à esquerda, se existirem em outros registros.