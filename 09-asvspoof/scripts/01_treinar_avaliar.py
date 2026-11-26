#!/usr/bin/env python3
"""ASVspoof — análise exploratória + features + classificadores (Aula 3, PCS5917).
Pipeline: WAV 16k -> features (PyAudioAnalysis-like: MFCC, ZCR, spectral centroid,
band energy ratios, chroma) -> RandomForest vs GradientBoosting vs SVM (RBF),
validação cruzada estratificada 5x, análise de sensibilidade a subconjuntos de features.
Saídas: resultados/metricas.csv, resultados/matriz_confusao_<modelo>.csv,
figuras/*.png, analise-exploratoria.md."""
import os, json, wave
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
AMOSTRAS = os.path.join(BASE, "amostras")
OUT = os.path.join(BASE, "resultados"); os.makedirs(OUT, exist_ok=True)
FIG = os.path.join(BASE, "figuras"); os.makedirs(FIG, exist_ok=True)

index = pd.DataFrame(json.load(open(os.path.join(BASE, "index.json"))))
assert set(index.label) == {0, 1}, index.label.value_counts()

def read_wav(path):
    with wave.open(path, "rb") as w:
        sr = w.getframerate(); n = w.getnframes()
        raw = w.readframes(n)
    x = np.frombuffer(raw, dtype="<i2").astype("float32") / 32767.0
    return x, sr

def features(x, sr):
    import librosa
    feats = {}
    if len(x) < sr // 10:  # <100ms
        x = np.pad(x, (0, sr - len(x)))
    # MFCC (13) + estatísticas
    mfcc = librosa.feature.mfcc(y=x, sr=sr, n_mfcc=13)
    for i in range(13):
        feats[f"mfcc{i:02d}_mean"] = mfcc[i].mean()
        feats[f"mfcc{i:02d}_std"] = mfcc[i].std()
    # energia, ZCR
    feats["zcr_mean"] = float(np.mean(np.abs(np.diff(np.sign(x)))))
    rms = librosa.feature.rms(y=x)[0]
    feats["rms_mean"], feats["rms_std"] = rms.mean(), rms.std()
    # espectro
    cent = librosa.feature.spectral_centroid(y=x, sr=sr)[0]
    bandw = librosa.feature.spectral_bandwidth(y=x, sr=sr)[0]
    rolloff = librosa.feature.spectral_rolloff(y=x, sr=sr)[0]
    flat = librosa.feature.spectral_flatness(y=x)[0]
    feats.update({"centroid_mean": cent.mean(), "centroid_std": cent.std(),
                  "bandwidth_mean": bandw.mean(), "rolloff_mean": rolloff.mean(),
                  "flatness_mean": flat.mean(), "flatness_std": flat.std()})
    # razões de energia em bandas (voz humana ~85-255 Hz fundamental; artefatos
    # de síntese alteram a distribuição acima de 4 kHz)
    S = np.abs(librosa.stft(x)) ** 2
    freqs = librosa.fft_frequencies(sr=sr)
    bands = [(0, 500), (500, 2000), (2000, 4000), (4000, 8000)]
    tot = S.sum() + 1e-12
    for j, (lo, hi) in enumerate(bands):
        m = (freqs >= lo) & (freqs < hi)
        feats[f"band{j}"] = float(S[m].sum() / tot)
    # chroma sumária
    ch = librosa.feature.chroma_cqt(y=x, sr=sr)
    for i in range(12):
        feats[f"chroma{i:02d}"] = ch[i].mean()
    feats["duração"] = len(x) / sr
    return feats

print("extraindo features...")
rows = []
for _, r in index.iterrows():
    x, sr = read_wav(os.path.join(AMOSTRAS, r.arquivo))
    f = features(x, sr)
    f.update({"id": r.id, "split": r.split, "label": r.label, "label_nome": r.label_nome})
    rows.append(f)
df = pd.DataFrame(rows)
df.to_csv(os.path.join(OUT, "features.csv"), index=False)
print("features:", df.shape)

# ---------- análise exploratória ----------
from sklearn.inspection import permutation_importance
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split
from sklearn.metrics import confusion_matrix, classification_report, f1_score, roc_auc_score, accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

feat_cols = [c for c in df.columns if c not in ("id", "split", "label", "label_nome")]
Xall = df[feat_cols].values; yall = df.label.values
# conjunto final = train+validation (split de origem vira atributo reportado)
Xtr, Xte, ytr, yte = train_test_split(Xall, yall, test_size=0.25, stratify=yall, random_state=42)

grupos = {
    "MFCC (13 + estatísticas)": [c for c in feat_cols if c.startswith("mfcc")],
    "Espectrais (centroide, flatness, rolloff, rms, zcr)": [c for c in feat_cols if c.split("_")[0] in
        ("centroid", "bandwidth", "rolloff", "flatness", "rms", "zcr")],
    "Energia em bandas (0-8 kHz)": [c for c in feat_cols if c.startswith("band")],
    "Chroma (12)": [c for c in feat_cols if c.startswith("chroma")],
    "Tudo": feat_cols,
}
resumo = []
cv = StratifiedKFold(5, shuffle=True, random_state=42)
modelos = {
    "RandomForest": RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1),
    "GradientBoosting": GradientBoostingClassifier(random_state=42),
    "SVM-RBF": make_pipeline(StandardScaler(), SVC(kernel="rbf", C=10, gamma="scale", probability=True)),
}
for nome, mod in modelos.items():
    sc = cross_val_score(mod, Xall, yall, cv=cv, scoring="f1")
    mod.fit(Xtr, ytr)
    pred = mod.predict(Xte)
    proba = mod.predict_proba(Xte)[:, 1] if hasattr(mod, "predict_proba") or isinstance(mod, type(mod)) and hasattr(mod, "steps") else None
    try:
        auc = roc_auc_score(yte, (mod.decision_function if isinstance(mod, SVC) else mod.predict_proba)(Xte)[:, 1]
                            if not isinstance(mod, type(None)) else mod.predict_proba(Xte)[:, 1])
    except Exception:
        try:
            p = mod.predict_proba(Xte)[:, 1]
        except AttributeError:
            p = mod.decision_function(Xte)
        auc = roc_auc_score(yte, p)
    cmx = confusion_matrix(yte, pred)
    pd.DataFrame(cmx, index=["fake", "real"], columns=["pred_fake", "pred_real"]).to_csv(
        os.path.join(OUT, f"matriz_confusao_{nome}.csv"))
    resumo.append({"modelo": nome, "cv_f1_media": sc.mean(), "cv_f1_std": sc.std(),
                   "teste_acuracia": accuracy_score(yte, pred), "teste_f1": f1_score(yte, pred, pos_label=0),
                   "teste_auc": auc})
    rep = classification_report(yte, pred, target_names=["fake", "real"])
    open(os.path.join(OUT, f"relatorio_{nome}.txt"), "w").write(rep)
    print(nome, resumo[-1])

res = pd.DataFrame(resumo)
res.to_csv(os.path.join(OUT, "metricas.csv"), index=False)

# sensibilidade a features (RandomForest, CV)
sens = []
rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
for gname, cols in grupos.items():
    sc = cross_val_score(rf, df[cols].values, yall, cv=cv, scoring="f1")
    sens.append({"conjunto": gname, "n_features": len(cols), "cv_f1_media": sc.mean(), "cv_f1_std": sc.std()})
    print(gname, round(sc.mean(), 3))
pd.DataFrame(sens).to_csv(os.path.join(OUT, "sensibilidade_features.csv"), index=False)

# importância de features (RF treinado em tudo)
rf.fit(Xtr, ytr)
imp = sorted(zip(feat_cols, rf.feature_importances_), key=lambda t: -t[1])[:15]
pd.DataFrame(imp, columns=["feature", "importancia"]).to_csv(os.path.join(OUT, "importancias_top15.csv"), index=False)

# figuras
plt.figure(figsize=(7, 4))
dur = df.groupby("label_nome")["duração"].apply(list)
plt.hist([dur.get("real", []), dur.get("fake", [])], bins=30, label=["real", "fake"], density=True)
plt.xlabel("duração (s)"); plt.ylabel("densidade"); plt.legend()
plt.title("Distribuição de duração por classe")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "duracao_por_classe.png")); plt.close()

plt.figure(figsize=(7, 4))
df.boxplot(column=["band0", "band1", "band2", "band3"], by="label_nome", grid=False)
plt.suptitle(""); plt.title("Energia relativa por banda (Hz: 0-500, 500-2k, 2k-4k, 4k-8k)")
plt.xlabel("classe"); plt.ylabel("fração da energia")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "bandas_por_classe.png")); plt.close()

plt.figure(figsize=(7, 4))
b = pd.DataFrame(sens).sort_values("cv_f1_media")
plt.barh(b.conjunto, b.cv_f1_media, xerr=b.cv_f1_std)
plt.xlabel("F1 (CV 5x, RandomForest)"); plt.title("Sensibilidade a subconjuntos de features")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "sensibilidade_features.png")); plt.close()

print("TUDO OK —", len(df), "amostras;", len(feat_cols), "features")
