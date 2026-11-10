# Apresentação do Artigo — Roteiro v0 (5–8 min, bilíngue slide-a-slide)

**Atividade 5 — PCS5917 IA Adversarial (Poli/USP) | Apresentação individual, bonificação se em inglês**
Autor: Leonardo Kawakami Hissanaga — NUSP 11374864
Artigo-base: `produto/relatorio-defesas-v0.md` ("Defesas a Nível de Prompt contra Jailbreaks em Qwen2.5-7B-Instruct")

**Alvo de tempo:** ~6:30 no plano completo (8 slides + Q&A buffer). Cada slide traz o tempo "full" e a versão "compacta" para fechar em 5 min (cortar os slides marcados ⏭ ou ler só o bullet 1).
**Regra de ouro:** falar em bullets, nunca ler texto corrido. Slide = dado; boca = interpretação.

---

## Slide 1 — Título / Title (0:20)

**Título no slide:** *Defesas a Nível de Prompt contra Jailbreaks em LLMs Abertos: ASR com Self-Reminder e Intention Analysis* | *Prompt-Level Defenses Against Jailbreaks in Open LLMs: ASR with Self-Reminder and Intention Analysis*

**Fala (bullets):**
- Quem sou, disciplina, artigo apresentado
- Uma frase-âncora: "Defesas de prompt anulam jailbreaks manuais num Qwen2.5-7B — mas ataques adaptativos ficam sem teste"
- Versão EN de abertura: "Today I'll show how two prompt-level defenses perform against manual and automatic jailbreaks on open-weight LLMs."

**Visual:** título + 1 logo (USP/Poli) + lista curta dos modelos-alvo (Qwen2.5-7B-Instruct, Llama-2-7B-chat, MiniCPM5-2B). Nada de abstract no slide.

---

## Slide 2 — Motivação e contexto / Motivation (0:45 | compacta 0:30)

**Título:** *Por que defesas de prompt? | Why Prompt-Level Defenses?*

**Fala (bullets):**
- Jailbreak = prompting que induz LLM alinhado a conteúdo nocivo **sem tocar nos pesos**
- Defesas de prompt (Self-Reminder, Intention Analysis) rodam **só em inferência** — baratas, sem re-treino
- Ponto de partida: estudo de caso USP/Hayashi et al. 2026 (IEEE Access) sobre DeepSeek-R1/V3
- Nosso gap: reproduzir o protocolo num **alvo aberto de 7B** + adicionar vetor Base64 (família CipherChat) não coberto em modelos pequenos
- Citar de passagem: Xie et al. 2023 (SR, Nature MI), Zhang et al. 2025 (IA, COLING), Chao et al. 2025 (PAIR)

**Visual:** diagrama de 1 linha do fluxo do ataque (usuário → jailbreak → LLM alinhado → resposta nociva?) com as duas defesas encaixadas como caixas no prompt. Fonte: `produto/01-estudo-defesas.md` (descrição dos mecanismos SR/IA).

---

## Slide 3 — Método em 4 blocos / Method in 4 Blocks (0:50)

**Título:** *Metodologia | Methodology*

**Fala (bullets):**
- **Alvo:** Qwen2.5-7B-Instruct NF4 (bitsandbytes) em T4/Colab; auxiliares: Llama-2-7B-chat (PAIR), MiniCPM5-2B (nanoGCG, Aula 4)
- **Ataques:** (a) 10 jailbreaks manuais × 5 tarefas = 50 queries/condição; (b) Base64 (5); (c) automático: PAIR (50 streams) + nanoGCG (11 casos)
- **Defesas isoladas:** {baseline, Self-Reminder, Intention Analysis one-pass}
- **Juiz:** Mistral-7B-Instruct-v0.3, rubrica binária escrita (compliance parcial = 1; disclaimer não cancela recusa); 165/165 respostas avaliadas sem falha
- ASR = sucessos / respostas válidas, por célula (família × defesa)

**Visual:** tabela-resumo 3 linhas (ataque × alvo × n) — reconstruir da seção 2 do relatório; ícones de pipeline: ataque → defesa → juiz → ASR.

---

## Slide 4 — Resultado principal: defesas × ASR / Headline Result (1:00 | não cortar)

**Título:** *Self-Reminder zerou os jailbreaks manuais | Self-Reminder Zeroed Manual Jailbreaks*

**Fala (bullets):**
- Baseline manual: **ASR 12,0% (6/50)**
- Self-Reminder: **0,0% (0/50)** — zeração total
- Intention Analysis: **2,0% (1/50)**
- Base64: **0,0% em TODAS as condições, inclusive baseline** — surpresa do estudo
- Interpretação 1: coerente com a literatura (Zhang: Llama2-7B 23,5%→1,03% com SR)
- Interpretação 2: IA (2%) > SR (0%) está **dentro do ruído** com n=50 (±2 p.p. por resposta)

**Visual:** **Tabela 1 do relatório v0** (ASR família × defesa) como slide inteiro, números grandes; setas 12→0 e 12→2. Se houver espaço, mini-barra da Tabela 2 (por tarefa: phishing e aquecimento global puxam o baseline a 20%).
Fonte dos números: `produto/dados/aula7_asr_tables.txt` (NB3 cells 9–10).

---

## Slide 5 — Por que Base64 falhou / Why Base64 Failed (0:45 | compacta ⏭ 0:20, virar fala do slide 4)

**Título:** *Ofuscação Base64: ineficaz em alvos treinados em código | Base64 Obfuscation: Ineffective on Code-Trained Targets*

**Fala (bullets):**
- Hipótese: Qwen2.5 decodifica Base64 com folga (treinamento pesado em código) → payload decodada continua nociva → alinhamento recusa igual
- Ofuscação por codificação só ajuda contra alvos com **capacidade fraca de decodificação**
- Zhang et al. evitaram testar CipherChat em 7B (respostas inválidas); nosso dado: custo-benefício baixo para alvos com código
- Caveat honesto: n=5 por célula — evidência preliminar, não teorema

**Visual:** exemplo real de 1 query Base64 do `encoded_attacks.csv` → "decoded = harmful → refused" em 3 caixinhas. (Capturar uma linha do CSV de `produto/dados/`.)

---

## Slide 6 — Ataques automáticos: PAIR + nanoGCG / Automated Attacks (1:00)

**Título:** *Ataques automáticos: pipeline validado, defesa não testada | Automated Attacks: Pipeline Validated, Defense Untested*

**Fala (bullets):**
- **PAIR** (atacante Qwen3.5-9B → alvo Llama-2-7B-chat): ASR **10,0% (1/50 streams, IC 95% Wilson 1,8–40,4)** — sem defesa; comportamento 5G/COVID score 10; 4 comportamentos bateram score 9 sem sucesso
- **nanoGCG** (MiniCPM5-2B, avaliação humana): obediência completa **0/11**; parciais **caíram de 3/11 (sem sufixo) para 1/11 (com sufixo)**; recusas subiram de 8 para 10
- Leitura do nanoGCG: modelo com `<think>` inspecionou o sufixo adversarial e **recusou mais com o ataque do que sem** — raciocínio explícito detecta artefato
- Limitação assumida: PAIR **não rodou com SR/IA** (PAIR-lite em andamento) → lacuna exata que a literatura aponta como mais perigosa (ataque adaptativo vs. defesa estática)

**Visual:** **Tabelas 3 e 4 do relatório v0** lado a lado; no nanoGCG, destaque na mudança 3→1 (parciais). Fonte: `produto/dados/pair_asr_tables.txt`, `produto/dados/Aula_4_-_IA_Adversarial_resultados.txt`.

---

## Slide 7 — Trojan em hardware: extensão do ano / Hardware Trojan Extension (0:45)

**Título:** *Do prompt ao silício: dataset de trojans em AES | From Prompt to Silicon: AES Hardware-Trojan Dataset*

**Fala (bullets):**
- Mesmo tema (confiança em sistemas gerados por IA), outro domínio: golden model AES RISC-V (secworks, MIT)
- Dataset **20/20** amostras geradas e validadas: **10 legítimas + 10 trojans** via LLM, todas aprovadas em verificação iverilog
- Diversidade de payloads: 1-bit flip na S-box, estado auto-lacado na FSM, vazamento de metade da chave mestra (`key_dbg`), supressão de handshake
- Planilha anônima embaralhada (A01–A20) + gabarito separado — protocolo de detecção cega equivalente ao de troca entre grupos
- Ponte com o artigo: IA gera e IA ajuda a auditar — detecção exige inspeção semântica, igual ao juiz dos jailbreaks

**Visual:** captura da `trojans/resultados/planilha_anonima.csv` (colunas embaralhadas) + 1 diff real de trojan (ex.: TRJ-04, S-box 0x7c→0x7d, 1 linha). Fonte: `trojans/resultados/`, `trojans/resultados_gen.log`.

---

## Slide 8 — Conclusão e próximos passos / Conclusion & Next Steps (0:50 | compacta 0:40)

**Título:** *Conclusões | Conclusions*

**Fala (bullets):**
- SR e IA **anulam/reduzem jailbreaks manuais** num 7B aberto (12%→0% / →2%); recomendação da literatura se confirma: **combinar contramedidas**, não eleger uma
- Base64 é ineficaz contra alvos treinados em código
- Pipeline de ataque automático validado (PAIR 10%, nanoGCG 0/11 obediências); próximo passo decisivo: **PAIR/nanoGCG × SR/IA**
- Juiz único tem viés de falso negativo → plano: juiz duplo (Mistral + Llama-3) + **calibração humana com kappa de Cohen** (protocolo pronto, semente 42)
- Frase final: "Zero ASR today is not immunity tomorrow — the real test is the adaptive attacker."

**Visual:** 3 bullets-âncora + mini-tabela "limitações" (n pequeno, juiz não calibrado, alvos distintos entre tabelas — ASRs não estritamente comparáveis). Encerrar com QR/código do repositório `leokawakami/portfolio-pcs5917`.

---

**Tempos:** 0:20 + 0:45 + 0:50 + 1:00 + 0:45 + 1:00 + 0:45 + 0:50 = **6:15** (+transições ≈ 6:30).
**Modo 5 min:** slide 5 vira fala do slide 4 (−0:45), slides 2 e 7 na versão compacta (−0:40) → ≈ 5:05.

---

## Roteiro de figuras (o que puxar de onde)

| Slide | Elemento visual | Arquivo-fonte |
|---|---|---|
| 2 | Diagrama ataque→defesa→juiz | desenhar a partir de `produto/01-estudo-defesas.md` |
| 3 | Tabela ataque × alvo × n | seção 2 de `produto/relatorio-defesas-v0.md` |
| 4 | **Tabela 1** (ASR família×defesa) + barras da Tabela 2 | `produto/relatorio-defesas-v0.md` §3; dados: `produto/dados/aula7_asr_tables.txt` |
| 5 | Exemplo Base64 real → recusa | `encoded_attacks.csv` via `produto/dados/` |
| 6 | **Tabelas 3 e 4** lado a lado | `produto/dados/pair_asr_tables.txt`, `produto/dados/Aula_4_-_IA_Adversarial_resultados.txt` |
| 7 | Planilha anônima + diff do TRJ-04 | `trojans/resultados/planilha_anonima.csv`, `trojans/trojans/TRJ-04/` |
| 8 | Bullets + limitações + QR do repo | `produto/relatorio-defesas-v0.md` §5 |

Regra de comparabilidade (dizer em voz alta no slide 6 ou 8): Tabelas 1–2 usam juiz Mistral-7B; Tabela 3 usa o juiz vendorizado do PAIR; Tabela 4 é humana — **ASRs não são estritamente comparáveis entre tabelas**.

---

## Dicas para bonificação em inglês

### A. Pronúncia de termos técnicos (aproximação PT-friendly)

| Termo | Pronúncia aprox. | Cuidado |
|---|---|---|
| jailbreak | ˈdʒeɪl-brek ("djêil-brék") | "j" de *jeans*, não "dj" de *dia* |
| large language model (LLM) | leitura letra a letra: "ɛl-ɛl-ɛm" | nunca "lham-lam" |
| inference | ˈɪn-fə-rəns ("ÍN-fa-râns") | acento na 1ª sílaba |
| weight (peso do modelo) | wéit | não confundir com "wait" |
| alignment | ə-ˈlaɪn-mənt | |
| self-reminder | sɛlf-rɪ-ˈmaɪn-dər | acento em MAI |
| intention analysis | ɪn-ˈtɛn-ʃən | "tention" com "ten" de *ten* (10) |
| attack success rate (ASR) | ə-ˈtæk | "success" = kə-SÊSS |
| judge / judge model | dʒʌdʒ ("dâdj") | som de "j" longo |
| refusal | rɪ-ˈfjuː-zəl | |
| obfuscation | ˌɒb-fʌs-ˈkeɪ-ʃən | acento em KEI |
| Base64 | "beis-siksti-fɔːr" | ler "64" sempre |
| fine-tuning | fain-ˈtjuːn-ing | |
| quantization / NF4 | kwɒn-tə-ˈaɪ-zeɪ-ʃən; "ɛn-ɛf-fɔːr" | |
| Cohen's kappa | ˈkoʊ-ənz ˈkæ-pə | Cohen = "KÔ-enz", kappa = "KÁ-pa" (2 plosivos) |
| confidence interval | ˈkɒn-fɪ-dəns | |
| suffix / adversarial suffix | ˈsʌf-ɪks; æd-və-ˈsɛə-ri-əl | acento em SEÊ |
| handshake (protocolo) | ˈhænd-ʃeɪk | |
| circuit / silicon | ˈsɜː-kɪt / ˈsɪ-lɪ-kən | |
| pipeline | ˈpaɪp-laɪn | |
| baseline | ˈbeɪs-laɪn | |
| Cohen/Landis-Koch (citações) | "kô-enz", "læn-dɪs-kɔx" | sobrenomes: falar devagar |

Dica geral: em apresentações técnicas, **ralentizar em números e nomes próprios** vale mais que sotaque perfeito. "twelve point zero percent" > velocidade.

### B. Frases de transição prontas (decorar uma por slide)

1. **Abrir (slide 1→2):** "Let me start with the motivation behind this work."
2. **Motivação→método:** "So, how did we actually measure this?" / "With that in mind, let me describe the methodology."
3. **Método→resultado:** "That brings us to our headline result." / "Here is what we found."
4. **Resultado→análise:** "Zero sounds like immunity — but let's be careful about what this number means."
5. **Slide 4→5 (surpresa):** "There is one result that surprised us." / "One finding deserves its own slide."
6. **Manual→automático:** "Manual prompts are only half the story. What happens when the attack is automatic?"
7. **PAIR→nanoGCG:** "Let me now turn to a second automatic attack, with a very different behavior."
8. **LLM→trojan (slide 7):** "The same theme — trust in AI-generated artifacts — also appears closer to the silicon."
9. **Resultados→limitações:** "Before concluding, let me be honest about what these numbers do not show."
10. **Limitações→conclusão:** "Taking all of this into account, three takeaways."
11. **Encerrar:** "To sum up: prompt-level defenses work against static attacks, but the adaptive attacker is the real test. Thank you — I'm happy to take questions."

### C. Respostas prontas para Q&A provável

- **"Why only one judge model?"** → "Good question. A single LLM judge has a false-negative bias. Our plan is a second judge, Llama-3, with intersection voting, plus human calibration with Cohen's kappa — the protocol is ready."
- **"Isn't n=50 too small?"** → "Yes, and we state it. With fifty queries, one extra success moves the ASR by two points, so the gap between two percent and zero is within sampling noise."
- **"Did you test defenses against PAIR?"** → "Not yet — that's exactly our next step, PAIR-lite with isolated defenses. Static defenses may not survive an adaptive rewrite loop."
- **"Are the tables comparable?"** → "Not strictly. Tables one and two use the Mistral judge, table three uses the PAIR judge, and table four is human-rated. We flag that limitation in the paper."

### D. Checklist final antes de gravar/apresentar

- [ ] Ensaiar cronometrado 2×: uma vez modo 6:30, uma vez modo 5:05
- [ ] Números-chave na cabeça (ordem decoreba): **12 / 2 / 0 — 0 — 10 com IC 1.8 to 40.4 — 3 out of 11 down to 1 out of 11 — 20 out of 20**
- [ ] Nunca dizer "the model is safe" → dizer "we observed zero successes in this setting"
- [ ] Slides com no máximo 6 linhas; tabela do slide 4 é o único slide denso
- [ ] Se a bonificação exigir entrega em EN, título do slide 1 já nasce bilíngue (formato acima)
