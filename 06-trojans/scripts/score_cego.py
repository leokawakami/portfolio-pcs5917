#!/usr/bin/env python3
"""Score da detecção cega: junta deteccao_cega_v1.csv + gabarito.csv e
calcula acurácia, recall, precisão, FP, FN. Só rodar DEPOIS de as 20
sentenças estarem fechadas."""
import csv, os

BASE = '/opt/data/projetos/ia-adversarial/trojans/resultados'
det = {r['amostra_id']: r for r in csv.DictReader(open(f'{BASE}/deteccao_cega_v1.csv'))}
gab = {r['amostra_id']: r for r in csv.DictReader(open(f'{BASE}/gabarito.csv'))}

assert len(det) == 20 and all(d['verdict'] in ('legitimo', 'trojan') for d in det.values()), \
    f"detecção incompleta/inválida: {len(det)} linhas, verdicts ruins: {[a for a,d in det.items() if d['verdict'] not in ('legitimo','trojan')]}"

tp = tn = fp = fn = 0
rows = []
for aid in sorted(gab):
    truth = gab[aid]['label_tipo']          # legitimo | trojan
    pred = det[aid]['verdict']
    if truth == 'trojan' and pred == 'trojan': tp += 1; tag = 'TP'
    elif truth == 'legitimo' and pred == 'legitimo': tn += 1; tag = 'TN'
    elif truth == 'legitimo' and pred == 'trojan': fp += 1; tag = 'FP'
    else: fn += 1; tag = 'FN'
    rows.append((aid, gab[aid]['id'], truth, pred, det[aid]['confidence'], tag, det[aid]['trigger'][:60]))

acc = (tp + tn) / 20
recall = tp / (tp + fn) if tp + fn else 0
prec = tp / (tp + fp) if tp + fp else 0
print(f"{'amostra':8} {'orig':8} {'real':10} {'veredito':10} {'conf':4} {'tag':3}  gatilho detectado")
for r in rows:
    print(f"{r[0]:8} {r[1]:8} {r[2]:10} {r[3]:10} {str(r[4]):4} {r[5]:3}  {r[6]}")
print(f"\nAcurácia {acc:.0%} | Recall {recall:.0%} | Precisão {prec:.0%} | FP {fp} | FN {fn}")
print(f"TP {tp} TN {tn} FP {fp} FN {fn}")

with open(f'{BASE}/score_deteccao_v1.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['amostra_id', 'id_original', 'real', 'veredito', 'confianca', 'tag', 'gatilho_detectado'])
    w.writerows(rows)
    w.writerow([])
    w.writerow(['acuracia', acc]); w.writerow(['recall', recall])
    w.writerow(['precisao', prec]); w.writerow(['falsos_positivos', fp]); w.writerow(['falsos_negativos', fn])
print("gravado score_deteccao_v1.csv")
