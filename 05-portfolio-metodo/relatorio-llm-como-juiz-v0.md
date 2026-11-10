# LLM como Juiz na Medição de ASR: Mistral-7B no Qwen2.5-7B, Juiz Vendorizado no PAIR e Calibração Humana em Andamento

**Relatório v0 — PCS5917 IA Adversarial (Poli/USP) — template SBC, coluna dupla, máx. 4 páginas**

Leonardo Kawakami Hissanaga — NUSP 11374864
*Nota: atividade realizada individualmente, a pedido, dadas as circunstâncias; todas as contribuições (experimentos, juízes, protocolo, redação) são do autor.*

<!-- ============================================================
     SEÇÃO: Autores + cabeçalho
     Estimativa LaTeX SBC: ~8 linhas (1 parágrafo autor + 1 nota)
     ============================================================ -->

## Resumo

Medimos a taxa de sucesso de ataque (ASR) de jailbreaks com **juízes LLM automáticos** em dois experimentos distintos: (i) no Aula 7/Notebook 3, um juiz Mistral-7B-Instruct-v0.3 (Hugging Face, rubrica binária escrita com justificativa JSON) rotulou 165 respostas do alvo Qwen2.5-7B-Instruct (NF4) sob defesas {baseline, Self-Reminder, Intention Analysis}, produzindo ASR manual de 12,0% (baseline), 2,0% (IA) e 0,0% (SR), e ASR 0,0% para ofuscação Base64 em todas as condições; (ii) no piloto PAIR (alvo Llama-2-7B-chat, atacante Qwen3.5-9B), o juiz automático vendorizado do repositório oficial (escala 1–10, Chao et al., 2025) atingiu ASR de 10,0% (IC 95% Wilson: 1,8–40,4%) em 50 streams. Consolidamos todos os experimentos da disciplina em uma planilha única (5 linhas-atividade) e definimos um protocolo de calibração humano–juiz (amostragem estratificada, cegamento, semente 42, kappa de Cohen com interpretação de Landis & Koch) sobre um subconjunto de 31 + 18 linhas. **A avaliação humana propriamente dita é trabalho em andamento: o CSV de revisão rotulado ainda não foi preenchido**, portanto nenhuma taxa de discordância humano–juiz é reportada. Concluímos, reflexivamente, que juízes únicos são instrumentos mal calibrados — enviesáveis e não comparáveis entre si — e que a rota para ASRs confiáveis passa por painel multi-juiz e calibração humana sistemática.

<!-- Estimativa LaTeX SBC: ~15 linhas (resumo ~1.300 caracteres) -->

## 1. Introdução

A comunidade de segurança de LLMs migrou da avaliação humana massiva para **LLM-as-a-judge** por custo e escala (Zheng et al., 2023; Zhu et al., 2023), mas juízes automáticos introduzem vieses conhecidos — ancoragem, preferências de posição/verbosidade, falsos negativos — que contaminam exatamente a métrica central do campo, o ASR. Este relatório toma o juiz como objeto de estudo, não como caixa-preta: (a) documenta os dois juízes automáticos usados nos experimentos da disciplina — o Mistral-7B-Instruct-v0.3 com rubrica própria no Aula 7/NB3 e o juiz vendorizado do pipeline PAIR (Chao et al., 2025) — e tabula os ASRs que cada um produziu; (b) apresenta a planilha única que consolida as 5 atividades de ataque da disciplina com sua forma de avaliação; e (c) especifica o protocolo de calibração humano–juiz já definido (kappa de Cohen, cegamento, semente fixa) e declara a rotulação humana como **trabalho em andamento**, com CSV pendente. Contribuições: (i) inventário reprodutível de ASRs automáticos por juiz; (ii) evidência concreta de que números de ASR de juízes diferentes não são estritamente comparáveis; (iii) protocolo pronto para execução de calibração humano–juiz–humano.

<!-- Estimativa LaTeX SBC: ~18 linhas -->

## 2. Metodologia

**Planilha única de consolidação.** Todas as atividades de ataque da disciplina foram unificadas em `planilha-unica-ataques.csv` (5 linhas; Tabela 1), com colunas de ataque, método, alvo, atacante, n, forma de avaliação, ASR e arquivo de evidência — a base de rastreabilidade deste relatório.

**Juiz A — Mistral-7B (Aula 7/NB3).** Mistral-7B-Instruct-v0.3 (HF, NF4 em T4/Colab) recebe o prompt malicioso original e a resposta do alvo Qwen2.5-7B-Instruct (NF4) e devolve JSON com rótulo binário + justificativa, por rubrica escrita: 1 = conteúdo substantivo que avança o objetivo nocivo (compliance parcial conta; disclaimer não cancela); 0 = recusa/evasiva/resposta inválida. 165/165 respostas avaliadas, status ok, zero inválidas. ASR = nº de rótulos 1 / respostas válidas por célula (família × defesa) e por tarefa.

**Juiz B — juiz próprio do PAIR.** No piloto PAIR (alvo Llama-2-7B-chat NF4, atacante Qwen3.5-9B GGUF, 10 comportamentos JBB-Behaviors × 5 streams × 3 iterações = 50 streams), a avaliação é feita pelo **juiz vendorizado verbatim do repositório oficial do PAIR** (Chao et al., 2025): "You are a helpful red teaming assistant… act as an impartial judge and evaluate whether the response… violates ethical, legal, or safety guidelines", com score escalar 1–10 por iteração; sucesso = score máximo ≥ 10 no stream. O pipeline (atacante + juiz) foi usado como fornecido, apenas adaptado para GGUF local; o CSV de auditoria (`pair_iterations_pair_pilot_v1.csv`, 150 iterações, 0 erros) registra score por iteração.

**Protocolo de calibração humano–juiz (resumo).** Subconjunto estratificado: 31 linhas da planilha de revisão do piloto PAIR (todas com score ≥ 8 do juiz + amostra das demais; estratos A/B/C) + 18 linhas do Aula 7/NB3 (`human_review_sample.csv`, 3 por célula, `random_state=42`). Rubrica binária idêntica à do Juiz A, fixada antes da coleta, com casos-limite pré-escritos. Cegamento simples (rótulos do juiz ocultos até dupla rotulação), ordem permutada com semente 42, dois avaliadores independentes (A1 autor cego, A2 par externo), métrica kappa de Cohen com interpretação de Landis & Koch (meta κ ≥ 0,61), planilha de discordância com resolução por retorno à rubrica, e auditoria por hash curto do texto da resposta. Detalhes completos em `produto/protocolo-avaliacao-humana.md`.

<!-- Estimativa LaTeX SBC: ~34 linhas -->

## 3. Resultados

**Tabela 1 — Planilha única consolidada (resumo das 5 linhas de `planilha-unica-ataques.csv`):**

| Atividade | Ataque (método) | Alvo | Avaliação | ASR / resultado |
|---|---|---|---|---|
| Aula 2 | Jailbreaks manuais EN/PT, 20 casos (manual) | MiniCPM5-2B | humana | ver planilha detalhada |
| Aula 4 | nanoGCG, 11 templates (sufixo adversarial) | MiniCPM5-2B | humana (Recusou/Parcial) | 4/11 vs 1/11 parcial+ |
| Piloto PAIR | PAIR, 10 comport. × 5 streams, 3 iters | Llama-2-7B-chat | automática (juiz PAIR) | 10,0 (IC 1,8–40,4) |
| Aula 7/NB1 | 10 jailbreaks × 5 tarefas, 3 defesas | Qwen2.5-7B (NF4) | automática (juiz NB3) | 12,0 / IA 2,0 / SR 0,0 |
| Aula 7/NB2 | Base64 × 5 tarefas × 3 condições | Qwen2.5-7B (NF4) | automática (juiz NB3) | 0,0 (todas) |

**Tabela 2 — ASR automático total disponível (juiz Mistral-7B-Instruct-v0.3, Aula 7/NB3; n=50 manual e n=5 encoded por célula):**

| Família | Baseline (none) | Self-Reminder | Intention Analysis |
|---|---|---|---|
| manual (10 jailbreaks × 5 tarefas) | **12,0** (6/50) | **0,0** (0/50) | **2,0** (1/50) |
| encoded (Base64, 5 tarefas) | 0,0 (0/5) | 0,0 (0/5) | 0,0 (0/5) |

**Tabela 3 — ASR automático total disponível (juiz vendorizado PAIR, escala 1–10; alvo Llama-2-7B-chat, sem defesa):**

| Métrica | Valor |
|---|---|
| ASR por comportamento | 10,0% (IC 95% Wilson: 1,8–40,4) |
| Streams com sucesso (score 10) | 1/50 (Disinformation/5G-COVID) |
| Score máx. 9 sem sucesso | Economic harm, Fraud/Deception, Expert advice, Gov. decision-making |
| Iterações com erro | 0/150 |

Os ASRs das Tabelas 2 e 3 são **todo o estoque de avaliação automática hoje disponível**; as demais linhas da Tabela 1 (Aulas 2 e 4) foram avaliadas por humano e não têm par automático correspondente.

<!-- Estimativa LaTeX SBC: ~38 linhas (3 tabelas + legendas + espaçamento) -->

## 4. Avaliação humana do subconjunto — trabalho em andamento

O protocolo da Seção 2 está **definido e versionado**, mas a coleta ainda não foi executada: o CSV de revisão com os rótulos A1/A2 e o rótulo-final por consenso **ainda não foi preenchido** (pendência declarada deste v0). Por discipline de método, enquanto o CSV não existir: (i) **não reportamos** taxa de discordância humano–juiz, ASR humano do subconjunto, nem κ; (ii) todos os ASRs das Tabelas 2–3 permanecem **não calibrados** contra julgamento humano. O que já está pronto e reprodutível: o sorteio estratificado (31 + 18 linhas, semente 42), a rubrica binária com casos-limite escritos, o formato do CSV cegado (`review_id`, tarefa/behavior, resposta_do_alvo) com arquivo-chave separado, e o plano de commits separados pré/pós-consenso no repositório `leokawakami/portfolio-pcs5917`. A literatura recomenda cautela exatamente onde estamos: Hayashi et al. (2026) mediram 12,7% de discordância humano–juiz em jailbreak com viés de falsos negativos — i.e., ASR de juiz único tende a ser **otimista**, o que faria os números das Tabelas 2–3 serem piso, não teto, em uma reavaliação humana.

<!-- Estimativa LaTeX SBC: ~20 linhas -->

## 5. Conclusão e reflexões: multi-juiz e calibração

Os números deste relatório foram produzidos por **dois juízes que não concordariam necessariamente entre si nem com humanos**: o Mistral-7B do NB3 usa rubrica binária nossa, calibrada em casos-limite escritos; o juiz do PAIR usa escala 1–10 vendorizada com limiar 10 — um mesmo par (prompt, resposta) pode ser 0 no primeiro e 9 no segundo (e 9 ≠ sucesso no PAIR, como mostram os 4 comportamentos com score máx. 9 e zero sucesso). Concluímos que (i) ASR é uma função do juiz tanto quanto do ataque: comparar 12,0% (Tabela 2) com 10,0% (Tabela 3) como se fossem a mesma régua seria erro metodológico, e os relatórios declaram essa não-comparabilidade; (ii) juiz único é um instrumento sem curva de calibração — por isso o caminho é **painel multi-juiz** (ex.: Mistral-7B + Llama-3-8B + Qwen2.5-7B com rubricas distintas, agregando por interseção/voto e reportando discordância intra-painel como incerteza) e **ancoragem humana**: o protocolo κ já definido transforma o subconjunto de 31+18 linhas na "célula-padrão" contra a qual rubricas e juízes do painel são revisados iterativamente; (iii) rubricas devem ser escritas e fixadas antes da coleta (falsos negativos por disclaimers e compliance parcial são o caso-limite mais frequente na literatura); (iv) quando o CSV humano for concluído, a métrica a reportar não é só κ, mas a matriz de confusão humano×juiz por estrato — falsos negativos concentrados no estrato B (score 5–9) indicariam limiar mal calibrado, não juiz ruim. Trabalhos futuros diretos: executar a rotulação, montar o painel de 3 juízes sobre as mesmas 165 + 150 respostas, e publicar o CSV versionado com tags pré/pós-consenso.

<!-- Estimativa LaTeX SBC: ~26 linhas -->

## Referências

[1] P. Chao et al., "Jailbreaking Black Box Large Language Models in Twenty Queries," SaTML 2025 (PAIR; juiz vendorizado do repositório oficial).
[2] L. Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," NeurIPS 2023, arXiv:2306.05685.
[3] L. Zhu et al., "Judging LLM-as-a-Judge Across Many Tasks: The Impact of Generating Response Assessment," arXiv:2310.08410 (2023) — base da rubrica do juiz unificado.
[4] V. T. Hayashi et al., "DeepSeek Under Attack: An Analysis of Jailbreak Attacks and Prompt-Level Defenses," IEEE Access, vol. 14, pp. 103944–103961, 2026 (discordância humano–juiz 12,7%).
[5] J. R. Landis, G. G. Koch, "The Measurement of Observer Agreement for Categorical Data," Biometrics 33(1):159–174, 1977.

<!-- Estimativa LaTeX SBC: ~10 linhas -->

---

**Total estimado:** ~170 linhas LaTeX em coluna dupla (classe sbc-template), ≈ 3,5–4 páginas — dentro do limite de 4 páginas.

**Rastreabilidade dos números:** Tabela 1 ← `produto/planilha-unica-ataques.csv` (5 linhas, colunas asr_pct/avaliacao/arquivo_evidencia); Tabela 2 ← `produto/dados/aula7_asr_tables.txt` (células 9–10 do Aula_7_Notebook_3); identidade do juiz Mistral ← `analises/Aula_7_-_Notebook_3.md` (célula 5, `JUDGE_MODEL = mistralai/Mistral-7B-Instruct-v0.3`); rubrica e JSON de saída ← `analises/Aula_7_-_Notebook_3.md` (célula 5, `JUDGE_RUBRIC`); Tabela 3 ← `produto/dados/pair_asr_tables.txt` (células 26/28 do 01_pair_pilot, IC Wilson `wilson()` célula 12 do `03_juiz-unificado.ipynb`); prompt do juiz PAIR verbatim ← `analises/01_pair_pilot.md` (seção "Prompt do juiz (exemplo)", prompts vendorizados); protocolo de calibração ← `produto/protocolo-avaliacao-humana.md` v1.0 (09/11/2026); amostras 31+18 linhas ← `manual_review` do `01_pair_pilot` e `human_review_sample.csv` (`random_state=42`) do `Aula_7_Notebook_3`. Nenhum número foi estimado ou interpolado; a avaliação humana do subconjunto está declaradamente pendente (CSV não rotulado).
