import csv
import json
from collections import Counter

NULL_TOKENS = {'', 'NULL', 'NaN', 'N/D', 'NA', 'None', '-'}

def is_null(val):
    if val is None:
        return True
    v = val.strip()
    return v in NULL_TOKENS

def main():
    path = 'dataset_vendas.csv'
    with open(path, 'r', encoding='utf-8', errors='replace', newline='') as fh:
        reader = csv.reader(fh, delimiter=';')
        header = next(reader)
        ncols = len(header)
        null_counts = [0] * ncols
        total = 0
        for row in reader:
            total += 1
            # pad short rows
            if len(row) < ncols:
                row += [''] * (ncols - len(row))
            for i in range(ncols):
                if is_null(row[i]):
                    null_counts[i] += 1

    out = {'total_rows': total, 'header': header, 'null_counts': null_counts}
    print(json.dumps(out, ensure_ascii=False))

if __name__ == '__main__':
    main()
