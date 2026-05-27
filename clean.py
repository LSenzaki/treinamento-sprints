import csv
import hashlib
import os

NULL_TOKENS = {'', 'NULL', 'NaN', 'N/D', 'NA', 'None', '-'}

def is_null(val):
    if val is None:
        return True
    return val.strip() in NULL_TOKENS

def hash_cliente(name: str) -> str:
    s = name.strip().lower()
    return hashlib.sha1(s.encode('utf-8')).hexdigest()

def clean_stream(in_path='dataset_vendas.csv', out_path='dataset_vendas_clean.csv'):
    """Lê em streaming e aplica regras de tratamento de nulos conforme sprint-02/nulos.md.

    Regras aplicadas (resumo):
    - descartar linhas sem `data_hora_venda`.
    - anonimizar `nome_cliente` -> `cliente_id` (SHA1); quando ausente deixar vazio e marcar flag.
    - imputar `quantidade` -> '1.0000' quando ausente; `valor` -> '0.00' quando ausente.
    - marcar `filial`/`cidade`/`genero_cliente` ausentes com 'UNKNOWN' ou 'DESCONHECIDO'.
    - manter demais colunas e acrescentar flags no final do registro para rastreabilidade.
    """
    with open(in_path, 'r', encoding='utf-8', errors='replace', newline='') as inf, \
         open(out_path, 'w', encoding='utf-8', newline='') as outf:
        reader = csv.reader(inf, delimiter=';')
        writer = csv.writer(outf, delimiter=';')

        # The source file has no header; use position indexes based on sprint-01/dicionario_colunas.md
        cols = ['filial','cidade','status_venda','data_hora_venda','nome_cliente','data_nascimento_cliente','genero_cliente','produto_descricao','ean_produto','quantidade','valor','categoria_produto','tipo_controle']
        # output header: replace nome_cliente with cliente_id and append flags
        out_header = cols.copy()
        out_header[out_header.index('nome_cliente')] = 'cliente_id'
        out_header += ['filial_missing','cidade_missing','data_nascimento_missing','ean_missing','quantidade_imputada','valor_imputado','cliente_missing']
        writer.writerow(out_header)

        for row in reader:
            # pad short rows
            if len(row) < len(cols):
                row += [''] * (len(cols) - len(row))

            # map
            rec = dict(zip(cols, row))

            # flags
            filial_missing = '0'
            cidade_missing = '0'
            data_nascimento_missing = '0'
            ean_missing = '0'
            quantidade_imputada = '0'
            valor_imputado = '0'
            cliente_missing = '0'

            # data_hora_venda: if missing discard
            if is_null(rec['data_hora_venda']):
                continue

            # filial
            if is_null(rec['filial']):
                rec['filial'] = 'UNKNOWN'
                filial_missing = '1'

            # cidade
            if is_null(rec['cidade']):
                rec['cidade'] = 'UNKNOWN'
                cidade_missing = '1'

            # status_venda
            if is_null(rec['status_venda']):
                rec['status_venda'] = 'DESCONHECIDO'

            # nome_cliente -> cliente_id (anonimizar)
            if is_null(rec['nome_cliente']):
                cliente_missing = '1'
                cliente_id = ''
            else:
                cliente_id = hash_cliente(rec['nome_cliente'])

            # data_nascimento_cliente
            if is_null(rec['data_nascimento_cliente']):
                data_nascimento_missing = '1'

            # genero
            if is_null(rec['genero_cliente']):
                rec['genero_cliente'] = 'DESCONHECIDO'

            # produto_descricao
            if is_null(rec['produto_descricao']):
                rec['produto_descricao'] = 'UNKNOWN_PRODUCT'

            # ean_produto
            if is_null(rec['ean_produto']):
                ean_missing = '1'

            # quantidade
            if is_null(rec['quantidade']):
                rec['quantidade'] = '1.0000'
                quantidade_imputada = '1'

            # valor
            if is_null(rec['valor']):
                rec['valor'] = '0.00'
                valor_imputado = '1'

            out_row = [rec[c] if c != 'nome_cliente' else cliente_id for c in cols]
            out_row += [filial_missing,cidade_missing,data_nascimento_missing,ean_missing,quantidade_imputada,valor_imputado,cliente_missing]
            writer.writerow(out_row)

def main():
    in_path = os.environ.get('INPUT_CSV','dataset_vendas.csv')
    out_path = os.environ.get('OUTPUT_CSV','dataset_vendas_clean.csv')
    clean_stream(in_path, out_path)

if __name__ == '__main__':
    main()
