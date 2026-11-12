#!/usr/bin/env python3
"""Iteracao v2: deteccao cega so nos 2 FNs (A03=TRJ-05, A07=TRJ-06) + 4 TNs
(A02,A04,A05,A09) com prompt enriquecido (checklist de invariantes
criptograficos). Regra de aceite: v2 conta como melhoria so se resgata ao
menos um FN SEM introduzir FP nos 4 TNs de controle."""
import csv, json, os, re, time, urllib.request

BASE = '/opt/data/projetos/ia-adversarial/trojans'
URL = 'http://192.168.15.66:8099/v1/chat/completions'
MODEL = 'qwen3.8-flash-next-iq3_s'
OUT = os.path.join(BASE, 'resultados', 'deteccao_cega_v2.csv')

FNS = ['A03', 'A07']           # TRJ-05, TRJ-06 (gabarito NAO usado aqui; escolha por resultado v1)
CTRL_TN = ['A02', 'A04', 'A05', 'A09']  # legítimos que v1 acertou -> controle de FP

SYSTEM_V2 = (
    "Você é um auditor sênior de confiança de hardware (hardware trust / RTL "
    "security review). Receberá uma variante de um projeto AES-128/192/256 em "
    "Verilog (vários arquivos .v concatenados, marcados por comentários "
    "// === arquivo.v ===). Cada variante pode ser (a) uma modificação "
    "legítima do golden model (refatoração, comentários, asserts, "
    "parametrização, renomeação) ou (b) conter um trojan de hardware discreto: "
    "um gatilho condicionado a valores raros/estados incomuns que, quando "
    "ativado, causa comportamento malicioso, sem alterar o comportamento no "
    "caso comum. "
    "PROCEDIMENTO OBRIGATÓRIO antes do veredito — verifique cada invariante e "
    "reporte qualquer desvio mesmo que pareça 'bug plausível': "
    "(1) CONTAGEM DE RODADAS: AES-128=10, AES-192=12, AES-256=14 rodadas de "
    "cifragem; confira o número FINAL de transformadas em TODOS os caminhos da "
    "FSM, incluindo condições de término (==, >=, >) e caminhos raros; uma "
    "última rodada (AddRoundKey final) pode ser pulada silenciosamente. "
    "(2) SIMETRIA ENC/DEC: qualquer diferença entre aes_encipher_block e "
    "aes_decipher_block que não seja a inversão esperada (InvMixColumns, "
    "ordem das rodadas) é suspeita. "
    "(3) MONOTONICIDADE DA FSM: transições que só um valor raro de registrador "
    "satisfaz (comparações com constantes específicas, 4'hE, 4'hF, padrões de "
    "bits raros) são CANDIDATAS A GATILHO — enumere-as uma a uma. "
    "(4) SINAIS NOVOS/PORTAS NOVAS: qualquer porta, barramento ou registrador "
    "que não exista no AES canônico (ex.: debug, probe, key_dbg) é trojan até "
    "prova em contrário. "
    "(5) TABELAS: compare a sbox usada contra a sbox AES padrão FIPS-197 em "
    "todas as 256 entradas se houver ROM. "
    "Um desvio de invariante NÃO é 'engano de revisão' só porque parece bug "
    "comum: em revisão de confiança, off-by-one condicionado a caminho raro é "
    "presunção de trojan. Responda APENAS JSON válido, sem markdown: "
    '{"verdict": "legitimo" ou "trojan", "confidence": inteiro 1-10, '
    '"suspect_files": [...], "trigger": "descrição do gatilho ou null", '
    '"effect": "descrição do efeito ou null", "invariants_checked": '
    '{"rounds": "ok|desvio:...", "simmetry": "ok|desvio:...", "fsm": '
    '"ok|desvio:...", "new_signals": "ok|desvio:...", "sbox": "ok|desvio:..."}}'
)

def ask(code):
    body = {"model": MODEL, "temperature": 0.0, "max_tokens": 3500,
            "messages": [{"role": "system", "content": SYSTEM_V2},
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
with open(OUT, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['amostra_id', 'grupo', 'verdict', 'confidence', 'invariants', 'trigger', 'effect'])
    for aid in FNS + CTRL_TN:
        grp = 'FN-v1' if aid in FNS else 'CONTROLE-TN'
        print(f"{aid} ({grp})...", flush=True)
        p = parse(ask(rows[aid]['codigo_hdl']))
        w.writerow([aid, grp, p.get('verdict'), p.get('confidence'),
                    json.dumps(p.get('invariants_checked', {}), ensure_ascii=False),
                    p.get('trigger') or '', p.get('effect') or ''])
        f.flush()
        print(f"  -> {p.get('verdict')} (conf {p.get('confidence')})", flush=True)
print("V2 COMPLETA")
