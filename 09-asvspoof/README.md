# 09 — Detecção de Áudio Falso (ASVspoof) — Atividade prática da Aula 3

**Disciplina:** PCS5917 — IA Adversarial (Poli/USP) · **Aluno:** Leonardo Kawakami Hissanaga — NUSP 11374864
**Atividade:** treinar e avaliar classificador para detecção de áudio falso (identificação binária de ataque), com análise exploratória e validação cruzada (desafio: múltiplos classificadores + sensibilidade a features).

> **Nota de reprodutibilidade / substituição de fonte.** O enunciado pede o dataset do ASVspoof no Kaggle, que exige login. Usei o **ASVspoof 2021 LA** na república pública e sem-login `MoaazTalab/ASVspoof_2021_LA_Balanced_Normalized` no Hugging Face (mesmo corpus oficial, balanceado e normalizado). Decisão registrada aqui e no notebook.

## 1. Dados

- Conjunto total: 34.931 train / 18.057 validação / 200.831 teste (parquet, áudio FLAC embutido).
- Amostra efetiva deste trabalho: **1.200 áudios balanceados** (300 fake + 300 real em train; 300 + 300 em validação), seed 42, WAV 16 kHz mono.
- Rótulos: `fake` (ataque: síntese/conversão de voz) × `real` (bona fide). Os shards vêm ordenados por rótulo; o script baixa shards suficientes por split para preencher as duas bandas (limitação conhecida do dataset no HF).
- Códigos-fonte desta entrega: `scripts/00_baixar_amostra.py` (ingestão) e `scripts/01_treinar_avaliar.py` (features + classificadores). Notebook para Colab: `asvspoof-deteccao.ipynb`.

## 2. Análise exploratória

- 52 features por amostra (extração estilo PyAudioAnalysis via librosa): MFCC 1–13 (média+desvio), ZCR, RMS, centroide/bandwidth/rolloff de espectro, *spectral flatness*, razão de energia em 4 bandas (0–500 Hz, 0,5–2 kHz, 2–4 kHz, 4–8 kHz), chroma (12), duração.
- Hipótese testada: artefatos de síntese alteram a distribuição de energia acima de ~4 kHz e a *flatness* espectral: as bandas e a flatness separam mais que features de prosódia (duração), que quase não distingue as classes (figura `duracao_por_classe.png`).
- A razão de energia 4–8 kHz é consistentemente menor nas amostras falsas (figura `bandas_por_classe.png`), compatível com o efeito de vocoders/TTS sobre o teto espectral.

## 3. Classificadores e resultados (CV estratificada 5×, semente 42; teste 25% estratificado)

| Modelo | F1 (CV 5×) | Acurácia (teste) | F1 fake (teste) | AUC (teste) |
|---|---|---|---|---|
| **SVM-RBF** (C=10, escala) | **0,820 ± 0,015** | **81,3%** | 0,811 | 0,885 |
| GradientBoosting | 0,803 ± 0,020 | 78,0% | 0,787 | 0,892 |
| RandomForest (300 árvores) | 0,798 ± 0,019 | 79,0% | 0,804 | **0,901** |

Matrizes de confusão e relatórios por classe em `resultados/`. O SVM (com *scaling*) vence em F1/acurácia; a RandomForest tem a melhor AUC (ranking de probabilidade mais bem calibrado). Números compatíveis com a literatura para pipelines clássicos MFCC no LA (eavesdropping): EER da ordem de dezenas de % sem features profundas; o estado da arte (AASIST e afins) usa redes espectrais.

## 4. Sensibilidade a subconjuntos de features (RandomForest, mesma CV)

| Conjunto | n-features | F1 (CV) |
|---|---|---|
| MFCC (13 + estatísticas) | 26 | 0,750 |
| Espectrais (centroide, flatness, rolloff, RMS, ZCR) | 8 | 0,682 |
| Chroma (12) | 12 | 0,648 |
| Energia em bandas (0–8 kHz) | 4 | 0,585 |
| **Tudo** | 52 | **0,801** |

Leitura: MFCC carrega o grosso do sinal; flatness/centroide e bandas adicionam ganho incremental (~+0,05 F1 juntas com o resto); chroma sozinha é fraca mas complementa. Top-5 importâncias (RF): mfcc02_std, mfcc04_mean, mfcc03_std, flatness_std, mfcc02_mean: variância temporal de MFCC de ordem média é o preditor dominante.

## 5. Limitações

- Amostra de 1.200 (não usei os 200k de teste: custo de download sem ganho para o escopo da atividade; split teste original permanece intacto p/ comparação futura honesta).
- Condições LA apenas (ataque por ataque de voz); CTS/SAS e condições de canal não cobertas.
- Áudio re-amostrado/normalizado por terceiros no HF (a versão "Normalized" aplica normalização, o que pode suprimir artefatos de amplitude que seriam sinal).

## 6. Reprodução

```bash
cd asvspoof
.venv/bin/python 00_baixar_amostra.py   # baixa shards + monta 1.200 WAVs (seed 42)
.venv/bin/python 01_treinar_avaliar.py  # features + CV + figuras (~2 min)
```
No Colab: abrir `asvspoof-deteccao.ipynb` (mesmo pipeline, monta a amostra via `datasets`).
