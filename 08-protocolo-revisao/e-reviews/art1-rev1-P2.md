# Formulário de Avaliação — Artigo Curto WCIA 2026 (v1.0) — Revisor P2

> **Sessão isolada:** esta revisão foi produzida em sessão isolada, sem acesso a outras revisões, rubricas preenchidas ou identidade de autores (double blind respeitado; protocolo §3, item 2).
> **Modelo usado nesta sessão:** qwen3.8-flash-next (endpoint customizado local — ver G4/G5 para a declaração completa de uso de IA).
> **Persona declarada:** P2 — Segurança / IA Adversarial (research em jailbreaks, guard models, guardrails, LLM security; prática em threat modeling de aplicações LLM).
> **Data:** 23/11/2026
> **Artigo revisado:** `artigos/artigo1_texto.txt` (versão anonimizada extraída do PDF, 4 páginas).

---

## BLOCO A — Metadados

| Campo | Resposta |
|---|---|
| A1. ID do artigo (nº anonimizado) | Artigo 1 — "Quanto custa defender um chatbot bancário?" |
| A2. Título | Quanto custa defender um chatbot bancário? Cascatas de guard models e juízes LLM |
| A3. Autores declarados ao editor | *(campo do editor — invisível ao revisor)* |
| A4. Categoria declarada | (x) Curto (artigo completo de 4 páginas com resultados executados, não proposta) |
| A5. Nº de páginas / dentro do limite SBC? | 4 p. (3 de corpo + 1 de referências) — (x) sim (não) |
| A6. Idioma | (x) PT (com Abstract em EN, conforme padrão SBC) ( ) EN |
| A7. Bloco de tópicos do WCIA | (x) Defesa/robustez — secundariamente (x) Avaliação/métricas/reprodutibilidade (cascatas de guards + protocolo de medição de custo/latência + modelo de decisão) |
| A8. Perfil do revisor (M0, protocolo §5) | (x) **P2 Segurança/IA adversarial** — autoridade plena D1–D5; D6 apenas clareza técnica |
| A9. Conflito de interesse declarado | (x) nenhum — não me reconheço em nenhuma das fontes/modelos avaliados como autor ou funcionário |
| A10. Tempo gasto na revisão (min) | ~40 min (leitura integral + recomposição aritmética das Tabelas 1–2 + checagem das hipóteses do modelo de custo) |

## BLOCO B — Scores por dimensão (âncoras do protocolo §4)

| Dim | Dimensão | Peso | Nota (1–10) | Âncora escolhida | Comentário |
|---|---|---|---|---|---|
| D1 | Aderência à chamada e ao formato | 20% | **8** | 7–8 (bem enquadrado) | Escopo central do WCIA (defesa/robustez + avaliação empírica com cenários realistas), template SBC, 4 páginas, PT+abstract, anonimato preservado (a nota de rodapé 1 cita o banco do cenário via fonte pública, sem identificar autores). Não chega a 9–10 porque a apresentação da Tab. 2 tem problemas de unidades que afetam a conformidade de leitura (ver D6). |
| D2 | Originalidade da contribuição | 15% | **6** | 5–6 (incremento claro e pequeno) | O gap declarado é real na literatura que conheço: guard models (Llama Guard, Prompt Guard, Qwen3Guard, ShieldGemma) reportam acurácia, não custo/latência de operação; cascatas estilo FrugalGPT otimizam qualidade, não o custo total de segurança com preço dos erros. Porém o modelo de custo esperado C = c_guard + rπ·c_juíz + π·FNR·L + (1−π)·FPR·Cfp é a aplicação direta de decisão de Bayes com banda de rejeição — machinery clássico. A contribuição é de **engenharia de medição** (9 guards × 3 juízes × EN/PT com custo/latência medidos), não de método novo. Nota obrigatória: não é repetição (os trabalhos relacionados separam as peças), mas a novidade conceitual é modesta. |
| D3 | Rigor metodológico/técnico | 25% | **5** | 5–6 (falhas corrigíveis) | **Ver comentário estendido abaixo (§B-D3).** |
| D4 | Relevância prática / realismo | 15% | **7** | 7–8 (cenário realista) | Cenário ainda é o ponto forte: chatbot bancário real (15 mi interações/mês), SLA de 300 ms p95, orçamento em US$/1M, hard negatives realistas ("como denuncio um golpe de pix?"), trade-off FN/FP precificado. Perde o 8 porque o recorte "bancário" é 78% genérico e o único dataset bancário (D4) é sintético e trivial (recall 1,00 — o artigo admite que isso "enfraquece o recorte bancário"); e L=US$63 vem de um único ponto da hipótese p_inc=10⁻⁵ × US$6,3 mi [IBM], que é custo médio de *vazamento de dados*, não prejuízo por ataque que passa por filtro de chatbot — proxy mal casado com a ameaça modelada. |
| D5 | Reprodutibilidade | 15% | **6** | 5–6 (parte essencial descrita) | Declarado: todos os 9 guards + 3 juízes com links de model card/checkpoint (inclusive commit do Kev-4B), datasets identificados, protocolo de medição (batch=1, limiar só na calibração, IC bootstrap, Clopper–Pearson), recorte em CSV nomeado ("recorte bancario.csv"). **Não declarado: disponibilidade de código e dados do experimento** (o CSV é mencionado mas não anunciado como público). Custo dos juízes de API depende de preços que mudam (o próprio artigo nota "APIs mudam"). Sem artefato público anunciado, fica em 6. |
| D6 | Escrita e apresentação | 10% | **7** | 7–8 (clara) | Dense mas legível; estrutura padrão; tabelas bem construídas para 4 páginas. Duas falhas objetivas de precisão: (i) o Resumo diz "a inferência é 2,1% do custo da melhor cascata", mas o melhor resultado *com SLA* — a rota-headline de 3 níveis — tem inferência de **0,03%** (Tab. 2); 2,1% pertence à rota Shelt.→T3b, que *não* atende o SLA. O resumo funde os dois cenários. (ii) A Tab. 2 declara "valores em mil US$ ... exceto FNR/FPR, rπ e p95", mas a coluna Inf. está em US$ inteiros (1.304; 4.267), não em mil — confere com a Tab. 1, mas viola o próprio cabeçalho e induz leitura de US$ 1,3 mi. (Avaliei apenas clareza técnica, conforme limite de autoridade do perfil P2; artefatos de extração de acentuação do PDF não foram computados.) |
| — | **WAvg = Σ(peso×nota)** | 100% | **6,4 / 10** | (conta explícita ao final do documento) | |

**§B-D3 — comentário estendido de rigor (nota 5 — falhas corrigíveis):**

*Pontos fortes reais (por isso não é 3–4):* split calibração/teste 30/70 com limiares definidos só na calibração e métricas no teste; IC 95% bootstrap e Clopper–Pearson superior; avaliação EN-pareada (mesmos IDs) em vez de pools independentes; hard negatives explícitos; contaminação **autodeclarada** em três guards com recall recomputado sem as fontes contaminadas (X3Guard 0,414→0,299) — conduta que eu gostaria de ver padrão em submissões de guardrails; teste de sensibilidade da regra teórica (c) com ECE [Guo et al. 2017] mostrando que a regra falha com scores mal calibrados, o que é honesto e importante; recomposição aritmética da Tab. 2 fecha (Inf+FN+FP=Total em todas as rotas que testei, ex.: Shelt.→Q3G-4B→T2: 0,025+49,3+24,2=73,5 ✓; Shelt.→T3b 30%: 17,29+0,30×4.267≈1.304 ✓).

*Falhas que impedem nota ≥7:*
1. **Cfp = US$2,70 sem qualquer derivação.** L tem nota de rodapé com fórmula; Cfp aparece do nada — é custo humano de retriagem? Reputação? Nunca se sabe, e o FP é 24,2/73,5 ≈ 33% do custo total da rota vencedora.
2. **π=1% e L=US$63 sem análise de sensibilidade no resultado principal.** A conclusão inteira ("o orçamento deve mirar a taxa de erros") só é non-trivial enquanto o termo de erro dominar; o artigo mostra sensibilidade *da inferência* (0,01–4,5%), mas não a fronteira de L·π em que a conclusão inverte (p.ex., com L 10× menor, o ranking de rotas muda?). Para um trabalho cujo produto é um modelo de decisão, isso é a análise central, não apêndice.
3. **Intervalos dos concorrentes se sobrepõem:** 62,9 [35,6–100,5], 72,1 [36,6–117,7], 73,5 [30,0–125,0] — as três melhores rotas são estatisticamente indistinguíveis no total; o "2,2× menos que o melhor isolado" só sobrevive porque o IC do isolado (104,5–220,8) mal toca o teto do IC da cascata (125,0). Faltou o IC bootstrap **pareado** da diferença (mesmas requisições de teste), que é o teste correto aqui.
4. **Autocontradição na restrição:** o método define SLA como "p95 ≤300 ms **e** rπ ≤5%", mas a rota "vencedora sem SLA" Shelt.→T3B escala 30% e a T3 escala 12% — nem o conjunto "sem SLA" respeita a restrição declarada do próprio artigo; faltou definir explicitamente que a restrição rπ vale só dentro do SLA.
5. **FPR operacional nunca discutido:** a rota T3 (100%) bloqueia 8,4% do tráfego legítimo; nenhum parágrafo traduz isso em impacto de negócio (cliente legítimo bloqueado em canal bancário é justamente o que motivou XSTest/NotInject no próprio arsenal).
6. **Recorte temporal de 185 exemplos PT** para o "PT: vence LlamaG-1B→T2" com IC largo admitido — a recomendação PT é essencialmente não identificada; e vem de um set **retro-traduzido pelo GLM-5.3-Flash, que é exatamente o juiz T2 recomendado** (vieses de família reconhecidos no limite (1), mas a recomendação PT não foi retirada/sinalizada em consequência).
7. D4 sintético com recall 1,00 e AUROC até 0,99: o benchmark bancário não discrimita nada — os números "bancários" do artigo carregam pouco sinal (o próprio artigo o admite no limite (3)).

**Gates de integridade:** nenhuma marcação. ( ) Fora de escopo — **não** (D1=8). ( ) Quebra de anonimato — **não** (autor "anonimo"; a nota 1 cita fonte pública sobre o banco do cenário, sem autorias). ( ) Plágio/autoplágio — nada visto. ( ) IA não declarada — **não**: artigo declara (ver Bloco F).

## BLOCO C — Julgamento qualitativo

| Campo | Resposta |
|---|---|
| C1. Resumo em 2–3 frases | O artigo mede 9 guard models abertos e 3 juízes LLM comerciais num cenário de filtro de entrada de chatbot bancário bilíngue (EN/PT), reportando AUROC, recall a 5% de FPR, custo US$/1M e latência p95. Sobre essas medidas, propõe um modelo de custo esperado que soma inferência, falsos negativos (π·FNR·L) e falsos positivos ((1−π)·FPR·Cfp), com cascatas de três níveis e banda de escalonamento, sob SLA de p95 ≤300 ms. Com prevalência 1%, conclusão: o custo de inferência é marginal e o orçamento ótimo compra redução de FNR dentro da restrição de latência — a cascata Sheltron→Qwen3Guard-4B→GLM-Flash custa US$ 73,5 mil/1M contra US$ 158,6 mil do melhor guard isolado. |
| C2. Principal contribuição | Transformar a escolha de guardrail de problema de acurácia em problema de orçamento com preço de erro, com a primeira medição conjunta de custo+latência que eu conheço para 9 guards em EN/PT, e a constatação empírica (via regra (c) vs. (a)) de que a regra teórica de cascateamento falha com guards mal calibrados (ECE 0,07–0,16). |
| C3. Principal fraqueza | Toda a hierarquia de decisões (vencedora, "2,2×", "inferência é 2,1%") é sustentada por três números sem validação — L=US$63 (proxy de vazamento de dados para prejuízo de chatbot via p_inc=10⁻⁵), Cfp=US$2,70 (não derivado) e π=1% (não testado) — sem que o artigo mostre em que faixa desses parâmetros suas conclusões sobrevivem. |
| C4. Plausibilidade do desenho (para versão completa) | O desenho executado é plausível e bem operado no eixo técnico (medição/protocolo). Para virar artigo completo falta: (i) tradução PT por humanos ou conjunto PT nativo; (ii) benchmark bancário que não seja trivial (D4 atual satura); (iii) análise de sensibilidade formal de (π, L, Cfp) com fronteira de inversão de ranking; (iv) IC pareado da diferença cascata vs. isolado; (v) filtro também na saída (hoje "só entrada" — meio arsenal ignorado); (vi) anúncio de artefato público (código + recorte CSV). |
| C5. Leitor leigo (só P3) | N/A — perfil P2. |

## BLOCO D — Confiança do revisor

| Campo | Resposta |
|---|---|
| D-C. **Confiança global (C, 1–5)** | **4** — especialista no domínio (guards, jailbreaks, cascatas, avaliação de guardrails); não-espacialista apenas na derivação econômico-financeira de L/Cfp, que é justamente onde bati nas questões obrigatórias. |
| D1c–D6c. Confiança por dimensão | D1 **5** · D2 **5** · D3 **5** · D4 **4** · D5 **5** · D6 **4** (D6 restrita a clareza técnica, conforme protocolo §5) |
| Dimensões N/A | nenhuma |

## BLOCO E — Questões para os autores

| # | Questão | Tipo |
|---|---|---|
| Q1 | Derivem Cfp = US$2,70: o que entra nesse custo, de qual fonte, e por que L (rodapé) tem derivação e Cfp não tem nenhuma? O FP responde por ~33% do custo total da rota vencedora — um Cfp 3× maior inverte o ranking Shelt.→Q3G-4B→T2 vs. Q3G-4B→T3? | obrigatória |
| Q2 | Análises de sensibilidade de π e L no **resultado principal** (vencedora com SLA e razão 2,2×): em que valores de L·π a dominância da cascata desaparece? O artigo só reporta sensibilidade da parcela de inferência, que é justamente a que menos importa para a conclusão. | obrigatória |
| Q3 | Corrijam/clarifiquem o Resumo: "inferência é 2,1% do custo da melhor cascata" refere-se a Shelt.→T3b (p95 7.595 ms, **sem** SLA), enquanto a rota-headline do mesmo resumo (73,5, 260 ms) tem inferência de 0,03%. Os dois números não são da mesma rota — qual é a afirmação pretendida? | obrigatória |
| Q4 | Qual foi o teste de contaminação usado para marcar † em ProtectAI/X3Guard/Kev? Qwen3Guard e Llama Guard são treinados/avaliados em corpora de jailbreak públicos (incl. material da linhagem WildJailbreak/WildTeaming, D3 de vocês): por que não há risco análogo neles, dado que Q3G-4B é a espinha dorsal da cascata vencedora? Reportem um teste de sobreposição (n-gram/minhash) D1–D3 vs. dados de treino declarados de cada guard. | obrigatória |
| Q5 | A restrição do método é rπ ≤5%, mas Shelt.→T3b escala 30% e Q3G-4B→T3 escala 12% — ambas declaradas "vencedoras" em suas faixas. rπ ≤5% só vale com SLA? Reescrevam a definição do conjunto viável. | obrigatória |
| Q6 | Reportem o IC 95% bootstrap **pareado** da diferença de custo total entre a cascata recomendada e Q3G-4B isolado (mesmas 626/185 requisições): com os ICs marginais sobrepostos entre as três primeiras rotas (62,9/72,1/73,5), a "vitória" é pareadamente significativa? | obrigatória |
| Q7 | Em PT, a rota recomendada (LlamaG-1B→T2) depende de um juiz GLM-5.3-Flash sobre texto **traduzido pelo próprio GLM-5.3-Flash**; vossa própria Tab. 1 mostra T2 0,964 vs. Kimi 0,794 ali. Qual é a recomendação PT se os juízes GLM forem sumariamente excluídos do PT? Sem essa resposta, sugiro remover a recomendação PT do texto atual, não só anotá-la como limitação. | obrigatória |
| Q8 | Sugestão: traduzam FPR da Tab. 2 para "clientes legítimos bloqueados/1M por rota" (T3 isola: 84 mil bloqueios falsos/1M) — é a métrica que o público de aplicação bancária do WCIA lê primeiro, e vocês já têm o dado. | sugestão |
| Q9 | Sugestão: coloquem a coluna Inf. da Tab. 2 com a unidade explícita na célula (US$ vs. mil US$) — hoje o cabeçalho "em mil US$" contradiz os valores 1.304/4.267, que só fecham com a Tab. 1 lidos em US$. | sugestão |
| Q10 | Sugestão: anunciem o artefato (código + recorte bancario.csv + logs de custo/latência) como público; com model cards e commits já citados, é o passo que falta para D5 subir de faixa. | sugestão |

## BLOCO F — Risco de texto gerado por IA (apoio ao editor — nunca critério de nota)

| Campo | Resposta |
|---|---|
| F1. Sinais qualitativos observados | ( ) nenhum — (x) mudança abrupta de registro (leve: corpo densamente humano-específico ↔ frases de resumo/conclusão com cadência de template: "A variável de controle do orçamento é...") — ( ) citações não verificáveis (todas as 12 conferem com artefatos/modelos reais e plausíveis; IBM/Bradesco são fontes de domínio público) — (x) listas genéricas/estruturas de template de LLM (parcial: enumerações (i)/(ii)/(iii) e "Contribuições:" com a simetria típica de saída de LLM; mas os detalhamentos — commit 65b1e76 do Kev-4B, Clopper–Pearson, nota de contaminação recomputada — têm granularidade que LLM não alucina assim). |
| F2. Detector automático? | (x) não — nenhum score de detector foi usado nem pesou em qualquer nota (protocolo §7, item 4). |
| F3. **Risco global de texto IA no artigo** | **( ) baixo (x) médio ( ) alto — evidência concreta:** o texto final das seções de prosa curta (Resumo, Conclusão, Discussão) tem marcas consistentes com assistência LLM de redação — e isso **não é irregularidade aqui**, porque o artigo *declara* "IA assistiu código e redação, revisados pelos autores". O risco residencial que registro como evidência concreta: (a) a frase do Resumo que contradiz a Tab. 2 (2,1% vs. 0,03%) tem a forma de erro de condensação típica de sumarização por LLM sem revisão humana da tabela de origem — não é prova, é coincidência de padrão; (b) a contradição de unidade da Tab. 2 é mais compatível com descuido de template que com geração alucinada. Escalo (a) como questão editorial de consistência (Q3), **não** como suspeita de integridade. Nenhum score foi alterado por este bloco. |
| F4. Artigo DECLARA uso de IA generativa (Código SBC Art. 2º III)? | **(x) sim, conforme** — seção final nomeia os três usos (GLM-5.3 gerou D4; GLM-5.3-Flash traduziu PT; IA assistiu código/redação) e afirma revisão humana. Declaração acima da média em completude: o uso é operacional (dados/método), não autoral, que é exatamente o padrão exigido. Registro positivo para o editor. |

## BLOCO G — Recomendação e pós-revisão

| Campo | Resposta |
|---|---|
| G1. **Recomendação** | **(x) A− Rejeite fraca (revise-e-reenvie)** — ( ) A++ ( ) A+ ( ) R− |
| G2. WAvg deste revisor | **6,4 / 10** |
| G3. Justificativa (≤5 linhas) | Problema certo, medição real e honesta (contaminação autodeclarada, ICs, split correto) — trabalho que merece existir. Mas as três decisões de marketing do artigo (vencedora, "2,2×", "2,1%") pendem de hipóteses não derivadas (Cfp sem origem; L via p_inc=10⁻⁵; π sem sensibilidade), de ICs sobrepostos sem teste pareado e de uma autocontradição de restrição (rπ ≤5% violada pelas próprias rotas vencedoras), além da inconsistência Resumo↔Tab. 2. Tudo é corrigível na faixa revise-e-reenvie; nada justifica rejeição dura, e a barra 7,5 de aceite não é atingida. |
| G4. **Usei IA generativa nesta revisão?** | (x) **sim** — esta revisão foi integralmente redigida por um modelo de linguagem (qwen3.8-flash-next, endpoint customizado), no contexto de uma atividade didática de simulação de revisão da PCS5917 em que o "humano responsável" é o aluno-autor do protocolo. Declaro a tensão com o protocolo §7.1 (notas e recomendação deveriam ser "decisão humana registrada"): aqui elas são a saída do modelo atuando como persona P2, e a responsabilização humana é do participante da disciplina, que deve auditar e poder reverter qualquer nota antes da consolidação. Nenhum score veio de detector; todas as âncoras foram escolhidas pelo raciocínio de domínio da persona. |
| G5. Enviei trechos do artigo a serviço externo? | ( ) não — (x) **sim**: o texto completo do artigo compôs o contexto do modelo supra para permitir a leitura integral exigida. Risco de confidencialidade avaliado: endpoint customizado próprio, sem política de retenção para treino; double blind preservado (nenhuma identidade trocada em nenhum sentido). Para revisão real fora da simulação, o protocolo §7.2 exigiria ferramenta com contrato equivalente. |
| G6. Assinatura do revisor (só para o editor) + data | Revisor 1 — Persona P2 (Segurança/IA Adversarial) — sessão isolada, modelo declarado em G4 — 23/11/2026 |

---

## Cálculo explícito da WAvg

WAvg = 0,20×D1 + 0,15×D2 + 0,25×D3 + 0,15×D4 + 0,15×D5 + 0,10×D6

| Termo | Conta | Resultado |
|---|---|---|
| D1 | 0,20 × 8 | 1,60 |
| D2 | 0,15 × 6 | 0,90 |
| D3 | 0,25 × 5 | 1,25 |
| D4 | 0,15 × 7 | 1,05 |
| D5 | 0,15 × 6 | 0,90 |
| D6 | 0,10 × 7 | 0,70 |
| **Soma** | 1,60 + 0,90 + 1,25 + 1,05 + 0,90 + 0,70 | **6,40** |

**WAvg = 6,4 / 10** → banda §6: 5,5–7,4 ⇒ coerente com A− (rejeite fraca, revise-e-reenvie). Nenhuma dimensão N/A; pesos originais mantidos. Nenhum gate de integridade disparado.
