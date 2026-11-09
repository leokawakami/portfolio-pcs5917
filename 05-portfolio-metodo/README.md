# 05 – Método do Portfólio & Consolidação

## O que foi feito
Consolidação de **todos os ataques executados** no semestre em uma planilha única, com autoria, método, modelo, avaliação e ASR por linha — insumo das atividades "LLM como Juiz" e "Defesas a Nível de Prompt", e spine do portfólio.

## Método
Cada experimento (manual, nanoGCG, PAIR, encoded) foi normalizado em uma linha: `atividade_origem, aula, data, ataque, metodo, modelo_alvo, modelo_atacante, n_ataques, avaliacao, asr_pct, sucesso_total, arquivo_evidencia, autoria`. Dois protocolos de avaliação coexistem e são declarados por linha: **humana** (Aulas 2 e 4) e **juiz automático** (PAIR e Aula 7) — a comparação entre eles é uma limitação documentada.

## Modelos
Todos os alvos do portfólio: MiniCPM5-2B, Phi-3-mini-4k (reprodução), Llama-2-7B-Chat, Qwen2.5-7B-Instruct.

## Resultados-chave
- [`planilha-unica-ataques.csv`](planilha-unica-ataques.csv): 5 experimentos, 106 casos executados (20 + 11 + 50 + 15 + 10 comportamentos PAIR), ASR por linha.
- Faixa de ASR observada: 0.0% (Base64/Self-Reminder) a 12.0% (manual baseline em Qwen2.5).
- Todos os registros com autoria individual (Leonardo) e trilha de evidência (notebook de origem).

## Arquivos
- Planilha: `planilha-unica-ataques.csv` (aqui; cópia .xlsx na release ZIP)
- _Placeholder_: CSVs derivados por atividade serão upados nas pastas `01-` a `04-` e linkados daqui.
