#!/usr/bin/env python3
"""ASVspoof (atividade Aula 3 — PCS5917).
Dataset: MoaazTalab/ASVspoof_2021_LA_Balanced_Normalized (HF, publico, sem login;
equivalente ao ASVspoof 2021 LA que o Kaggle exige conta — substituicao registrada).
Baixa shards train+validation, monta amostra balanceada (cap+sub) em WAV 16k mono."""
import os, json, wave, urllib.request, random
import numpy as np
import pyarrow.parquet as pq

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "raw"); os.makedirs(RAW, exist_ok=True)
DS = "MoaazTalab/ASVspoof_2021_LA_Balanced_Normalized"

def api(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Chrome/120"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

info = api(f"https://huggingface.co/api/datasets/{DS}")
shards = {}
for s in info["siblings"]:
    fn = s["rfilename"]
    if fn.endswith(".parquet"):
        split = fn.split("/")[-1].split("-")[0]
        shards.setdefault(split, []).append(fn)
print({k: len(v) for k, v in shards.items()})

def dl(fn):
    dest = os.path.join(RAW, os.path.basename(fn))
    if os.path.exists(dest) and os.path.getsize(dest) > 10000:
        print("cache", os.path.basename(fn)); return dest
    url = f"https://huggingface.co/datasets/{DS}/resolve/main/{fn}"
    print("baixando", url, flush=True)
    with urllib.request.urlopen(url, timeout=600) as r, open(dest + ".part", "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk: break
            f.write(chunk)
    os.replace(dest + ".part", dest)
    print("  ok", os.path.getsize(dest) // (1024 * 1024), "MB")
    return dest

# baixar shards por split ate ter >=TARGET em CADA banda (shards vem ordenados por label)
TARGET = 300  # por banda por split
random.seed(42)
from collections import Counter

rows = []
for split in ("train", "validation"):
    buckets = {}
    for fn in sorted(shards[split]):
        t = pq.read_table(dl(fn), columns=["audio", "label"])
        auds = t.column("audio").to_pylist(); labs = t.column("label").to_pylist()
        for au, lab in zip(auds, labs):
            b = str(int(lab)) if not isinstance(lab, str) else lab
            buckets.setdefault(b, []).append(au)
        del auds, labs, t
        have = {k: len(v) for k, v in buckets.items()}
        print(split, have, flush=True)
        if len(buckets) >= 2 and all(len(v) >= TARGET for v in buckets.values()):
            break
    print(split, "final", {k: len(v) for k, v in buckets.items()})
    take = min(TARGET, min(len(v) for v in buckets.values()))
    for band, items in sorted(buckets.items()):
        random.shuffle(items)
        for au in items[:take]:
            rows.append({"split": split, "band": band, "audio": au})
    del buckets

outdir = os.path.join(BASE, "amostras"); os.makedirs(outdir, exist_ok=True)
index, per = [], Counter()
for row in rows:
    key = f"{row['split']}_{row['band']}_{per[(row['split'],row['band'])]:03d}"
    per[(row['split'], row['band'])] += 1
    au = row["audio"]; sr = 16000
    try:
        if "array" in au and au["array"] is not None:
            x = np.asarray(au["array"], dtype="float32")
            sr = au.get("sampling_rate", 16000)
        else:
            import io, soundfile as sf
            data = au.get("bytes")
            try:
                x, sr = sf.read(io.BytesIO(data), dtype="float32")
            except Exception:
                import subprocess as sp
                p = sp.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", "pipe:0",
                            "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                           input=data, capture_output=True)
                if p.returncode != 0:
                    raise RuntimeError(p.stderr[:120].decode(errors="replace"))
                x = np.frombuffer(p.stdout, dtype="<f4"); sr = 16000
        if np.ndim(x) > 1: x = np.asarray(x).mean(axis=1)
    except Exception as e:
        print("pula amostra ilegivel", row["band"], str(e)[:80]); continue
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(os.path.join(outdir, key + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(pcm.tobytes())
    index.append({"id": key, "split": row["split"], "label": int(row["band"]),
                  "label_nome": "fake" if int(row["band"]) == 0 else "real",
                  "sr": sr, "arquivo": key + ".wav"})
json.dump(index, open(os.path.join(BASE, "index.json"), "w"), indent=1)
print("gravados:", len(index), dict(Counter((r['split'], r['label_nome']) for r in index)))
