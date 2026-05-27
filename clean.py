"""Pipeline de limpeza do dataset_vendas.csv.

Executa em streaming sobre o CSV bruto e produz:
- CSV limpo (sempre)
- Parquet limpo (opcional, --parquet)
- Log JSON com contagens de linhas alteradas/removidas e comparativo
  antes/depois de valores unicos para colunas textuais.

Regras aplicadas (resumo):
- Descartar linhas sem `data_hora_venda` ou com `status_venda` != FECHADO.
- Anonimizar `nome_cliente` -> `cliente_id` (SHA1).
- Imputar `quantidade` (1.0000) e `valor` (0.00) ausentes; marcar flags.
- Normalizar textos: produto_descricao, cidade, filial, categoria_produto
  (strip, colapso de espacos, uppercase, remocao de acentos).
- Marcar campos ausentes com UNKNOWN / DESCONHECIDO e flags por coluna.
"""
import argparse
import csv
import hashlib
import json
import os
import sys
import unicodedata
from pathlib import Path
from datetime import datetime, timezone
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
TEXT_COLUMNS = ('produto_descricao', 'cidade', 'filial', 'categoria_produto')

COLS = [
    'filial', 'cidade', 'status_venda', 'data_hora_venda', 'nome_cliente',
    'data_nascimento_cliente', 'genero_cliente', 'produto_descricao',
    'ean_produto', 'quantidade', 'valor', 'categoria_produto', 'tipo_controle',
]


def is_null(val):
    if val is None:
        return True
    return val.strip() in NULL_TOKENS


def hash_cliente(name: str) -> str:
    s = name.strip().lower()
    return hashlib.sha1(s.encode('utf-8')).hexdigest()


def normalize_text(value: str) -> str:
    """Padroniza texto para evitar duplicidade semantica.

    Etapas: strip, colapso de espacos internos, uppercase, remocao de acentos.
    Aplicada a colunas categoricas (produto, cidade, filial, categoria).
    """
    if value is None:
        return ''
    text = value.strip()
    if not text:
        return ''
    text = ' '.join(text.split())
    text = text.upper()
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(ch for ch in text if not unicodedata.combining(ch))
    return text


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


def build_out_header():
    out_header = COLS.copy()
    out_header[out_header.index('nome_cliente')] = 'cliente_id'
    out_header += [
        'filial_missing', 'cidade_missing', 'data_nascimento_missing',
        'ean_missing', 'quantidade_imputada', 'valor_imputado', 'cliente_missing',
    ]
    return out_header


def clean_stream(in_path: str, out_csv_path: str):
    """Le em streaming, aplica regras e grava CSV limpo. Retorna stats."""
    stats = {
        'rows_in': 0,
        'rows_out': 0,
        'rows_dropped_no_datetime': 0,
        'rows_dropped_status': 0,
        'rows_dropped_type_error': 0,
        'datetime_converted': 0,
        'valor_converted': 0,
        'quantidade_converted': 0,
        'valor_imputado': 0,
        'quantidade_imputada': 0,
        'filial_missing': 0,
        'cidade_missing': 0,
        'data_nascimento_missing': 0,
        'ean_missing': 0,
        'cliente_missing': 0,
        'text_normalized_changed': {c: 0 for c in TEXT_COLUMNS},
    }
    unique_before = {c: set() for c in TEXT_COLUMNS}
    unique_after = {c: set() for c in TEXT_COLUMNS}

    out_header = build_out_header()

    with open(in_path, 'r', encoding='utf-8-sig', errors='replace', newline='') as inf, \
         open(out_csv_path, 'w', encoding='utf-8', newline='') as outf:
        reader = csv.reader(inf, delimiter=';')
        writer = csv.writer(outf, delimiter=';')
        writer.writerow(out_header)

        for row in reader:
            stats['rows_in'] += 1
            if len(row) < len(COLS):
                row += [''] * (len(COLS) - len(row))

            rec = dict(zip(COLS, row))

            # snapshot textual antes da normalizacao (apenas valores nao nulos)
            for c in TEXT_COLUMNS:
                raw = rec.get(c, '')
                if not is_null(raw):
                    unique_before[c].add(raw)

            # data_hora_venda obrigatorio
            if is_null(rec['data_hora_venda']):
                stats['rows_dropped_no_datetime'] += 1
                continue
            try:
                rec['data_hora_venda'] = parse_datetime(rec['data_hora_venda'])
                stats['datetime_converted'] += 1
            except ValueError:
                stats['rows_dropped_type_error'] += 1
                continue

            # status_venda
            if is_null(rec['status_venda']):
                rec['status_venda'] = 'DESCONHECIDO'
            if rec['status_venda'].strip().upper() != KEEP_STATUS:
                stats['rows_dropped_status'] += 1
                continue

            # flags
            filial_missing = '0'
            cidade_missing = '0'
            data_nascimento_missing = '0'
            ean_missing = '0'
            quantidade_imputada = '0'
            valor_imputado = '0'
            cliente_missing = '0'

            # filial / cidade
            if is_null(rec['filial']):
                rec['filial'] = 'UNKNOWN'
                filial_missing = '1'
                stats['filial_missing'] += 1
            if is_null(rec['cidade']):
                rec['cidade'] = 'UNKNOWN'
                cidade_missing = '1'
                stats['cidade_missing'] += 1

            # produto / categoria
            if is_null(rec['produto_descricao']):
                rec['produto_descricao'] = 'UNKNOWN_PRODUCT'
            if is_null(rec['categoria_produto']):
                rec['categoria_produto'] = 'SEM_CATEGORIA'
            if is_null(rec['tipo_controle']):
                rec['tipo_controle'] = 'SEM_CONTROLE'

            # normalizacao textual
            for c in TEXT_COLUMNS:
                original = rec[c]
                normalized = normalize_text(original)
                if normalized != original:
                    stats['text_normalized_changed'][c] += 1
                rec[c] = normalized
                unique_after[c].add(normalized)

            # nome_cliente -> cliente_id
            if is_null(rec['nome_cliente']):
                cliente_id = ''
                cliente_missing = '1'
                stats['cliente_missing'] += 1
            else:
                cliente_id = hash_cliente(rec['nome_cliente'])

            # data_nascimento_cliente
            if is_null(rec['data_nascimento_cliente']):
                data_nascimento_missing = '1'
                stats['data_nascimento_missing'] += 1

            # genero
            if is_null(rec['genero_cliente']):
                rec['genero_cliente'] = 'DESCONHECIDO'

            # ean
            if is_null(rec['ean_produto']):
                ean_missing = '1'
                stats['ean_missing'] += 1

            # quantidade
            if is_null(rec['quantidade']):
                rec['quantidade'] = '1.0000'
                quantidade_imputada = '1'
                stats['quantidade_imputada'] += 1
            try:
                rec['quantidade'] = parse_decimal(rec['quantidade'])
                stats['quantidade_converted'] += 1
            except ValueError:
                stats['rows_dropped_type_error'] += 1
                continue

            # valor
            if is_null(rec['valor']):
                rec['valor'] = '0.00'
                valor_imputado = '1'
                stats['valor_imputado'] += 1
            try:
                rec['valor'] = parse_decimal(rec['valor'])
                stats['valor_converted'] += 1
            except ValueError:
                stats['rows_dropped_type_error'] += 1
                continue

            out_row = [rec[c] if c != 'nome_cliente' else cliente_id for c in COLS]
            out_row += [filial_missing, cidade_missing, data_nascimento_missing,
                        ean_missing, quantidade_imputada, valor_imputado, cliente_missing]
            writer.writerow(out_row)
            stats['rows_out'] += 1

    unique_counts = {
        c: {'before': len(unique_before[c]), 'after': len(unique_after[c])}
        for c in TEXT_COLUMNS
    }
    return stats, unique_counts


def csv_to_parquet(csv_path: str, parquet_path: str):
    import pyarrow as pa
    import pyarrow.csv as pacsv
    import pyarrow.parquet as pq

    read_opts = pacsv.ReadOptions(block_size=64 << 20)
    parse_opts = pacsv.ParseOptions(delimiter=';')
    convert_opts = pacsv.ConvertOptions(
        column_types={'quantidade': pa.float64(), 'valor': pa.float64()},
        strings_can_be_null=True,
    )
    with pacsv.open_csv(csv_path, read_options=read_opts,
                        parse_options=parse_opts, convert_options=convert_opts) as reader:
        writer = None
        try:
            for batch in reader:
                if writer is None:
                    writer = pq.ParquetWriter(parquet_path, batch.schema, compression='snappy')
                writer.write_batch(batch)
        finally:
            if writer is not None:
                writer.close()


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


def write_log(log_path: Path, payload: dict):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description='Pipeline de limpeza do dataset_vendas.csv')
    parser.add_argument('--input', default=os.environ.get('INPUT_CSV', 'dataset_vendas.csv'),
                        help='Caminho do CSV bruto de entrada (padrao: dataset_vendas.csv)')
    parser.add_argument('--output', default=os.environ.get('OUTPUT_CSV', 'dataset_vendas_clean.csv'),
                        help='Caminho do CSV limpo de saida (padrao: dataset_vendas_clean.csv)')
    parser.add_argument('--parquet', nargs='?', const='dataset_vendas_clean.parquet', default=None,
                        help='Tambem gera parquet. Caminho opcional (padrao: dataset_vendas_clean.parquet)')
    parser.add_argument('--log', default='clean_log.json',
                        help='Caminho do log JSON (padrao: clean_log.json)')
    parser.add_argument('--no-validate', action='store_true', help='Pular validacao final do CSV de saida')
    return parser.parse_args(argv)


def resolve(base: Path, value: str) -> Path:
    p = Path(value)
    return p if p.is_absolute() else (base / p).resolve()


def main(argv=None):
    args = parse_args(argv)
    base_dir = Path(__file__).resolve().parent
    in_path = resolve(base_dir, args.input)
    out_csv = resolve(base_dir, args.output)
    log_path = resolve(base_dir, args.log)
    parquet_path = resolve(base_dir, args.parquet) if args.parquet else None

    started = datetime.now(timezone.utc).isoformat()
    stats, unique_counts = clean_stream(str(in_path), str(out_csv))
    checked = None if args.no_validate else validate_output(str(out_csv))
    if parquet_path is not None:
        csv_to_parquet(str(out_csv), str(parquet_path))
    finished = datetime.now(timezone.utc).isoformat()

    payload = {
        'started_at': started,
        'finished_at': finished,
        'input': str(in_path),
        'output_csv': str(out_csv),
        'output_parquet': str(parquet_path) if parquet_path else None,
        'stats': stats,
        'unique_counts': unique_counts,
        'validated_rows': checked,
    }
    write_log(log_path, payload)

    print(
        f"rows_in={stats['rows_in']} rows_out={stats['rows_out']} "
        f"dropped_no_datetime={stats['rows_dropped_no_datetime']} "
        f"dropped_status={stats['rows_dropped_status']} "
        f"dropped_type_error={stats['rows_dropped_type_error']} "
        f"checked={checked} log={log_path}"
    )


if __name__ == '__main__':
    main()
