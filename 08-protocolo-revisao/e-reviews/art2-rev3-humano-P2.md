# Formulário de Avaliação — Artigo 2 · Revisor 3 (humano: Leonardo, perfil P2)

> **Sessão:** revisão humana do aluno, 23/11/2026 (antes de ver as demais avaliações — ordem de independência respeitada: este formulário foi preenchido sem acesso aos formulários dos revisores-proxy R1/R2).
> **Artigo:** Liu, Y. et al. *Prompt Injection attack against LLM-integrated Applications* (HOUYI). arXiv:2306.05499v3 (v3 de 29/12/2025). Enquadramento avaliado: categoria **artigo curto** do WCIA 2026 (limite 4 páginas SBC).
> **Revisor:** Leonardo Kawakami Hissanaga — NUSP 11374864 (perfil P2 — Segurança/IA adversarial, pela prática na PCS5917: PAIR, nanoGCG, Base64-encoding, guards, juízes LLM).

## BLOCO A — Metadados

| Campo | Resposta |
|---|---|
| A1. ID do artigo | ART-2 (arXiv:2306.05499v3) |
| A2. Título | Prompt Injection attack against LLM-integrated Applications |
| A3. Autores declarados ao editor | *(campo do editor — invisível ao revisor)* |
| A4. Categoria declarada | (x) Curto *(enquadramento hipotético da atividade; o texto é versão longa de periódico, 18 p.)* |
| A5. Nº de páginas / dentro do limite SBC? | 18 p. — ( ) sim **(x) não** |
| A6. Idioma | ( ) PT **(x) EN** |
| A7. Bloco de tópicos do WCIA | (x) Ataques · (x) Defesa/robustez (avaliação de contramedidas) · ( ) outros |
| A8. Perfil do revisor | ( ) P1 **(x) P2** ( ) P3 |
| A9. Conflito de interesse declarado | (x) nenhum — trabalho não relacionado a coautores; uso do método como material de estudo na disciplina não configura CoI formal (registrado por transparência) |
| A10. Tempo gasto na revisão (min) | ~40 |

## BLOCO B — Scores por dimensão

| Dim | Dimensão | Peso | Nota | Âncora | Comentário |
|---|---|---|---|---|---|
| D1 | Aderência à chamada e formato | 20% | 5 | dentro do escopo com desvios leves | Escopo perfeito (bloco "Ataques"; OWASP LLM01). Desvio grave de formato: 18 p. vs. limite de 4 p. da categoria curta. Como conteúdo, seria condensável; como submissão, estaria fora de formato. |
| D2 | Originalidade | 15% | 8 | novidade notável | Primeira sistematização black-box de prompt injection (análogos de SQLi/XSS: framework/separator/disruptor); estudo-piloto explicando por que heurísticas falham; resultados novos (prompt stealing, uso arbitrário de LLM). Não é direção nova (injeção já era conhecida), então não 9–10. |
| D3 | Rigor metodológico | 25% | 7 | sólido | RQs explícitas, 36 aplicações reais, disclosure responsável validado por 10 vendors, ablação (RQ4), contramedidas testadas. Ressalvas: n=5 tentativas por alvo no piloto com taxa por tentativa não agregada estatisticamente; o 86,1% é "% de aplicações vulneráveis", métrica mais branda que ASR por tentativa — o texto precisa deixar isso explícito; detecção de sucesso do ataque depende de regex/heurística dos autores. |
| D4 | Relevância prática | 15% | 10 | deployável/perturba prática | **Comentário obrigatório (nota ≥9):** impacto direto e verificado — Notion (milhões de usuários), 10 vendors confirmaram, o OWASP listou a classe como risco nº 1. É o tipo de cenário realista que a chamada do WCIA pede. |
| D5 | Reprodutibilidade | 15% | 6 | parte essencial descrita | Componentes e estratégias descritos em detalhe (Tabs. 2–3); repositório público com payloads anunciado. Falta: infra de avaliação contra serviços comerciais é por natureza não reproduzível (APIs mudam — v3 já reporta alvos indisponíveis); sem IC para as taxas. |
| D6 | Escrita | 10% | 7 | clara | Estrutura RQ bem conduzida; prosa densa e por vezes prolixa ("Impressively", "groundbreaking" — autoelogio que revisor marca); figura 1 eficaz. |

**WAvg** = 0,20×5 + 0,15×8 + 0,25×7 + 0,15×10 + 0,15×6 + 0,10×7 = 1,00 + 1,20 + 1,75 + 1,50 + 0,90 + 0,70 = **7,1 / 10**

**Gates de integridade:** nenhum disparado.

## BLOCO C — Julgamento qualitativo

| Campo | Resposta |
|---|---|
| C1 | Estudo empírico de prompt injection contra 36 aplicações LLM reais. Mostra que ataques heurísticos existentes falham na prática (2/10 no piloto), propõe HOUYI — ataque black-box em 3 fases (inferência de contexto, geração de payload em 3 componentes, feedback iterativo) — e reporta 31/36 aplicações vulneráveis, com consequências novas (roubo de prompt, uso gratuito do LLM). |
| C2 | Primeira metodologia sistemática (não-heurística) de prompt injection black-box, validada com disclosure e confirmação de vendors. |
| C3 | A métrica-headline (86,1%) é fração de aplicações com ≥1 sucesso, não taxa por tentativa com intervalo de confiança — superestima a confiabilidade do ataque como quem lê "ASR". |
| C4 | N/A (artigo completo no conteúdo). Para caber em 4 páginas: cortar estudo-piloto para 1 parágrafo + 1 número, condensar Tabs. 4/5 em contagens por categoria, manter Fig. 1, HOUYI de 3 componentes e a tabela de contramedidas. |
| C5 | *(P3 — não aplicável a este revisor)* |

## BLOCO D — Confiança

| Campo | Resposta |
|---|---|
| D-C. Confiança global | **4** |
| Por dimensão | D1 4 · D2 4 · D3 4 · D4 5 · D5 3 · D6 4 |
| N/A | — |

## BLOCO E — Questões para os autores

| # | Questão | Tipo |
|---|---|---|
| Q1 | Reportar taxa de sucesso **por tentativa** (com IC 95%) separada da fração de aplicações vulneráveis; o leitor atual pode ler 86,1% como ASR. | obrigatória |
| Q2 | Formalizar o oráculo de "sucesso" (heurística/regex?) e estimar falsos positivos/negativos dessa detecção, com amostra auditada por humanos. | obrigatória |
| Q3 | Com a indisponibilidade de parte dos alvos entre versões, publicar os diálogos brutos (anonimizados) para permitir reanálise offline. | sugestão |
| Q4 | Discutir custo/latência das defesas testadas — a seção de contramedidas seria mais útil ao WCIA com o trade-off operacional. | sugestão |

## BLOCO F — Risco de texto IA

| Campo | Resposta |
|---|---|
| F1 | Mudança de registro pontual: prosa técnica sóbria na maior parte, com picos de marketing ("Impressively", "groundbreaking", "vibrant ecosystem") — padrão compatível com LLM assistindo redação; nada conclusivo. |
| F2 | Não usei detector. |
| F3 | **médio** — evidência: incoerência de registro descrita em F1 e adjetivação de autoelogio em artigo empírico; sem citações não verificáveis identificadas. |
| F4 | O artigo não declara uso de IA generativa (padrão de 2023; v3 de 2025 atualizada sem declaração). Não é falta sob a política do WCIA vigente se a versão submetida a declarar. |

## BLOCO G — Recomendação

| Campo | Resposta |
|---|---|
| G1 | **( ) A++ (x) A+ Aceite** *(condicionado a reformatação para 4 páginas — gate de formato, não de conteúdo)* |
| G2. WAvg | 7,1 / 10 |
| G3 | Contribuição sólida, empírica e de impacto verificado por vendors; o único obstáculo real à categoria curta é o formato. Rigor bom com duas lacunas mensuráveis (métrica agregada e oráculo de sucesso) que não invalidam as conclusões. |
| G4. Usei IA generativa? | **sim** — nesta sessão o aluno usou ferramentas de IA para extração de texto do PDF e organização de anotações; **notas, âncoras e recomendação são decisão humana** (protocolo §7.1). |
| G5. Trechos a serviço externo? | sim (extração local de texto do PDF próprio; sem envio a serviço que retém para treino) — risco de confidencialidade: baixo (artigo público arXiv). |
| G6. Assinatura (só ao editor) | Leonardo Kawakami Hissanaga — 23/11/2026 |
