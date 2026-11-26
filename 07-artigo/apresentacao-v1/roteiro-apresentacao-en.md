# Apresentação do Artigo — Roteiro v1 (alvo 6:30, slides em INGLÊS)

**Atividade — PCS5917 IA Adversarial (Poli/USP) | Apresentação individual, bonificação com material 100% EN**
Autor: Leonardo Kawakami Hissanaga — NUSP 11374864
Artigo-base: "Quanto custa defender um chatbot bancário? Cascatas de guard models pequenos com escalonamento por confiança" (submissão curta WCIA/SBSeg, anônimo)

**Alvo de tempo:** ~6:30 no plano completo (9 slides). Slides marcados ⏭ são cortáveis/encurtáveis para fechar em ~5 min (cortar slide 3 inteiro e ler só o bullet 1 dos slides 2 e 7).
**Regra de ouro:** falar em bullets, nunca ler texto corrido. Slide = dado; boca = interpretação.
**Todos os números abaixo vêm de:** `NUMEROS_CHAVE_V4.md` (V4), `RELATORIO_G3.md` (G3), `artigo/main.tex` (TEX), `resultados/g3/c1/tabela2.csv` (T2-C1), `resultados/g3/custo_juizes.csv` (CJ), `NUMEROS_CHAVE_G3.md` (G3K). Nenhum número foi inventado.

---

## Slide 1 — Title (0:20)

**No slide:** *How Much Does It Cost to Defend a Banking Chatbot?* / *Small Guard-Model Cascades with Confidence-Based Escalation* — Anonymous Author · WCIA 2026 (SBSeg)

**Fala (bullets):**
- Greeting, course (adversarial AI), anonymous short paper on defense *cost*
- Anchor line: "Guard rails are cheap per call, but nobody was pricing the whole pipeline"
- EN open: "Today I present our cost analysis of guard-model cascades for a banking chatbot"

**Visual:** título + subtítulo; sem abstract.

---

## Slide 2 — Motivation (0:45 | compacta ⏭ 0:25)

**No slide:** *Why price the defense?* — banking chatbots use account tools · AI-enabled breaches ≈ US$4.99M avg; US$6.3M financial · 20%+ orgs report AI-related breaches · guard models 22M–4B params: cheap filter, published numbers diverge

**Fala (bullets):**
- Banking assistant with tool access = natural target: jailbreaks, prompt injection, fraud help (TEX §1)
- Cost of failure is concrete: IBM 2026: US$4.99M breach average, US$6.3M financial, AI-enabled ≈ US$6M (TEX §1)
- Small guard models (22M–4B) promise a cheap input filter; self-reported scores diverge across benchmarks (TEX §1)
- The expensive piece: a big LLM judge: should it see every message or only the hard ones? (TEX §1)

**Visual:** 3 caixas de custo + seta "who pays per message?".

---

## Slide 3 — Research question & contributions (0:40 | ⏭ cortar inteiro p/ 5 min)

**No slide:** *Question:* when does a cascade beat guard-only or judge-only, in cost? Contributions: independent multi-guard measurement (EN+PT) · parametric expected-cost model, 3-way rule · optimal-configuration map over (π, L)

**Fala (bullets):**
- RQ verbatim from paper: for which attack prevalence π and loss L is the *cascade* cheaper than (a) small guard only or (b) big judge only? (TEX §1)
- C1: same-protocol measurement of 5–7 open guards, EN + PT, banking scenario (TEX §1)
- C2: expected-cost model with release / escalate / block rule (TEX §1, eq. 1)
- C3: optimum map over (π, L) for AI-security budgeting (TEX §1)

---

## Slide 4 — Method: the cascade (0:55)

**No slide:** *T0 Sheltron-68M (CPU) → T1 Qwen3Guard-4B → LLM judge*; band [τ_low, τ_high]: release / escalate / block. C = c_guard + r·c_judge + π·FNR·L + (1−π)·FPR·C_fp — r (escalation share) is *measured*

**Fala (bullets):**
- Tier 0: 86M-class CPU encoder front line; the winning route uses Sheltron 68M, p50 ≈ 8.9 ms on L4 (T2-C1 / G3 §4)
- Tier 1: Qwen3Guard-4B re-scores uncertain band; Tier 2: LLM judge (GLM-5.3-Flash API, US$95.18 per 1M requests at list price) (CJ / G3 §3)
- Three-way rule from calibrated probability: release below τ_low, block above τ_high, escalate in between (TEX §3.5)
- Cost equation: guard + r·judge + missed-attack loss + false-block cost; thresholds picked on calibration split only, seed 42 (TEX §3.2, §3.5)

**Visual:** pipeline horizontal com as 3 caixas e a banda de escalada destacada.

---

## Slide 5 — Experimental setup (0:40)

**No slide:** *Test sets:* EN n=682 (314 attacks / 368 benign) · PT n=271 · External: 3,080 fresh Banking77 + 1,056 FinVault. *Reference scenario C1:* π=1%, L=US$63M×20%, C_fp=US$2.70, 15M msg/month, AWS L4 sa-east-1

**Fala (bullets):**
- Corpus: jailbreaks (DAN/WildJailbreak), injections, synthetic financial attacks D4, real banking traffic BANKING77, hard negatives (TEX §3.2)
- EN test 682 samples, PT 271; thresholds fixed on 30% calibration, test used once (V4 / TEX §3.2)
- External stress: 3,080 new benign Banking77 + 1,056 FinVault attacks; thresholds frozen (G3 §2, §5)
- Production scenario C1: AWS L4 g6.xlarge US$1.368/h, 15M messages/month, π=1% (G3 §4 / V4 header)

---

## Slide 6 — Headline result: cost × recall (1:10 | não cortar)

**No slide (tabela):**

| Route (EN, rule a) | Sensitivity | Specificity | Cost US$/1M |
|---|---|---|---|
| **Cascade sheltron-68M → Q3G-4B → judge** | **0.825 [0.778–0.865]** | **0.986 (FP 5/368)** | **146,846** |
| Qwen3Guard-4B alone | 0.790 [0.741–0.834] | 0.981 (FP 7/368) | 183,785 |
| Judge alone (T2) | 0.949 | 0.891 (FP 40) | 322,741 |

**Fala (bullets):**
- Cascade = cheapest SLA-eligible route at US$146,846/1M, 20% cheaper than best guard-only (T2-C1)
- Judge-only: best sensitivity 0.949 but 2.2× the cost and specificity 0.891, blocking ~40 of 368 legit users (V4 §1 / T2-C1)
- Cascade beats guard-only by +3.5 pp sensitivity, paired CI [−0.6, +7.6], McNemar p=0.135: honest, not significant on our test (V4 §5)
- Escalation is rare: r = 11.3% raw band but only ~1% reaches the judge at π=1%; system p95 latency 191.7 ms (T2-C1)
- On 3,080 unseen benign banking messages: specificity 0.9997: ≈4,821 blocked clients/month at 15M msgs, judge escalation 0.16% (G3K / G3 §5)

**Visual:** tabela grande; seta "cheapest" na linha da cascata.

---

## Slide 7 — Sensitivity: when does the cascade win? (0:50 | compacta ⏭ 0:25)

**No slide (figura sens × clientes bloqueados + bullets):** cascade wins 13/24 cells at π=0.1% · 7/24 at π=1% · 4/24 at π=5% (EN). PT: no cascade meets 300 ms SLA. L4→H100 changes cost by only 0.4%

**Fala (bullets):**
- Grid over π × incident-probability × blocked-client cost: cascade wins 13/24 EN cells at π=0.1%, dropping to 7/24 at π=1% and 4/24 at π=5% (G3K item 6)
- Above ~1% prevalence, cheap guard-only (Sheltron) wins most cells (G3K item 6)
- PT: escalation volume breaks the 300 ms SLA; the winner is Qwen3Guard-4B alone, US$196,733/1M (G3 §4)
- Hardware is not the lever: L4→H100 moves total cost 146,846→147,462 (+0.4%); defense is judge-API dominated (G3 §4)
- Threshold choice is unstable across calibration bootstraps (test sensitivity 0.75–0.95); the single winner is not uniquely optimal (G3 App. G2)

**Visual:** `fig-sens-bloqueados` (sensibilidade × clientes bloqueados/mês, π=1%, C1 elegível ao SLA destacado).

---

## Slide 8 — Limitations (0:40)

**No slide:** external jailbreak recall is low (FinVault 18%; 8.6% jailbreak); PT cascades miss the 300 ms SLA; D4 attacks are LLM-generated; L4 latencies estimated, not measured; π and L are scenario parameters

**Fala (bullets):**
- Hardest honest number: on external FinVault the cascade detects only 18% overall, 8.6% on jailbreaks: a harder attack regime than our corpus (G3 §5)
- Threshold instability (slide 7) limits how far to trust the winner route (G3 App. G2)
- L4 p95 is extrapolated from RTX 3090 measurements, range 52–1,742 ms, measurement pending (G3K item 7)
- Synthetic D4 and LLM-translated PT corpus; π/L are parameters, not measurements (TEX §5)

---

## Slide 9 — Conclusion (0:30)

**No slide:** cascade = cheapest SLA-eligible defense at low prevalence (π ≤ 0.1%); escalation is rare (≈1%), so paying the judge rarely is real savings; cost is API-dominated: price the judge, not the GPU. Code + data released for reproducibility

**Fala (bullets):**
- Answer to the RQ: cascade wins when attacks are rare; guard-only wins when they are common (G3K item 6)
- Confidence escalation cuts judge traffic to ~1% at π=1%; the saving mechanism is measured, not assumed (T2-C1)
- Budget advice: L4 vs H100 changes nothing (+0.4%); optimize judge pricing/routing first (G3 §4)
- Closing line: "Defend cheap where you can, escalate rarely, and price the escalation."

**Tempos:** 0:20 + 0:45 + 0:40 + 0:55 + 0:40 + 1:10 + 0:50 + 0:40 + 0:30 = **6:30**
**Modo 5 min:** cortar slide 3 (−0:40), slides 2 e 7 compactos (−0:40), slide 6 vira leitura das 3 linhas da tabela + 2 bullets (−0:20) → ≈ **4:50–5:05**

---

## Mapa de números → origem

| Número | Arquivo |
|---|---|
| 0.8248/0.9864, FN 55/314 FP 5/368; isolado 0.7898/0.9810; T2 0.949/0.891; Δ+3.5pp IC[−0.6;+7.6] p=0.135 | `NUMEROS_CHAVE_V4.md` §1, §5 |
| US$146,846/183,785/322,741 por 1M; r=0.1129; p95 191.7 ms; PT 196,733 | `resultados/g3/c1/tabela2.csv` |
| π=1%, p_inc=1e-5, C_fp=US$2.70, 15M msg/mês | `NUMEROS_CHAVE_V4.md` cabeçalho |
| US$95.18/1M juiz T2; US$1.368/h L4; PT sem cascata no SLA; C1→C2 +0.4%; D5x esp 0.9997, 4,821 bloqueios/mês, escalada 0.16%; FinVault 0.180/0.086; sheltron L4 p50 8.9 ms; PT p95 172 ms medido | `RELATORIO_G3.md` §3–§5 |
| 13/24, 7/24, 4/24 (EN); 1/24, 1/24, 0/24 (PT) | `NUMEROS_CHAVE_G3.md` item 6 |
| L4 p95 estimada 52–1.742 ms; τ instável (0.75–0.95) | `NUMEROS_CHAVE_G3.md` item 7; `RELATORIO_G3.md` Ap. G2 |
| US$4.99M / US$6.3M / 20%+ violações; n=682/271; equação de custo; modelo de dados | `artigo/main.tex` §1, §3 |
| 1959 ms p95 cascata PT 2s | `NUMEROS_CHAVE_V4.md` §2 |
