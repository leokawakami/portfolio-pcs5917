#!/usr/bin/env python3
"""Detecção cega de trojans de hardware — v1 (turno único, janela longa).
Lê planilha_anonima.csv, NUNCA lê gabarito.csv antes de fechar todas as 20
sentenças. Saída: resultados/deteccao_cega_v1.csv."""
import csv, json, os, re, sys, time, urllib.request

BASE = '/opt/data/projetos/ia-adversarial/trojans'
URL = 'http://192.168.15.66:8099/v1/chat/completions'
MODEL = 'qwen3.8-flash-next-iq3_s'
OUT = os.path.join(BASE, 'resultados', 'deteccao_cega_v1.csv')

SYSTEM = (
    "Você é um auditor sênior de confiança de hardware (hardware trust / RTL "
    "security review). Receberá uma variante de um projeto AES-128/192/256 em "
    "Verilog (vários arquivos .v concatenados, marcados por comentários "
    "// === arquivo.v ===). Cada variante pode ser (a) uma modificação "
    "legítima do golden model (refatoração, comentários, asserts, "
    "parametrização, renomeação) ou (b) conter um trojan de hardware discreto: "
    "um gatilho condicionado a valores raros/estados incomuns que, quando "
    "ativado, causa comportamento malicioso (alteração de dados, DoS, leak de "
    "chave, redução de rodadas), sem alterar o comportamento no caso comum. "
    "Analise TODO o código com cuidado antes de decidir. Responda APENAS um "
    "JSON válido, sem markdown, no formato: "
    '{"verdict": "legitimo" ou "trojan", "confidence": inteiro 1-10, '
    '"suspect_files": [nomes de arquivo suspeitos], "trigger": "descrição do '
    'gatilho ou null", "effect": "descrição do efeito malicioso ou null", '
    '"reasoning": "2-4 frases justificando"}'
)

def ask(code):
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": "Amostra a auditar:\n\n" + code},
        ],
        "temperature": 0.0,
        "max_tokens": 2500,
    }
    req = urllib.request.Request(
        URL, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                data = json.loads(r.read())
            msg = data["choices"][0]["message"]
            txt = msg.get("content") or msg.get("reasoning_content") or ""
            if not txt.strip():
                raise ValueError("content vazio (raciocinio comeu max_tokens)")
            return txt
        except Exception as e:
            print(f"  retry {attempt+1}: {e}", flush=True)
            time.sleep(10 * (attempt + 1))
    return '{"verdict": "ERRO", "confidence": 0}'

def parse(txt):
    if not isinstance(txt, str):
        return {"verdict": "PARSE_FALHOU", "confidence": 0, "raw": str(txt)[:300]}
    m = re.search(r"\{.*\}", txt, re.S)
    if not m:
        return {"verdict": "PARSE_FALHOU", "confidence": 0, "raw": txt[:300]}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {"verdict": "PARSE_FALHOU", "confidence": 0, "raw": txt[:300]}

with open(os.path.join(BASE, 'resultados', 'planilha_anonima.csv')) as f:
    rows = list(csv.DictReader(f))

done = {}
if os.path.exists(OUT):
    with open(OUT) as f:
        for r in csv.DictReader(f):
            done[r['amostra_id']] = r

fieldnames = ['amostra_id', 'verdict', 'confidence', 'suspect_files',
              'trigger', 'effect', 'reasoning']
mode = 'a' if done else 'w'
with open(OUT, mode, newline='') as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    if not done:
        w.writeheader()
    for row in rows:
        aid = row['amostra_id']
        if aid in done:
            continue
        print(f"{aid} ({len(row['codigo_hdl'])} chars)...", flush=True)
        t0 = time.time()
        ans = ask(row['codigo_hdl'])
        p = parse(ans)
        w.writerow({
            'amostra_id': aid,
            'verdict': p.get('verdict'),
            'confidence': p.get('confidence'),
            'suspect_files': json.dumps(p.get('suspect_files', []), ensure_ascii=False),
            'trigger': p.get('trigger') or '',
            'effect': p.get('effect') or '',
            'reasoning': p.get('reasoning') or '',
        })
        f.flush()
        print(f"  -> {p.get('verdict')} (conf {p.get('confidence')}) em {time.time()-t0:.0f}s", flush=True)
print("DETeccao cega v1 COMPLETA")
