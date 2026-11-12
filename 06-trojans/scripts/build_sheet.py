import json, glob, os, random, re
import pandas as pd
BASE="/opt/data/projetos/ia-adversarial/trojans"
os.makedirs(f"{BASE}/resultados", exist_ok=True)
rows_lab, rows_anon = [], []
for kind in ["legitimate","trojans"]:
    for d in sorted(glob.glob(f"{BASE}/{kind}/*/")):
        meta=json.load(open(f"{d}/meta.json"))
        files=sorted(glob.glob(d+"*.v"))
        code="\n\n".join(f"// === {os.path.basename(f)} ===\n"+open(f).read() for f in files)
        rows_lab.append({"id":meta["id"],"label_tipo":meta["tipo"],"descricao":meta["descricao"],
                         "arquivo_alvo":meta["arquivo_alvo"],"categoria_ou_gatilho":meta.get("gatilho",meta.get("categoria","—")),
                         "dimensao_bytes":len(code),"n_arquivos":len(files)})
        # anonimizar: remove referencias a IDs LEG-/TRJ- do codigo
        code_anon=re.sub(r"\b(LEG|TRJ)-\d+\b","VARIANTE",code)
        rows_anon.append({"codigo_hdl":code_anon})
lab=pd.DataFrame(rows_lab); anon=pd.DataFrame(rows_anon)
rng=random.Random(42); order=list(range(20)); rng.shuffle(order)  # posicao p <- amostra original order[p]
anon2=anon.iloc[order].reset_index(drop=True)
anon2.insert(0,"amostra_id",[f"A{i+1:02d}" for i in range(20)])
lab["posicao"]=[order.index(i)+1 for i in range(20)]
lab["amostra_id"]=[f"A{order.index(i)+1:02d}" for i in range(20)]
mapa=lab.sort_values("posicao")[["amostra_id","id","label_tipo","descricao"]]
anon2[["amostra_id","codigo_hdl"]].to_csv(f"{BASE}/resultados/planilha_anonima.csv",index=False)
mapa.to_csv(f"{BASE}/resultados/gabarito.csv",index=False)
# XLSX: celula tem limite 32767 -> splitar codigo em partes
import numpy as np
def split_col(code, size=30000):
    return [code[i:i+size] for i in range(0,len(code),size)]
parts=list(split_col(anon2.codigo_hdl.max()))
wide=pd.DataFrame({"amostra_id":anon2.amostra_id})
for j in range(len(parts)):
    wide[f"codigo_parte{j+1}"]=["".join(c[j] if False else (split_col(c,30000)[j] if len(split_col(c,30000))>j else "")) for c in anon2.codigo_hdl]
with pd.ExcelWriter(f"{BASE}/resultados/planilha_trojans.xlsx",engine="openpyxl") as w:
    wide.to_excel(w,sheet_name="ANONIMA (trocar)",index=False)
    # F1 (revisao 2026-11-10): GABARITO NAO vai no xlsx publico — fica so no
    # gabarito.csv, que e o artefato rotulado nunca-enviavel (AVISO-GABARITO.txt).
print("planilhas ok; leak check:", any(re.search(r"(LEG|TRJ)-\d",c) for c in anon2.codigo_hdl))
print(mapa[["amostra_id","id","label_tipo"]].to_string(index=False))
