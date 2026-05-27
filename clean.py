import csv
import hashlib
import os
import sys
from pathlib import Path
from datetime import datetime
from decimal import Decimal, InvalidOperation

_field_limit = 2 ** 31 - 1
while True:
    try:
        csv.field_size_limit(_field_limit)
        break
    except OverflowError:
        _field_limit //= 10

NULL_TOKENS = {'', 'NULL', 'NaN', 'N/D', 'NA', 'None', '-'}
KEEP_STATUS = 'FECHADO'

def is_null(val):
    if val is None:
        return True
    return val.strip() in NULL_TOKENS

def hash_cliente(name: str) -> str:
    s = name.strip().lower()
    return hashlib.sha1(s.encode('utf-8')).hexdigest()

def parse_datetime(value: str) -> str:
    text = value.strip()
    if is_null(text):
        raise ValueError('datetime vazio')
    for fmt in ('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M:%S.%f', '%d/%m/%Y %H:%M:%S'):
        try:
            return datetime.strptime(text, fmt).strftime('%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            continue
    raise ValueError(f'datetime invalido: {value!r}')

def parse_decimal(value: str, default: str | None = None) -> str:
    text = value.strip()
    if is_null(text):
        if default is None:
            raise ValueError('decimal vazio')
        text = default
    text = text.replace('.', '').replace(',', '.') if text.count(',') == 1 and text.count('.') > 1 else text.replace(',', '.')
    try:
        return format(Decimal(text), 'f')
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f'decimal invalido: {value!r}') from exc

def clean_stream(in_path='dataset_vendas.csv', out_path='dataset_vendas_clean.csv'):
    """Lê em streaming e aplica regras de tratamento de nulos conforme sprint-02/nulos.md.

    Regras aplicadas (resumo):
    - descartar linhas sem `data_hora_venda`.
    - anonimizar `nome_cliente` -> `cliente_id` (SHA1); quando ausente deixar vazio e marcar flag.
    - imputar `quantidade` -> '1.0000' quando ausente; `valor` -> '0.00' quando ausente.
    - marcar `filial`/`cidade`/`genero_cliente` ausentes com 'UNKNOWN' ou 'DESCONHECIDO'.
    - manter demais colunas e acrescentar flags no final do registro para rastreabilidade.
    """
    stats = {
        'rows_in': 0,
        'rows_out': 0,
        'rows_dropped_status': 0,
        'datetime_converted': 0,
        'valor_converted': 0,
        'quantidade_converted': 0,
        'bom_removed': 0,
        'type_errors': 0,
    }

    with open(in_path, 'r', encoding='utf-8-sig', errors='replace', newline='') as inf, \
         open(out_path, 'w', encoding='utf-8', newline='') as outf:
        reader = csv.reader(inf, delimiter=';')
        writer = csv.writer(outf, delimiter=';')

        # The source file has no header; use position indexes based on sprint-01/dicionario_colunas.md
        cols = ['filial','cidade','status_venda','data_hora_venda','nome_cliente','data_nascimento_cliente','genero_cliente','produto_descricao','ean_produto','quantidade','valor','categoria_produto','tipo_controle']
        # output header: replace nome_cliente with cliente_id and append flags
        out_header = cols.copy()
        out_header[out_header.index('nome_cliente')] = 'cliente_id'
        out_header[out_header.index('data_hora_venda')] = 'data_hora_venda'
        out_header += ['filial_missing','cidade_missing','data_nascimento_missing','ean_missing','quantidade_imputada','valor_imputado','cliente_missing']
        writer.writerow(out_header)

        for row in reader:
            stats['rows_in'] += 1
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

            try:
                rec['data_hora_venda'] = parse_datetime(rec['data_hora_venda'])
                stats['datetime_converted'] += 1
            except ValueError:
                stats['type_errors'] += 1
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

            if rec['status_venda'].strip().upper() != KEEP_STATUS:
                stats['rows_dropped_status'] += 1
                continue

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
            try:
                rec['quantidade'] = parse_decimal(rec['quantidade'])
                stats['quantidade_converted'] += 1
            except ValueError:
                stats['type_errors'] += 1
                continue

            # valor
            if is_null(rec['valor']):
                rec['valor'] = '0.00'
                valor_imputado = '1'
            try:
                rec['valor'] = parse_decimal(rec['valor'])
                stats['valor_converted'] += 1
            except ValueError:
                stats['type_errors'] += 1
                continue

            out_row = [rec[c] if c != 'nome_cliente' else cliente_id for c in cols]
            out_row += [filial_missing,cidade_missing,data_nascimento_missing,ean_missing,quantidade_imputada,valor_imputado,cliente_missing]
            writer.writerow(out_row)
            stats['rows_out'] += 1

    return stats

def validate_output(path: str):
    with open(path, 'r', encoding='utf-8', newline='') as fh:
        reader = csv.DictReader(fh, delimiter=';')
        required = {'data_hora_venda', 'quantidade', 'valor'}
        if not required.issubset(reader.fieldnames or []):
            raise AssertionError(f'colunas obrigatorias ausentes: {required - set(reader.fieldnames or [])}')
        checked = 0
        for row in reader:
            checked += 1
            datetime.strptime(row['data_hora_venda'], '%Y-%m-%d %H:%M:%S.%f')
            Decimal(row['quantidade'])
            Decimal(row['valor'])
            if row['status_venda'].strip().upper() != KEEP_STATUS:
                raise AssertionError(f"status inesperado na saida: {row['status_venda']!r}")
        return checked

def main():
    base_dir = Path(__file__).resolve().parent
    in_path = Path(os.environ.get('INPUT_CSV', str(base_dir / 'dataset_vendas.csv')))
    if not in_path.is_absolute():
        in_path = (base_dir / in_path).resolve()
    out_path = Path(os.environ.get('OUTPUT_CSV', str(base_dir / 'dataset_vendas_clean.csv')))
    if not out_path.is_absolute():
        out_path = (base_dir / out_path).resolve()
    stats = clean_stream(in_path, out_path)
    checked = validate_output(out_path)
    print(f"rows_in={stats['rows_in']} rows_out={stats['rows_out']} dropped_status={stats['rows_dropped_status']} checked={checked} datetime_converted={stats['datetime_converted']} quantidade_converted={stats['quantidade_converted']} valor_converted={stats['valor_converted']} type_errors={stats['type_errors']}")

if __name__ == '__main__':
    main()
