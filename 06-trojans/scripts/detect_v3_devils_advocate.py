#!/usr/bin/env python3
"""Iteracao v3: deteccao cega nas 20 amostras com prompt de contra-argumento
forcado (devil's advocate): antes do veredito o auditor DEVE escrever a
melhor hipotese de legitimidade para cada achado suspeito e a melhor hipotese
de trojan para cada amostra 'limpa', so decidindo depois. Hipotese: recupera
os 2 FNs da v1 sem os 3 FPs da v2 (calibragem do custo de erro).
Retomavel: pula amostras ja presentes no CSV de saida."""
import csv, json, os, re, time, urllib.request

BASE = '/opt/data/projetos/ia-adversarial/trojans'
URL = 'http://192.168.15.66:8099/v1/chat/completions'
MODEL = 'qwen3.8-flash-next-iq3_s'
OUT = os.path.join(BASE, 'resultados', 'deteccao_cega_v3.csv')

SYSTEM_V3 = (
    "Você é um auditor sênior de confiança de hardware (hardware trust / RTL "
    "security review). Receberá uma variante de um projeto AES-128/192/256 em "
    "Verilog (vários arquivos .v concatenados, marcados por comentários "
    "// === arquivo.v ===). Cada variante pode ser (a) uma modificação "
    "legítima do golden model (refatoração, comentários, asserts, "
    "parametrização, renomeação) ou (b) conter um trojan de hardware discreto: "
    "um gatilho condicionado a valores raros/estados incomuns que, quando "
    "ativado, causa comportamento malicioso, sem alterar o comportamento no "
    "caso comum. "
    "PROCEDIMENTO OBRIGATÓRIO (debate interno antes do veredito): "
    "PASSO 1 — liste até 3 ACHADOS suspeitos (diferenças vs. AES canônico: "
    "contagem de rodadas por tamanho de chave 128=10/192=12/256=14 em TODOS "
    "os caminhos da FSM incluindo condições == vs >=, assimetrias ENC/DEC "
    "inesperadas, comparações com constantes raras, portas/sinais novos, "
    "sbox fora do padrão FIPS-197). "
    "PASSO 2 — para CADA achado, escreva o MELHOR argumento de que ele é "
    "LEGÍTIMO (refatoração, asserção, otimização, estilo de codificação, bug "
    "de revisão anterior) e o MELHOR argumento de que é um TROJAN deliberado "
    "(condicionado a caminho raro, efeito útil ao atacante, plausibilidade "
    "de bug comum fabricada). "
    "PASSO 3 — pondere: um achado só conta como evidência de trojan quando o "
    "argumento de legitimidade NÃO explica a condicionado a valor raro com "
    "efeito explorável; e um veredito 'trojan' só se sustenta quando o melhor "
    "contra-argumento legítimo foi refutado com base no código. "
    "Se a amostra parecer limpa, ainda assim escreva o melhor argumento "
    "adverso possível antes de confirmar 'legitimo'. "
    "Responda APENAS JSON válido, sem markdown: "
    '{"verdict": "legitimo" ou "trojan", "confidence": inteiro 1-10, '
    '"findings": [{"observation": "...", "legit_argument": "...", '
    '"trojan_argument": "...", "resolution": "legitimo|trojan|inconclusivo"}], '
    '"trigger": "descrição do gatilho ou null", "effect": "descrição do '
    'efeito ou null"}'
)

def ask(code):
    body = {"model": MODEL, "temperature": 0.0, "max_tokens": 3500,
            "messages": [{"role": "system", "content": SYSTEM_V3},
                         {"role": "user", "content": "Amostra a auditar:\n\n" + code}]}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                msg = json.loads(r.read())["choices"][0]["message"]
            txt = msg.get("content") or msg.get("reasoning_content") or ""
            if txt.strip():
                return txt
            raise ValueError("content vazio")
        except Exception as e:
            print(f"  retry {attempt+1}: {e}", flush=True)
            time.sleep(10 * (attempt + 1))
    return '{"verdict": "ERRO"}'

def parse(txt):
    m = re.search(r"\{.*\}", txt or "", re.S)
    if not m:
        return {"verdict": "PARSE_FALHOU"}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {"verdict": "PARSE_FALHOU", "raw": txt[:300]}

rows = {r['amostra_id']: r for r in csv.DictReader(open(os.path.join(BASE, 'resultados', 'planilha_anonima.csv')))}
done = set()
if os.path.exists(OUT):
    done = {r['amostra_id'] for r in csv.DictReader(open(OUT))}
allids = [f"A{i:02d}" for i in range(1, 21)]
new_file = not os.path.exists(OUT)
with open(OUT, 'a', newline='') as f:
    w = csv.writer(f)
    if new_file:
        w.writerow(['amostra_id', 'run', 'veredito', 'confianca', 'findings', 'trigger', 'effect'])
    for aid in allids:
        if aid in done:
            continue
        print(f"{aid}...", flush=True)
        p = parse(ask(rows[aid]['codigo_hdl']))
        w.writerow([aid, 'full-v3', p.get('verdict'), p.get('confidence'),
                    json.dumps(p.get('findings', []), ensure_ascii=False),
                    p.get('trigger') or '', p.get('effect') or ''])
        f.flush()
        print(f"  -> {p.get('verdict')} (conf {p.get('confidence')})", flush=True)

# score v3
det = {r['amostra_id']: r for r in csv.DictReader(open(OUT))}
gab = {r['amostra_id']: r for r in csv.DictReader(open(os.path.join(BASE, 'resultados', 'gabarito.csv')))}
tp = tn = fp = fn = 0
lines = []
for aid in allids:
    truth, pred = gab[aid]['label_tipo'], det[aid]['veredito']
    if truth == 'trojan' and pred == 'trojan': tp += 1; tag = 'TP'
    elif truth == 'legitimo' and pred == 'legitimo': tn += 1; tag = 'TN'
    elif truth == 'legitimo' and pred == 'trojan': fp += 1; tag = 'FP'
    else: fn += 1; tag = 'FN'
    lines.append(f"{aid} {gab[aid]['id']:7} {truth:9} -> {pred:9} {tag}")
print('\n'.join(lines))
print(f"V3: Acuracia {(tp+tn)/20:.0%} | Recall {tp/(tp+fn):.0%} | Prec {tp/(tp+fp) if tp+fp else 0:.0%} | FP {fp} | FN {fn}")
