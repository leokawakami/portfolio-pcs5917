#!/usr/bin/env python3
"""Build slides.pptx for the PCS5917 article presentation (EN slides)."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

BG = RGBColor(0x0D, 0x11, 0x17)
INK = RGBColor(0xE6, 0xED, 0xF3)
DIM = RGBColor(0x8B, 0x94, 0x9E)
ACCENT = RGBColor(0x58, 0xA6, 0xFF)
GOLD = RGBColor(0xE3, 0xB3, 0x41)
RED = RGBColor(0xF8, 0x51, 0x49)
LINE = RGBColor(0x30, 0x36, 0x3D)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
W, H = prs.slide_width, prs.slide_height


def add_slide():
    s = prs.slides.add_slide(BLANK)
    r = s.shapes.add_shape(1, 0, 0, W, H)  # rectangle bg
    r.fill.solid(); r.fill.fore_color.rgb = BG
    r.line.fill.background()
    r.shadow.inherit = False
    return s


def tb(slide, l, t, w, h):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    return tf


def para(tf, text=None, size=20, bold=False, color=INK, first=False, align=PP_ALIGN.LEFT, space_after=8, runs=None):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    if runs:  # list of (text, color, bold)
        for txt, col, bd in runs:
            r = p.add_run(); r.text = txt
            r.font.size = Pt(size); r.font.color.rgb = col; r.font.bold = bd
    else:
        r = p.add_run(); r.text = text
        r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color
    return p


def kicker_title(slide, kicker, title, sub=None):
    tf = tb(slide, Inches(0.7), Inches(0.4), Inches(12), Inches(1.5))
    para(tf, kicker.upper(), size=13, bold=True, color=ACCENT, first=True, space_after=4)
    para(tf, title, size=30, bold=True, color=INK, space_after=4)
    if sub:
        para(tf, sub, size=15, color=DIM)


def bullets(slide, items, l=Inches(0.8), t=Inches(2.0), w=Inches(11.8), h=Inches(4.8), size=19):
    tf = tb(slide, l, t, w, h)
    for i, it in enumerate(items):
        if isinstance(it, list):
            if it[0][0] == "▸ ":
                runs = it
            else:
                runs = [("▸ ", ACCENT, True)] + it
            para(tf, size=size, first=(i == 0), runs=runs, space_after=12)
        else:
            para(tf, "▸ " + it, size=size, first=(i == 0), space_after=12)


def footer(slide, text, timing):
    tf = tb(slide, Inches(0.7), Inches(6.95), Inches(12), Inches(0.4))
    para(tf, text + "   ·   " + timing, size=10, color=DIM, first=True)


# ---------- 1 TITLE ----------
s = add_slide()
tf = tb(s, Inches(1.0), Inches(1.9), Inches(11.3), Inches(3.6))
para(tf, "SHORT PAPER · WCIA 2026 (SBSEG) · PCS5917 ADVERSARIAL AI", size=13, bold=True, color=ACCENT, first=True, space_after=14)
para(tf, "How Much Does It Cost to Defend a Banking Chatbot?", size=36, bold=True, color=INK, space_after=10)
para(tf, "Small Guard-Model Cascades with Confidence-Based Escalation", size=22, bold=True, color=ACCENT, space_after=16)
para(tf, "Anonymous author for blind review — identification removed for double-blind evaluation", size=15, color=DIM, space_after=8)
para(tf, "All figures from the paper's frozen dataset and reproduction scripts (G3/V4 rounds).", size=13, color=DIM)
footer(s, "Slide 1 · Title", "0:20")

# ---------- 2 MOTIVATION ----------
s = add_slide()
kicker_title(s, "Motivation", "Why price the defense?")
bullets(s, [
    [("▸ ", ACCENT, True), ("Banking assistants expose account tools → natural target for jailbreaks, prompt injection, fraud help", RED, False)],
    [("▸ ", ACCENT, True), ("AI-enabled breaches average ", INK, False), ("US$ 4.99 M", GOLD, True), ("; financial sector ", INK, False), ("US$ 6.3 M", GOLD, True), ("; 20%+ of orgs report AI-related breaches (IBM, 2026)", INK, False)],
    [("▸ ", ACCENT, True), ("Small guard models (", INK, False), ("22 M–4 B", GOLD, True), (" params) promise a cheap filter — self-reported scores diverge across benchmarks", INK, False)],
    "The expensive piece is the LLM judge: every message, or only the hard ones?",
], t=Inches(1.9), h=Inches(2.6), size=20)
tf = tb(s, Inches(0.8), Inches(4.7), Inches(11.8), Inches(1.9))
para(tf, "Guard model: 86 M-class encoder ≈ cents per call — recall varies by benchmark and language", size=16, color=DIM, first=True, space_after=6)
para(tf, "LLM judge: strong and language-agnostic — priced per token on every message", size=16, color=DIM, space_after=6)
para(tf, "Our question: what does the whole pipeline cost per million messages?", size=16, bold=True, color=ACCENT)
footer(s, "Slide 2 · Motivation", "0:45 · compact 0:25")

# ---------- 3 RQ ----------
s = add_slide()
kicker_title(s, "Research question", "When does a cascade beat guard-only or judge-only?")
tf = tb(s, Inches(1.2), Inches(2.1), Inches(10.9), Inches(1.2))
para(tf, "For which attack prevalence π and per-incident loss L is a guard → judge cascade", size=20, color=GOLD, first=True, align=PP_ALIGN.CENTER, space_after=2)
para(tf, "cheaper than (a) guard-only or (b) judge-only?", size=20, color=GOLD, align=PP_ALIGN.CENTER)
bullets(s, [
    [("▸ 1 · Measurement: ", ACCENT, True), ("5–7 open guard models, one protocol, banking scenario, EN + PT", INK, False)],
    [("▸ 2 · Cost model: ", ACCENT, True), ("parametric expected cost, three-way rule — release / escalate / block", INK, False)],
    [("▸ 3 · Optimum map: ", ACCENT, True), ("best configuration over the (π, L) grid for AI-security budgeting", INK, False)],
], t=Inches(3.6), h=Inches(3.2), size=20)
footer(s, "Slide 3 · Question & contributions · cuttable in 5-min mode", "0:40")

# ---------- 4 METHOD ----------
s = add_slide()
kicker_title(s, "Method", "A three-tier cascade with a confidence band")
boxes = [
    ("T0 · Sheltron-68M", "CPU/L4 encoder front line\np50 ≈ 8.9 ms · US$ 86.7/1M"),
    ("T1 · Qwen3Guard-4B", "re-scores the uncertain band\non the same GPU tier"),
    ("Judge · LLM API", "GLM-5.3-Flash\nUS$ 95.18 per 1M requests"),
]
for i, (h, b) in enumerate(boxes):
    x = Inches(0.8 + i * 4.2)
    r = s.shapes.add_shape(5, x, Inches(2.0), Inches(3.6), Inches(1.5))
    r.fill.solid(); r.fill.fore_color.rgb = RGBColor(0x16, 0x1B, 0x22)
    r.line.color.rgb = ACCENT; r.shadow.inherit = False
    tf = r.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run = p.add_run(); run.text = h; run.font.size = Pt(17); run.font.bold = True; run.font.color.rgb = ACCENT
    for line in b.split("\n"):
        p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
        run = p2.add_run(); run.text = line; run.font.size = Pt(14); run.font.color.rgb = INK
    if i < 2:
        tfa = tb(s, x + Inches(3.6), Inches(2.45), Inches(0.6), Inches(0.6))
        para(tfa, "→", size=28, bold=True, color=GOLD, first=True, align=PP_ALIGN.CENTER)
bullets(s, [
    [("▸ Band [τ", INK, False), ("low", DIM, False), (", τ", INK, False), ("high", DIM, False), ("]: ", INK, False), ("release", RGBColor(0x3F, 0xB9, 0x50), True), (" below · ", INK, False), ("block", RED, True), (" above · ", INK, False), ("escalate", GOLD, True), (" in between", INK, False)],
    "Thresholds from calibrated probabilities; picked on a 30% calibration split — test used once, seed 42",
], t=Inches(3.9), h=Inches(1.5), size=18)
tf = tb(s, Inches(1.2), Inches(5.5), Inches(10.9), Inches(0.8))
para(tf, "C = c_guard + r·c_judge + π·FNR·L + (1−π)·FPR·C_fp      —  r = measured escalation share",
     size=17, color=GOLD, first=True, align=PP_ALIGN.CENTER)
footer(s, "Slide 4 · Cascade & cost equation", "0:55")

# ---------- 5 SETUP ----------
s = add_slide()
kicker_title(s, "Experimental setup", "Frozen corpus, one production scenario")
cards = [
    ("Test sets", "EN n=682 (314 attacks / 368 benign)\nPT n=271 (140 / 131)\nDAN, WildJailbreak, injections, synthetic banking, Banking77, hard negatives"),
    ("External stress", "3,080 fresh benign Banking77 sentences\n1,056 FinVault attacks (injection / jailbreak / financial)\nThresholds frozen from calibration"),
    ("Scenario C1", "π = 1% · p_inc = 1e-5 · C_fp = US$ 2.70\n15 M messages/month\nAWS L4 g6.xlarge sa-east-1, US$ 1.368/h"),
]
for i, (h, b) in enumerate(cards):
    x = Inches(0.8 + i * 4.2)
    tf = tb(s, x, Inches(2.0), Inches(3.7), Inches(3.0))
    para(tf, h, size=17, bold=True, color=ACCENT, first=True, space_after=8)
    for line in b.split("\n"):
        para(tf, line, size=14, color=INK, space_after=4)
bullets(s, [
    "Latencies measured batch=1 on RTX 3090; L4 numbers extrapolated from spec ratios (flagged)",
    "Judge cost = list price × measured tokens (424 in / 63 out for the reference judge)",
], t=Inches(5.1), h=Inches(1.7), size=17)
footer(s, "Slide 5 · Setup", "0:40")

# ---------- 6 HEADLINE ----------
s = add_slide()
kicker_title(s, "Headline result · EN test · reference scenario C1", "Cascade is cheapest — and more accurate than guard-only")
rows = [
    ("Route", "Sensitivity", "Specificity", "Cost US$/1M", "p95"),
    ("Cascade Sheltron-68M → Q3G-4B → judge", "0.825 [.778–.865]", "0.986 (FP 5/368)", "146,846", "192 ms"),
    ("Qwen3Guard-4B alone", "0.790 [.741–.834]", "0.981 (FP 7/368)", "183,785", "187 ms"),
    ("LLM judge alone", "0.949", "0.891 (FP 40/368)", "322,741", "2.7 s"),
]
tbl = s.shapes.add_table(4, 5, Inches(0.7), Inches(2.0), Inches(11.9), Inches(1.9)).table
widths = [Inches(4.6), Inches(2.1), Inches(2.1), Inches(1.9), Inches(1.2)]
for j, wd in enumerate(widths):
    tbl.columns[j].width = wd
for i, row in enumerate(rows):
    for j, val in enumerate(row):
        cell = tbl.cell(i, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(0x16, 0x1B, 0x22) if i else BG
        tf = cell.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]
        if j: p.alignment = PP_ALIGN.RIGHT
        run = p.add_run(); run.text = val
        run.font.size = Pt(14 if i else 12)
        run.font.bold = (i == 1) or (i == 0)
        col = DIM if i == 0 else (GOLD if (i == 1 and j == 3) else (RED if (i == 3 and j in (2, 3, 4)) else INK))
        run.font.color.rgb = col
bullets(s, [
    "Only ~1% of traffic reaches the judge at π=1% (r = 11.3% of the band, ≈1% overall)",
    "+3.5 pp sensitivity vs guard-only: CI [−0.6, +7.6], McNemar p = 0.135 — not significant on our test",
    "3,080 unseen benign banking messages: specificity 0.9997 — ≈4,821 blocked clients/month, judge escalation 0.16%",
], t=Inches(4.3), h=Inches(2.5), size=17)
footer(s, "Slide 6 · Cost × recall — do not cut", "1:10")

# ---------- 7 SENSITIVITY ----------
s = add_slide()
kicker_title(s, "Sensitivity analysis", "The cascade wins when attacks are rare")
s.shapes.add_picture("fig-sens-bloqueados.png", Inches(0.7), Inches(1.95), width=Inches(6.6))
tf = tb(s, Inches(0.7), Inches(5.95), Inches(6.6), Inches(0.8))
para(tf, "Sensitivity vs legitimate clients blocked per month (15 M msgs, π=1%); C1 (L4) SLA-eligible routes highlighted.", size=11, color=DIM, first=True)
bullets(s, [
    [("▸ Cascade wins ", INK, False), ("13/24", GOLD, True), (" EN cells at π=0.1% — ", INK, False), ("7/24", GOLD, True), (" at π=1%, ", INK, False), ("4/24", GOLD, True), (" at π=5%", INK, False)],
    "Above ~1% prevalence, cheap guard-only takes most cells",
    "PT: escalation volume breaks the 300 ms SLA — winner is guard-only, US$ 196,733/1M",
    "L4 → H100 moves cost only +0.4%: defense is judge-API dominated",
    "Thresholds unstable across bootstraps (sens. 0.75–0.95): winner not uniquely optimal",
], l=Inches(7.5), t=Inches(2.0), w=Inches(5.4), size=15)
footer(s, "Slide 7 · Sensitivity · compact 0:25", "0:50")

# ---------- 8 LIMITATIONS ----------
s = add_slide()
kicker_title(s, "Limitations — the honest slide", "What these numbers do not show")
bullets(s, [
    [("▸ External jailbreak recall is low: FinVault overall ", INK, False), ("18%", RED, True), (", jailbreak subset ", INK, False), ("8.6%", RED, True), (" — a harder attack regime than our corpus", INK, False)],
    "L4 p95 is extrapolated (52–1,742 ms range), not measured on real L4 hardware",
    "Synthetic financial attacks (LLM-generated D4) and machine-translated PT corpus",
    "π and L are scenario parameters, not measurements — the map is a budgeting tool, not a forecast",
    "Judge family bias checked: no self-preference detected, but CIs are wide (n=69/199)",
], t=Inches(2.1), size=20)
footer(s, "Slide 8 · Limitations", "0:40")

# ---------- 9 CONCLUSION ----------
s = add_slide()
kicker_title(s, "Conclusion", "Defend cheap where you can, escalate rarely, price the escalation")
bullets(s, [
    [("▸ Cascade is the ", INK, False), ("cheapest SLA-eligible defense at low prevalence", GOLD, True), (" (13/24 cells at π=0.1%); guard-only wins when attacks are common", INK, False)],
    [("▸ Confidence escalation cuts judge traffic to ", INK, False), ("≈1%", GOLD, True), (" at π=1% — savings measured, not assumed", INK, False)],
    "Budget advice: hardware is not the lever (+0.4% L4→H100) — optimize judge pricing and routing first",
    "Code, datasets and prompts released for reproducibility",
], t=Inches(2.2), h=Inches(3.4), size=20)
tf = tb(s, Inches(0.8), Inches(5.9), Inches(11.8), Inches(0.6))
para(tf, "Thank you — questions welcome.", size=18, color=DIM, first=True, align=PP_ALIGN.CENTER)
footer(s, "Slide 9 · Conclusion", "0:30")

prs.save("slides.pptx")
print("saved slides.pptx,", len(prs.slides.slides if hasattr(prs.slides,'slides') else list(prs.slides)), "slides")
