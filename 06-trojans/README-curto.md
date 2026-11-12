# 06 — Trojans (geração e detecção)

Golden model: secworks/aes (MIT). Dataset: 10 legítimas + 10 trojans gerados por LLM,
20/20 compilando com Icarus Verilog 12.0. Planilha anonimizada (semente 42) em
`planilha_anonima.csv`; gabarito em `resultados/gabarito.csv` (publicado — atividade
entregue sem troca intergrupos, logística a confirmar com o professor).

Detecção **cega** (detetor nunca vê o gabarito; protocolo em `04-protocolo-deteccao.md`):
- v1 (prompt genérico, Qwen3.8 local 262K): acurácia **90%**, recall **80%**, precisão
  **100%**, FP 0, FN 2 → `resultados/score_deteccao_v1.csv`
- v2 (checklist de invariantes criptográficos): recall **100%**, precisão 77%, FP 3
  → comparativo e leitura purple team em `relatorio-trojans-v0.md` §4.1.

Colab do segundo detector independente (Qwen2.5-7B NF4 em T4):
`04_deteccao-trojans.ipynb`. Ver `README.md` para o método completo.
