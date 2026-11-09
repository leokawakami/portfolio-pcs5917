# 03 – PAIR: ataque automático preto-caixa

## O que foi feito
Piloto do ataque automático **PAIR** (Chao et al., "Jailbreaking LLMs in the Wild") de ponta a ponta em Colab (GPU L4): smoke test da infra (21/10) + execução completa (22/10) com **10 comportamentos do JBB-Behaviors × 5 streams × 3 iterações** = 150 linhas de diálogo, em inglês.

## Método
Loop PAIR com 3 papéis: **atacante** Qwen3.5-9B (GGUF via llama-cpp-python, fork JamePeng para arquitetura qwen35) gera/crossa/muta prompts; **alvo** Llama-2-7B-Chat (4-bit, gated) responde; **juiz automático** (classificador HF) pontua a resposta (0–10) e alimenta o próximo turno. Decisão de sucesso pelo juiz. CSV de revisão manual exportado (subconjunto de 31 linhas para rotulagem humana — pendente no período do piloto).

## Modelo
- **Alvo:** Llama-2-7B-Chat (4-bit)
- **Atacante:** Qwen3.5-9B (GGUF) — black-box, sem gradientes
- **Juiz:** classificador automático (AttackerBench/HF)

## Resultados-chave
- **ASR do juiz = 10.0%** (1 de 10 comportamentos; IC 95%: 1.8–40.4%)
- **1/50 streams** com sucesso; 0 erros de iteração nas 150 linhas
- Único comportamento quebrado: **Disinformation** (score máximo 10); score 9 alcançado sem sucesso em Economic harm, Fraud/Deception, Expert advice e Government decision-making
- Elo fraco documentado: revisão humana do subconjunto ficou em 0/31 rótulos → comparação ASR humano × automático pendente

## Arquivos
- Notebooks: `00_smoke_test.ipynb`, `01_pair_pilot.ipynb`
- CSVs: _placeholder_ — `pair_iterations_pair_pilot_v1.csv`, `pair_review_manual.csv` (a subir via release ZIP).
