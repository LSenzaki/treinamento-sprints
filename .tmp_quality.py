import csv
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation

path = 'dataset_vendas.csv'
cols = 13
missing = [0] * cols
invalid_dates = 0
negative_qty = 0
negative_val = 0
rows = 0
status = Counter()
card = [Counter() for _ in range(cols)]
qty_min = None
qty_max = None
val_min = None
val_max = None

with open(path, 'r', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        if not row:
            continue
        rows += 1
        if len(row) < cols:
            row = row + [''] * (cols - len(row))
        for i in range(cols):
            v = row[i].strip() if i < len(row) else ''
            if v == '':
                missing[i] += 1
            else:
                card[i][v] += 1
        status[row[2].strip()] += 1
        try:
            datetime.strptime(row[3].strip(), '%Y-%m-%d %H:%M:%S.%f')
        except Exception:
            try:
                datetime.strptime(row[3].strip(), '%Y-%m-%d %H:%M:%S')
            except Exception:
                invalid_dates += 1
        try:
            q = Decimal(row[9].replace(',', '.'))
            v = Decimal(row[10].replace(',', '.'))
            if q < 0:
                negative_qty += 1
            if v < 0:
                negative_val += 1
            qty_min = q if qty_min is None or q < qty_min else qty_min
            qty_max = q if qty_max is None or q > qty_max else qty_max
            val_min = v if val_min is None or v < val_min else val_min
            val_max = v if val_max is None or v > val_max else val_max
        except (InvalidOperation, IndexError):
            pass

print(f'ROWS\t{rows}')
for i, n in enumerate(missing, 1):
    print(f'MISSING\t{i}\t{n}\t{(n / rows * 100):.6f}')
print(f'INVALID_DATES\t{invalid_dates}')
print(f'NEG_QTY\t{negative_qty}')
print(f'NEG_VAL\t{negative_val}')
for k, v in status.most_common():
    print(f'STATUS\t{repr(k)}\t{v}\t{(v / rows * 100):.6f}')
for i, c in enumerate(card, 1):
    print(f'CARD\t{i}\t{len(c)}')
print(f'NUM_MINMAX\t{qty_min}\t{qty_max}\t{val_min}\t{val_max}')
