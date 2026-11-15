#!/usr/bin/env python3
"""Retoca amostras com veredito PARSE_FALHOU no deteccao_cega_v3.csv:
re-roda com max_tokens maior, parser de resgate (regex do campo verdict no
texto cru, ultima ocorrencia) e salva trecho cru no CSV. Depois recalcula o
score v3 completo."""
import csv, json, os, re, time, urllib.request

BASE = '/opt/data/projetos/ia-adversarial/trojans'
URL = 'http://192.168.15.66:8099/v1/chat/completions'
MODEL = 'qwen3.8-flash-next-iq3_s'
OUT = os.path.join(BASE, 'resultados', 'deteccao_cega_v3.csv')
exec(open(os.path.join(BASE, 'scripts', 'detect_v3_devils_advocate.py')).read().split('def ask(')[0].split('\nrows =')[0].replace('OUT = os.path.join(BASE, \'resultados\', \'deteccao_cega_v3.csv\')', ''))

def ask2(code, maxtok):
    body = {"model": MODEL, "temperature": 0.0, "max_tokens": maxtok,
            "messages": [{"role": "system", "content": SYSTEM_V3},
                         {"role": "user", "content": "Amostra a auditar:\n\n" + code}]}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                msg = json.loads(r.read())["choices"][0]["message"]
            txt = (msg.get("content") or "") or (msg.get("reasoning_content") or "")
            if txt.strip():
                return txt
            raise ValueError("content vazio")
        except Exception as e:
            print(f"  retry {attempt+1}: {e}", flush=True)
            time.sleep(10 * (attempt + 1))
    return ""

def rescue(txt):
    # 1) JSON integro
    m = re.search(r"\{.*\}", txt or "", re.S)
    if m:
        try:
            p = json.loads(m.group(0))
            if p.get('verdict') in ('legitimo', 'trojan'):
                return p.get('verdict'), p.get('confidence'), json.dumps(p.get('findings', []), ensure_ascii=False), p.get('trigger') or '', p.get('effect') or ''
        except Exception:
            pass
    # 2) resgate: ultima ocorrencia do campo verdict no texto
    vs = re.findall(r'"verdict"\s*:\s*"(legitimo|trojan)"', txt or "")
    if vs:
        conf = re.findall(r'"confidence"\s*:\s*(\d+)', txt or "")
        trg = re.search(r'"trigger"\s*:\s*"([^"]{0,300})', txt or "")
        return vs[-1], (conf[-1] if conf else ''), '[]', (trg.group(1) if trg else ''), 'resgate-regex'
    return None, None, '[]', '', ''

rows = {r['amostra_id']: r for r in csv.DictReader(open(os.path.join(BASE, 'resultados', 'planilha_anonima.csv')))}
data = list(csv.DictReader(open(OUT)))
fieldnames = list(data[0].keys())
bad = [r for r in data if r['veredito'] not in ('legitimo', 'trojan')]
print('re-rodam:', [r['amostra_id'] for r in bad])
for r in bad:
    aid = r['amostra_id']
    print(f"{aid}...", flush=True)
    txt = ask2(rows[aid]['codigo_hdl'], 7000)
    v, c, fnd, trg, eff = rescue(txt)
    if v is None:  # segunda tentativa ainda maior
        txt = ask2(rows[aid]['codigo_hdl'], 12000)
        v, c, fnd, trg, eff = rescue(txt)
    r['veredito'] = v or 'PARSE_FALHOU'
    r['confianca'] = c or ''
    r['findings'] = fnd
    r['trigger'] = trg
    r['effect'] = eff
    print(f"  -> {r['veredito']} (conf {r['confianca']})", flush=True)

with open(OUT, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader(); w.writerows(data)

det = {r['amostra_id']: r for r in csv.DictReader(open(OUT))}
gab = {r['amostra_id']: r for r in csv.DictReader(open(os.path.join(BASE, 'resultados', 'gabarito.csv')))}
tp = tn = fp = fn = 0
lines = []
for aid in [f"A{i:02d}" for i in range(1, 21)]:
    truth, pred = gab[aid]['label_tipo'], det[aid]['veredito']
    if truth == 'trojan' and pred == 'trojan': tp += 1; tag = 'TP'
    elif truth == 'legitimo' and pred == 'legitimo': tn += 1; tag = 'TN'
    elif truth == 'legitimo' and pred == 'trojan': fp += 1; tag = 'FP'
    else: fn += 1; tag = 'FN'
    lines.append(f"{aid} {gab[aid]['id']:7} {truth:9} -> {pred:9} {tag}")
print('\n'.join(lines))
print(f"V3: Acuracia {(tp+tn)/20:.0%} | Recall {tp/(tp+fn):.0%} | Prec {tp/(tp+fp) if tp+fp else 0:.0%} | FP {fp} | FN {fn}")
