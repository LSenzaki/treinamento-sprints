"""Smoke test do clean.py: gera CSV sintetico com duplicidades textuais conhecidas e roda o pipeline.

Confirma que apos a normalizacao o numero de valores unicos cai como esperado.
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SYNTH = ROOT / 'tmp_synth.csv'
OUT_CSV = ROOT / 'tmp_synth_clean.csv'
OUT_PARQUET = ROOT / 'tmp_synth_clean.parquet'
OUT_LOG = ROOT / 'tmp_synth_log.json'

# variacoes textuais propositais
PRODUTOS = [
    ('  Dipirona  500MG ', 'Diuretico'),
    ('DIPIRONA 500MG', 'DIURETICO'),
    ('Dipirona 500mg', 'diuretico'),
    ('PARACETAMOL 750mg', 'ANALGESICO'),
    ('Paracetamol  750MG', 'analgésico'),
]
FILIAIS = ['FCIA LIDER FILIAL 1', 'Fcia Lider Filial 1', 'FCIA  LIDER FILIAL 1']
CIDADES = ['Palotina', 'PALOTINA', 'palotina', 'São Paulo', 'SAO PAULO', 'SAO  PAULO']

rows = []
i = 0
for filial in FILIAIS:
    for cidade in CIDADES:
        for produto, categoria in PRODUTOS:
            i += 1
            rows.append([
                filial, cidade, 'FECHADO',
                f'2025-01-{(i%28)+1:02d} 10:00:00.000000',
                f'Cliente {i}', '1990-01-01', 'M',
                produto, '7891234567890', '1,000', '10,50', categoria, 'SEM CONTROLE',
            ])

# uma linha sem datetime (deve ser descartada)
rows.append(['F1', 'C1', 'FECHADO', '', 'X', '', 'M', 'P', '', '1', '1', 'C', 'SEM CONTROLE'])
# uma linha com status diferente (deve ser descartada)
rows.append(['F1', 'C1', 'CANCELADO', '2025-01-01 10:00:00.000000', 'X', '', 'M', 'P', '', '1', '1', 'C', 'SEM CONTROLE'])

with open(SYNTH, 'w', encoding='utf-8', newline='') as fh:
    w = csv.writer(fh, delimiter=';')
    for r in rows:
        w.writerow(r)

cmd = [sys.executable, str(ROOT / 'clean.py'),
       '--input', str(SYNTH), '--output', str(OUT_CSV),
       '--parquet', str(OUT_PARQUET), '--log', str(OUT_LOG)]
res = subprocess.run(cmd, capture_output=True, text=True)
print('STDOUT:', res.stdout)
print('STDERR:', res.stderr)
assert res.returncode == 0, f'clean.py falhou: rc={res.returncode}'

log = json.loads(OUT_LOG.read_text(encoding='utf-8'))
print('=== unique_counts ===')
print(json.dumps(log['unique_counts'], indent=2, ensure_ascii=False))
print('=== stats (resumo) ===')
print(json.dumps({k: v for k, v in log['stats'].items() if k != 'text_normalized_changed'}, indent=2))
print('text_normalized_changed:', json.dumps(log['stats']['text_normalized_changed']))

uc = log['unique_counts']
assert uc['produto_descricao']['after'] < uc['produto_descricao']['before'], 'produto: normalizacao nao colapsou duplicidades'
assert uc['cidade']['after'] < uc['cidade']['before'], 'cidade: normalizacao nao colapsou duplicidades'
assert uc['filial']['after'] < uc['filial']['before'], 'filial: normalizacao nao colapsou duplicidades'
assert uc['categoria_produto']['after'] < uc['categoria_produto']['before'], 'categoria: normalizacao nao colapsou duplicidades'
assert log['stats']['rows_dropped_no_datetime'] >= 1
assert log['stats']['rows_dropped_status'] >= 1
assert OUT_PARQUET.exists()
print('OK')

# cleanup
for p in (SYNTH, OUT_CSV, OUT_PARQUET, OUT_LOG):
    p.unlink(missing_ok=True)
