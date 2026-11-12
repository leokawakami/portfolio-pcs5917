#!/usr/bin/env python3
"""v2 full: reusa resultados/deteccao_cega_v2.csv (6 amostras) e roda o
restante das 20 com o mesmo SYSTEM_V2. Depois calcula score v2 completo."""
import csv, json, os, re, time, urllib.request
exec(open('/opt/data/projetos/ia-adversarial/trojans/scripts/detect_v2_checklist.py').read().split("rows = {")[0])  # SYSTEM_V2, ask, parse, BASE, OUT

rows = {r['amostra_id']: r for r in csv.DictReader(open(os.path.join(BASE, 'resultados', 'planilha_anonima.csv')))}
done = {r['amostra_id'] for r in csv.DictReader(open(OUT))}
allids = [f"A{i:02d}" for i in range(1, 21)]
with open(OUT, 'a', newline='') as f:
    w = csv.writer(f)
    for aid in allids:
        if aid in done:
            continue
        print(f"{aid}...", flush=True)
        p = parse(ask(rows[aid]['codigo_hdl']))
        w.writerow([aid, 'full-v2', p.get('verdict'), p.get('confidence'),
                    json.dumps(p.get('invariants_checked', {}), ensure_ascii=False),
                    p.get('trigger') or '', p.get('effect') or ''])
        f.flush()
        print(f"  -> {p.get('verdict')} (conf {p.get('confidence')})", flush=True)

# score v2
det = {r['amostra_id']: r for r in csv.DictReader(open(OUT))}
gab = {r['amostra_id']: r for r in csv.DictReader(open(os.path.join(BASE, 'resultados', 'gabarito.csv')))}
tp = tn = fp = fn = 0
lines = []
for aid in allids:
    truth, pred = gab[aid]['label_tipo'], det[aid]['verdict']
    if truth == 'trojan' and pred == 'trojan': tp += 1; tag = 'TP'
    elif truth == 'legitimo' and pred == 'legitimo': tn += 1; tag = 'TN'
    elif truth == 'legitimo' and pred == 'trojan': fp += 1; tag = 'FP'
    else: fn += 1; tag = 'FN'
    lines.append(f"{aid} {gab[aid]['id']:7} {truth:9} -> {pred:9} {tag}")
print('\n'.join(lines))
print(f"V2: Acuracia {(tp+tn)/20:.0%} | Recall {tp/(tp+fn):.0%} | Prec {tp/(tp+fp) if tp+fp else 0:.0%} | FP {fp} | FN {fn}")
