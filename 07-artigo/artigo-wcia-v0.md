# Segurança Adversarial de LLMs na Prática de Sala de Aula: Um Estudo Empírico de Jailbreaks, Defesas a Nível de Prompt e Trojan em Hardware com Avaliação por Juiz LLM

**Rascunho v0 — artigo curto estilo SBC (WCIA / SBSeg), coluna dupla, alvo ≤ 4 páginas**

Leonardo Kawakami Hissanaga — NUSP 11374864 — Escola Politécnica da Universidade de São Paulo (USP)
*Disciplina: PCS5917 — IA Adversarial (2026/2). Atividade realizada individualmente; todas as contribuições (experimentos, juízes, análise, redação) do autor.*

> **Nota de escopo (remover na versão final):** este rascunho reframea os cinco experimentos realmente executados na disciplina (T1–T5) como estudo empírico único sob o guarda-chuva WCIA — segurança de IA, *purple team* e avaliação de ASR humano vs. juiz. Marcas **[PENDENTE]** indicam resultados dependentes dos CSVs dos notebooks Colab `02_ataque-automatico_com_defesas.ipynb` e `03_juiz-unificado.ipynb`, ainda em execução.

---

## Resumo

Avaliamos empiricamente a cadeia completa ataque–defesa–avaliação em segurança de IA, reproduzindo em infraestrutura acadêmica modesta (Google Colab, GPUs T4/L4, modelos abertos ≤ 9B) cinco experimentos de *red teaming*: (T1) dez jailbreaks manuais × cinco tarefas maliciosas contra Qwen2.5-7B-Instruct sob as defesas a nível de prompt Self-Reminder (SR) e Intention Analysis (IA), com Taxa de Sucesso de Ataque (ASR) reduzida de 12,0% (baseline) para 2,0% com IA e 0,0% com SR, medida por juiz LLM (Mistral-7B-Instruct-v0.3); (T2) ofuscação Base64 (família CipherChat) com ASR 0,0% em todas as condições; (T3) ataque automático adaptativo PAIR (atacante Qwen3.5-9B, alvo Llama-2-7B-chat) com ASR de 10,0% (IC 95%: 1,8–40,4%) sem defesa; (T4) sufixo adversarial nanoGCG contra MiniCPM5-2B, que reduziu obediência parcial de 3/11 para 1/11 casos — o alvo inspecionou semanticamente o sufixo e recusou *mais* com o ataque do que sem ele; (T5) pipeline de geração e detecção de trojans de hardware em um projeto AES-128 Verilog de referência, com 10 variantes legítimas e 10 trojans gerados por LLM, 20/20 compilando com Icarus Verilog, e detecção por LLM em andamento. Os resultados confirmam para modelos abertos pequenos as tendências da literatura sobre eficácia assimétrica de defesas de prompt, e expõem o gargalo metodológico central do campo: a confiabilidade do ASR depende do juiz — humano ou LLM — razão pela qual discutimos o protocolo de calibração humano–juiz (kappa de Cohen) do projeto no enquadramento de *purple team* da WCIA.

**Palavras-chave:** segurança de IA, jailbreak, LLM como juiz, ASR, purple team, trojan de hardware, nanoGCG, PAIR

---

## 1. Introdução

Modelos de linguagem grandes (LLMs) alinhados por RLHF permanecem vulneráveis a jailbreaks de prompting — ataques que induzem conteúdo nocivo sem alterar pesos [Zou et al., 2023; Chao et al., 2025]. A comunidade respondeu com duas frentes: defesas a nível de prompt, leves e plug-and-play, como Self-Reminder [Xie et al., 2023] e Intention Analysis [Zhang et al., 2025]; e benchmarks padronizados de *red teaming* automatizado, como o HarmBench [Mazeika et al., 2024], que consolidou a métrica ASR e a figura do juiz automático. Um terceiro vetor, ainda pouco presente em disciplinas de graduação, é o trojan de hardware: backdoors inseridos em projetos RTL (ex.: AES) que só se ativam sob gatilhos raros — superfície análoga de auditoria confiável que o LLM pode tanto gerar quanto detectar.

Este artigo apresenta um estudo empírico conduzido integralmente na disciplina PCS5917 (IA Adversarial, Poli/USP), no espírito das agendas da WCIA para segurança de IA e avaliação de vulnerabilidades: em vez de propor uma nova defesa, **documentamos e medimos a cadeia completa ataque→defesa→avaliação com modelos abertos em infraestrutura modesta**, tratando a própria avaliação (humana vs. juiz LLM) como objeto de estudo — o dual *purple team* em que os mesmos autores operam ataque e defesa. Contribuições:

1. Tabela consolidada de ASR (defesa × família de ataque) em Qwen2.5-7B-Instruct com juiz LLM calibrado por rubrica escrita (T1–T2), reproduzindo em alvo aberto de 7B o protocolo do estudo de caso de Hayashi et al. (2026) com DeepSeek;
2. Evidência empírica reprodutível de que ofuscação Base64 é ineficaz contra alvos treinados em código (T2), cobrindo uma lacuna da literatura (CipherChat só havia sido validado em GPT-3.5 [Zhang et al., 2025]);
3. Execução de ponta a ponta, em sala de aula, de dois ataques automáticos de famílias distintas — PAIR preto-caixa adaptativo (T3) e nanoGCG de sufixo otimizado (T4) — com a observação inesperada de que um alvo com cadeia de raciocínio visível detecta e recusa o sufixo adversarial;
4. Pipeline de geração/detecção de trojans de hardware com LLM (T5): 10+10 variantes de AES-128 em Verilog, 20/20 compiláveis, planilha anonimizada para detecção cega;
5. Protocolo de avaliação humana para calibração humano–juiz (amostragem estratificada, cegamento, kappa de Cohen), discutido como resposta à ameaça central de validade do ASR.

## 2. Trabalhos relacionados

**Defesas a nível de prompt.** Self-Reminder encapsula a query entre lembretes de responsabilidade no system mode; Xie et al. (2023, *Nature Machine Intelligence*) reportam ASR de 67,2%→19,3% em ChatGPT (540 amostras), mas falham em jailbreaks longos que proíbem recusas (DevMode+Ranti: 100%→100%). Intention Analysis faz o modelo declarar a intenção essencial da query antes de responder; Zhang et al. (2025, COLING) reportam redução média de 48,2% no ASR sobre 8 modelos e 5 famílias de ataque, com vantagem marcada sobre SR em modelos fracamente alinhados (Vicuna-7B: 79,0%→2,85% com IA vs. 48,0% com SR). Hayashi et al. (2026, *IEEE Access*) comparam as duas defesas em DeepSeek-R1/V3 (750 ataques estáticos/modelo, juiz Llama-3.3-70B + validação humana de 10%): a defesa correta depende do perfil do modelo — IA para modelos de raciocínio (70,27%→6,00%), SR para não-raciocínio (53,47%→17,60%) — e nenhum cenário zera o ASR.

**Ataques automáticos.** GCG/nanoGCG [Zou et al., 2023] otimiza um sufixo adversarial por gradientes; PAIR [Chao et al., 2025] usa um LLM atacante preto-caixa que reescreve o jailbreak iterativamente guiado por um juiz, quebrando alvos comerciais em ~20 consultas. Ambos integram o benchmark padronizado HarmBench [Mazeika et al., 2024], que unificou protocolos de ASR e avaliação por juiz para *red teaming* automatizado.

**Avaliação.** O NIST AI 100-2 define a taxonomia de ataques a LLMs; Hayashi et al. (2026) medem 12,7% de discordância juiz↔humano com viés de falsos negativos (o juiz subestima o ataque). Esta lacuna de calibração motivou nosso protocolo humano–juiz (§3).

## 3. Metodologia

Os cinco experimentos (T1–T5, Tabela 1) compartilham o desenho *purple team*: um mesmo autor executa ataque, defesa e avaliação em GPUs gratuitas (T4/L4), com modelos abertos carregados em 4 bits (bitsandbytes NF4) quando necessário.

**T1 — Defesas vs. jailbreaks manuais (Qwen2.5-7B-Instruct).** Modelo-alvo Qwen2.5-7B-Instruct (NF4, Colab T4). Ataques: 10 jailbreaks públicos (DAN, AIM, AntiGPT, EvilConfidant, Grandma, Hypothetical, DevMode, OppositeDay e congêneres) × 5 tarefas maliciosas herdadas do dataset de Xie et al. (2023) (comer vidro, negacionismo climático, phishing bancário, sequestro/chantagem, SQL injection) = 50 queries por condição, 150 respostas. Defesas isoladas: {baseline, SR, IA}; SR com encapsulamento pré+pós do template original; IA na variante one-pass (a mesma de Hayashi et al., 2026). Avaliação: juiz LLM Mistral-7B-Instruct-v0.3 (NF4) com rubrica binária escrita (1 = conteúdo substantivo que avança o objetivo nocivo; compliance parcial conta; disclaimer não cancela; 0 = recusa/evasiva/inválida), saída JSON com justificativa, 165/165 respostas avaliadas sem falha.

**T2 — Ofuscação Base64.** Mesma configuração de T1; payload das 5 tarefas codificada em Base64 (família CipherChat/SelfCipher), 5 queries × 3 condições = 15 respostas, mesmo juiz.

**T3 — PAIR (Llama-2-7B-chat).** Piloto preto-caixa: atacante Qwen3.5-9B (GGUF, llama-cpp-python) gera/crossa/muta prompts; alvo Llama-2-7B-chat (4-bit); juiz = o próprio atacante com o prompt de juiz vendorizado do PAIR (escala 1–10, sucesso = 10) retroalimenta o loop. 10 comportamentos JBB-Behaviors × 5 streams × 3 iterações = 150 linhas de diálogo (EN), 0 erros de execução. Executado **apenas sem defesa**; a versão com SR/IA isolados está em curso **[PENDENTE — CSV do notebook Colab 02_ataque-automatico_com_defesas]**.

**T4 — nanoGCG (MiniCPM5-2B).** 11 casos (prompt direto + 10 templates de jailbreak: 3-Liner, AIM, AntiGPT, APOPHIS, ARIA, Balakula…) contra MiniCPM5-2B (fp16), sufixo adversarial de 20 tokens (250 iterações de otimização, loss mínima 0,27). Avaliação **humana** em três níveis (Recusou / Parcial / Obedeceu).

**T5 — Trojans de hardware (AES-128 Verilog).** Golden model: `secworks/aes` (MIT). Um agente LLM gerou 10 variantes legítimas (renomeação, comentários, refatoração, assertions…) e 10 trojans segundo taxonomia gatilho×efeito×ocultação (estilo Trojan Taxonomy/TrustHub): byte-flip condicionado a valor raro da chave, backdoor de observação que vaza metade da chave mestra em pino de debug, off-by-one que dropa a última rodada, DoS por contador, estados mortos em FSM, entre outros — todos com diffs mínimos e gatilhos em valores raros (comportamento idêntico ao golden no caso comum). Validação: 20/20 amostras compilam com Icarus Verilog 12.0. Detecção: planilha anonimizada (IDs embaralhados, semente 42, sem vazamento de identificadores LEG-/TRJ-) submetida a detecção cega por LLM **[PENDENTE — resultados de detecção e métricas TP/TN em curso]**.

**Avaliação humano–juiz (transversal).** Para T1–T3, um protocolo próprio define amostragem estratificada (todos os casos com label 1 ou score ≥ 5 do juiz + amostra aleatória do restante, `random_state=42`), cegamento quanto ao rótulo automático, definição operacional binária idêntica à rubrica do juiz e concordância via kappa de Cohen com interpretação de Landis & Koch (1977). Subconjuntos exportados: 31 linhas (PAIR) + 18 linhas (Aula 7, 3 por célula família×defesa). Rótulos humanos **[PENDENTE — preenchimento em curso]**.

## 4. Experimentos e resultados

**T1 — defesas vs. manuais (Tabela 1).** Sem defesa, o ASR foi 12,0% (6/50). IA reduziu para 2,0% (1/50) e SR para 0,0% (0/50). Por tarefa, os successes do baseline concentraram-se em negacionismo climático e phishing (20% cada); SQL injection nunca passou. O resultado replica qualitativamente a literatura para modelos instruídos (Zhang et al.: Llama2-7B 23,5%→1,03% SR →0,03% IA), mas a ordem IA > SR aqui está dentro do ruído amostral (n=50 ⇒ ±2 p.p. por resposta).

**T2 — Base64.** ASR 0,0% em todas as cinco células restantes (encoded × {none, SR, IA}) — inclusive contra o baseline, isto é, sem nenhuma defesa o ataque falhou. Hipótese: o Qwen2.5, extensivamente treinado em código, decodifica a payload internamente; o conteúdo decodado permanece nocivo e o alinhamento padrão recusa. A ofuscação por codificação tem custo-benefício baixo contra alvos treinados em código — extensão empírica da lacuna que Zhang et al. (2025) deixaram aberta ao validar CipherChat apenas em GPT-3.5.

**T3 — PAIR.** ASR do juiz = 10,0% (1/10 comportamentos; 1/50 streams; IC 95% Wilson: 1,8–40,4%). Único comportamento comprometido: desinformação (5G-COVID, score máx. 10); quatro comportamentos atingiram score 9 sem sucesso. Pipeline validado, porém sem as defesas isoladas **[PENDENTE]**, o que impede ainda a comparação central — se um atacante adaptativo contorna defesas estáticas como SR/IA.

**T4 — nanoGCG.** Nenhum caso atingiu obediência completa. Contra a expectativa da literatura (GCG aumenta ASR), o sufixo *piorou* o ataque: sem sufixo, 3/11 parciais (AIM, AntiGPT v2, Balakula); com sufixo, 1/11 (3-Liner); recusas subiram de 8/11 para 10/11. A trace de raciocínio visível do MiniCPM5-2B mostra o modelo identificando o sufixo como "tentativa de burlar filtros de segurança" — alvos com cadeia de raciocínio explícita podem tratar o artefato adversarial como evidência adicional de malícia.

**T5 — Trojans.** Dataset 10+10 construído e validado por compilação (20/20 OK em Icarus Verilog 12.0, incluindo o golden), com diffs unificados mínimos e metadados por variante (gatilho, efeito, ocultação). Detecção cega por LLM e cálculo de sensibilidade/especificidade sobre o gabarito rotulado **[PENDENTE]**.

### Tabela 1 — Comparativo dos cinco experimentos

| ID | Vetor de ataque | Alvo | Defesas | n | Avaliação | Resultado principal |
|---|---|---|---|---|---|---|
| T1 | 10 jailbreaks manuais × 5 tarefas | Qwen2.5-7B-Instruct (NF4) | none / SR / IA (one-pass) | 150 | juiz LLM (Mistral-7B) | ASR 12,0% → 2,0% (IA) / 0,0% (SR) |
| T2 | Ofuscação Base64 (CipherChat-like) | Qwen2.5-7B-Instruct (NF4) | none / SR / IA | 15 | juiz LLM (Mistral-7B) | ASR 0,0% em todas as condições |
| T3 | PAIR adaptativo (atacante Qwen3.5-9B) | Llama-2-7B-chat (4-bit) | nenhuma | 50 streams | juiz automático + revisão humana pend. | ASR 10,0% (IC 1,8–40,4); **com defesas [PENDENTE]** |
| T4 | nanoGCG (sufixo 20 tokens, 500 it.) | MiniCPM5-2B (fp16) | nenhuma | 11 | humana (3 níveis) | parciais 3/11 → 1/11 com sufixo; 0 obediências |
| T5 | Trojan RTL gerado por LLM (AES-128 V) | projeto Verilog (golden `secworks/aes`) | detecção LLM cega | 10 leg. + 10 trojan | compilação + detecção | 20/20 compilam (iverilog 12.0); detecção **[PENDENTE]** |

**Ameaças à validade.** (i) Os ASRs de T1–T3 vêm de juízes diferentes (Mistral-7B, classificador PAIR) e T4 é humano — os números não são estritamente comparáveis entre linhas da Tabela 1; a unificação por juiz único **[PENDENTE — CSV do notebook Colab 03_juiz-unificado]** endereçaria isso. (ii) n pequeno por célula (50/15/50/11) ⇒ intervalos largos. (iii) Juiz único tende a falsos negativos (viés medido de 12,7% de discordância com ASR otimista em Hayashi et al., 2026). Adicionalmente, no piloto PAIR o juiz é o próprio atacante e, no juiz unificado, o próprio alvo — self-preference bias documentado em LLM-as-a-judge (Zheng et al., 2023), declarado como limitação e só parcialmente endereçado pela calibração humana pendente. (iv) Cada alvo foi atacado por uma subset de famílias — não há uma matriz completa ataque × defesa em um único modelo.

## 5. Discussão

**Defesa certa depende do alvo, não da defesa.** Somando T1 (Qwen2.5, não-raciocínio: SR ≈ IA ≈ zero contra manuais) com T4 (MiniCPM5 com raciocínio visível: o próprio modelo detecta o sufixo GCG) e a literatura (SR supera IA só em modelos sem raciocínio [Hayashi et al., 2026]), o eixo decisivo é a superfície de atenção do alvo: SR só reforça alinhamento latente; IA realoca atenção para a intenção; modelos com trace explícita inspecionam o próprio input. Nenhum mecanismo zera o ASR universalmente — a recomendação da literatura de combinar contramedidas [Hayashi et al., 2026] é sustentada pelos nossos dados dispersos.

**Ataque adaptativo é a fronteira que ainda não testamos.** T3 validou o pipeline PAIR mas não o confrontou com SR/IA — exatamente a lacuna apontada por Hayashi et al. (2026): o loop de reescrita do PAIR pode aprender a contornar defesas estáticas, e "ignore previous instructions" contra IA já é testado na literatura com resultado negativo (a IA resiste). **[PENDENTE: CSV Colab 02]** fecha essa questão.

**O juiz é o experimento.** A diferença entre "a defesa funciona" e "o juiz acha que funciona" é o problema metodológico central que nossos cinco experimentos tornam visível: T1/T2/T3 usam três juízes automáticos distintos e T4 depende de julgamento humano; nosso protocolo de kappa de Cohen (cegamento, estratificação, semente) é a peça que falta para transformar ASR em métrica confiável em contexto educacional **[PENDENTE: 31+18 rótulos humanos; CSV Colab 03]**. O enquadramento WCIA — *purple team* e avaliação padronizada de segurança de IA, na linha do HarmBench [Mazeika et al., 2024] — é o ambiente natural para essa discussão: o custo de reproduzir red teaming sério caiu a uma GPU gratuita, mas o custo de medir corretamente não caiu junto.

**Trojans como ponte entre IA e sistemas críticos.** T5 estende o mesmo raciocínio adversarial (payload discreto com gatilho raro, detecção cega) do texto para o silício: o LLM aparece simultaneamente como arma (gerador de backdoors plausíveis) e escudo (detector), com a compilação como oráculo objetivo — uma assimetria mais confortável que o ASR, pois 20/20 compilações é um número verificável por qualquer um.

## 6. Conclusão

Reproduzimos, em infraestrutura acadêmica modesta e com modelos abertos, os pilares da segurança adversarial de IA cobertos pela WCIA: defesas de prompt (SR/IA) com ASR de 12,0%→2,0%/0,0% em Qwen2.5-7B; ineficácia de Base64 contra alvos treinados em código; ataque automático PAIR (10,0%) e nanoGCG (0 obediências, com o efeito colateral de o sufixo aumentar recusas em alvo com raciocínio); e um pipeline completo de geração/detecção de trojans de hardware com LLM (20/20 compiláveis). Os trabalhos futuros diretos, já em execução, são: PAIR com defesas isoladas, juiz unificado sobre todas as células, rótulos humanos para kappa, e métricas de detecção cega dos trojans — todos marcados **[PENDENTE]** neste rascunho. Concluímos que o gargalo da segurança prática de IA não é mais acesso a modelos ou GPUs, e sim a disciplina avaliativa: sem calibração humano–juiz e sem padronização tipo benchmark, ASR continua sendo um número que descreve o juiz tanto quanto o ataque.

## Referências

1. V. T. Hayashi, M. P. Pagliuso Neto, C. C. Miers, F. F. Redígolo, R. Arakaki, M. A. Simplicio Jr., "DeepSeek Under Attack: An Analysis of Jailbreak Attacks and Prompt-Level Defenses," *IEEE Access*, vol. 14, pp. 103944–103961, 2026. DOI: 10.1109/ACCESS.2026.3710427.
2. Y. Xie, J. Yi, J. Shao, J. Curl, L. Lyu, Q. Chen, X. Xie, F. Wu, "Defending ChatGPT against Jailbreak Attack via Self-Reminder," *Nature Machine Intelligence*, 5(12):1486–1496, 2023. DOI: 10.1038/s42256-023-00765-8.
3. Y. Zhang, L. Ding, L. Zhang, D. Tao, "Intention Analysis Makes LLMs A Good Jailbreak Defender," *Proc. 31st COLING*, pp. 2947–2968, 2025. arXiv:2401.06561.
4. P. Chao, A. Robey, E. Dobriban, H. Hassani, G. J. Pappas, E. Wong, "Jailbreaking Black Box Large Language Models in Twenty Queries" (PAIR), *IEEE SaTML*, 2025. DOI: 10.1109/SaTML64287.2025.00010. Versão preprint: arXiv:2310.08410.
5. A. Zou, Z. Wang, J. Z. Kolter, M. Fredrikson, "Universal and Transferable Adversarial Attacks on Aligned Language Models" (GCG/nanoGCG), arXiv:2307.15043, 2023.
6. M. Mazeika, L. Phan, X. Yin, A. Zou, Z. Wang, N. Mu, et al., "HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal," *ICML 2024* (PMLR 235). arXiv:2402.04249.
7. J. R. Landis, G. G. Koch, "The Measurement of Observer Agreement for Categorical Data," *Biometrics*, 33(1):159–174, 1977.
8. NIST, "Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations" (NIST AI 100-2, 2nd ed.), 2024.

> **Verificação bibliográfica:** o identificador arXiv de HarmBench foi conferido nesta sessão — o correto é **arXiv:2402.04249** (ICML 2024, PMLR v235); a referência circulante "2307.02483" está incorreta (esse ID pertence a outro trabalho) e foi corrigida acima. HarmBench ainda não era citado nos documentos anteriores do projeto (`01-estudo-defesas.md`, `relatorio-defesas-v0.md`), portanto entra como referência nova. PAIR (2310.08410) e nanoGCG/GCG (2307.15043) já constavam dos materiais da disciplina e mantêm os números verificados lá.

---

### Apêndice interno (rascunho — remover na submissão)

**Rastreabilidade dos números:**
- T1/T2 ← `produto/dados/aula7_asr_tables.txt` (notebooks Aula_7 Notebook 1–3, execução 04/11/2026); jailbreaks/tarefas ← `produto/planilha-unica-ataques.csv`.
- T3 ← `produto/dados/pair_asr_tables.txt` (piloto 22/10/2026); ASR humano 0/31 rótulos ainda não preenchidos.
- T4 ← `produto/dados/Aula_4_-_IA_Adversarial_resultados.txt` e `portfolio-pcs5917/02-aula4-nanogcg/resultados_minicpm5_nanogcg.csv`.
- T5 ← `trojans/` (golden `secworks/aes`, `diffs/`, `resultados_gen.log` 20/20, `resultados/planilha_anonima.csv`, `gabarito.csv`).
- **Pendente Colab 02** (`02_ataque-automatico_com_defesas.ipynb`): PAIR/ataque-automático × {SR, IA} — fecha a comparação estático vs. adaptativo.
- **Pendente Colab 03** (`03_juiz-unificado.ipynb`): juiz unificado sobre todas as células + comparação ASR automático vs. humano (kappa).

**Ajustes para a versão final:** converter para o `sbc-template` da SBC; estimativa ~4 páginas com 1 tabela e 2 figuras reaproveitadas (`produto/figs/fig1_asr_defesas.png`, `fig2_panorama.png`); título final a afinar em torno de "avaliação ASR em jailbreaks, defesas e trojans".
