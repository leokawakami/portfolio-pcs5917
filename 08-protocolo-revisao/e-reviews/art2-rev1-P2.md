# Formulário de Avaliação — Artigo Curto WCIA 2026 (v1.0)

> **SESSÃO ISOLADA** — revisão 1 deste artigo, elaborada sem acesso a qualquer outra revisão ou rubrica preenchida (protocolo §3, passo 2).
> **Modelo usado nesta simulação:** qwen3.8-flash-next-iq3_s (provedor custom, Hermes Agent), operando em sessão isolada de subagente.
> **Persona:** P2 — Segurança / IA Adversarial (revisora simulada; notas e recomendação registradas conforme protocolo §7.1).
> **Data/hora do registro:** 23/11/2026.

**Nota de escopo para o editor (transparência):** a ordem de serviço mencionou "Prompt Stealing / Two-Step Hot-Wire" e alvos "Bing Copilot/Bard/PoET". Nenhum desses nomes aparece no texto sob revisão. O artigo real é **HOUYI** (arXiv:2306.05499v3): o análogo do "prompt stealing" é o cenário **PROMPT LEAKING** (furto do prompt da aplicação), o "two-step" corresponde ao par *Separator + Disruptor* (separação de contexto + payload), e a avaliação incide sobre **36 aplicações comerciais agregadas do catálogo SUPERTOOLS** (Notion, Writesonic, Parea e 33 anonimizadas), não Bing Copilot/Bard. A presente revisão avalia o texto efetivamente submetido, registrando essa divergência para evitar erro de adjudicação.

---

## BLOCO A — Metadados

| Campo | Resposta |
|---|---|
| A1. ID do artigo (nº anonimizado) | ART2 (arXiv:2306.05499v3, versão completa fornecida ao editor) |
| A2. Título | Prompt Injection attack against LLM-integrated Applications (método "HOUYI") |
| A3. Autores declarados ao editor (invisível ao revisor — double blind) | *(campo do editor)* |
| A4. Categoria declarada | (x) Curto — **mas o texto submetido é a versão arXiv completa, incompatível com a categoria** |
| A5. Nº de páginas / dentro do limite SBC? | 14 p. de corpo + 4 p. de referências/apêndice (18 p. totais) — ( ) sim (**x**) não — limite é 4 p. SBC (3 corpo + 1 refs) |
| A6. Idioma | ( ) PT (**x**) EN |
| A7. Bloco de tópicos do WCIA em que se enquadra | (**x**) Ataques — secundariamente Avaliação/métricas/reprod. e Privacidade |
| A8. Perfil do revisor (M0 do protocolo §5) | ( ) P1 (**x**) P2 Segurança/IA adversarial ( ) P3 |
| A9. Conflito de interesse declarado | (x) nenhum |
| A10. Tempo gasto na revisão (min) | ~50 min |

## BLOCO B — Scores por dimensão (âncoras do protocolo §4)

| Dim | Dimensão | Peso | Nota (1–10) | Âncora escolhida | Comentário obrigatório p/ nota ≤4 ou ≥9 |
|---|---|---|---|---|---|
| D1 | Aderência à chamada e ao formato | 20% | **4** | 3–4 (formatação irregular) | **O artigo excede frontalmente o limite da categoria:** 18 páginas (14 de corpo) contra 4 páginas SBC (3+1). Não é "desvio leve" (banda 5–6). O conteúdo *núcleo* (pilot study de 10 apps → payload em 3 componentes → 36 apps/31 vulneráveis → 2 casos) é tecnicamente condensável, mas as tabelas 1/4/5 e a seção de defesas (§7.1) ocupariam o corpo inteiro; em 4 páginas restaria um paper de claims sem a evidência tabular que sustenta o ASR de 86,1%. A conformidade depende de reescrita estrutural, não de cortes cosméticos — e o resultado líquido em 4 p. seria um artigo substancialmente pior do que o material submetido. Idioma EN e escopo ("Ataques") OK; anonimato: a versão arXiv nominal (7 instituições) — presume-se versão anonímizada na submissão real, registrado como ressalva, sem disparo de gate. |
| D2 | Originalidade da contribuição | 15% | **4** | 3–4 (variação menor) | O inventário de táticas é conhecido: *escape characters*, "ignore previous instructions" e prompt leaking vêm de Perez & Ribeiro [44], Willison [4] e NCC Group [16]; *language switching* já circulava na comunidade de jailbreak ([33], dos próprios autores). A contribuição real é (i) empacotar isso numa gramática de 3 componentes (Framework/Separator/Disruptor) com analogia a SQLi/XSS e (ii) o loop automatizado inferência→geração→feedback. Útil como taxonomia operacional, mas não há formalização de vantagem sobre o estado da arte: qualquer reuso de "separator" nada mais é que um payload de contexto-enriquecido, e o cenário de *indirect injection* já fora coberto por Greshake et al. [20]. Novidade de direção/métrica: nenhuma. |
| D3 | Rigor metodológico/técnico | 25% | **4** | 3–4 (falhas graves) | Quatro falhas graves, todas corrigíveis mas estruturais: **(1) Critério de sucesso inconsistente com o próprio pilot:** na §3.2 os autores descartam como "weak indication" o chatbot responder Q2 ("capital dos EUA") porque responder é a função esperada do app — e na Tabela 4 contam CODE GENERATION (quicksort) como exploração bem-sucedida exatamente pelo mesmo raciocínio invertido; em apps que *são* wrappers sem guardrail, "o LLM responde qualquer coisa" é comportamento esperado, não vulnerabilidade demonstrada. **(2) ASR saturado e sem estatística:** a Tabela 4 é quase inteiramente 5/5/5/5/5; um ASR de 86,1% composto por células saturadas não discrimina mérito do método nem estabilidade; sem IC, sem teste, sem variação por semente de temperatura (GPT-3.5 a temp=1 no *judge*). **(3) Circularidade do oráculo:** GPT-3.5 gera o ataque, GPT-3.5 julga o sucesso (§5.6/§6.1) e a verificação manual não reporta concordância inter-avaliador. **(4) Vazio entre exploit e informação:** os autores admitem (§3.2, §5.6) que o prompt impresso pode ser alucinação; para PROMPT LEAKING — a contribuição central — isso é fatal *salvo* validação pelo fornecedor, que existe só para 10 de 31 casos; nos 21 anônimos a "vulnerabilidade" pode ser uma alucinação plausível nunca confirmada. A ablação cobre apenas o Separator; não há baseline automatizado forte (GPTFuzzer, PAIR, TAP) contra o qual o loop HOUYI fosse comparado. A §7.1 (6 defesas contornadas) é afirmada "por inspeção manual" sem tabela, alvos ou protocolo. Nota 4 e não 3 porque o desenho do pilot (§3.3, análise de falhas) é genuinamente bom e a validação por 10 fornecedores ancora o achado principal. |
| D4 | Relevância prática / realismo | 15% | **8** | 7–8 (cenário realista) | Cenário black-box contra 36 serviços comerciais reais com tráfego de produção; disclosure responsável com 10 confirmações de fornecedores, incluindo Notion (>20M usuários); OWASP Top 10 LLM #1. É o ponto mais forte do artigo. Ressalva que impede 9–10: a estimativa financeira (US$ 259,2/dia para PAREA) é extrapolação pontual de preço de API, e o snapshot experimental é de meados de 2023 (GPT-3.5-turbo, Supertools) — para WCIA 2026, mesmo a v3 de dez/2025 traz corpus de ameaças de três safras atrás, quando guardrails de prompt-leak já se difundiram. |
| D5 | Reprodutibilidade | 15% | **3** | 3–4 (só menção vaga) | **Nenhum artefato público declarado no texto sob revisão** — sem repositório, sem prompts do HOUYI (os prompts de *guidance* do contexto-inferer, do gerador de Separator e do oráculo de feedback jamais são impressos), sem dataset de Q&A, sem harness. Só se conhece o tamanho (2.150 LoC Python) e parâmetros do judge (temp=1, top_p=1). O §7.3 *admite* que a reprodutibilidade será perdida ("transient nature"), e 33 dos 36 alvos são aliases inidentificáveis, então nem o achado é auditável de ponta a ponta: apenas 3 nomes públicos (Notion, Writesonic, PAREA) e 1 caso de leak com prompt real impresso (Botsonic). A aleta de serviço RESTful feita "manualmente" para cada app é trabalho não publicado. A tarefa pede que eu avalie "reprodutibilidade dos prompts/ataques publicados no repositório GitHub dos autores": no texto que me foi entregue **não há repositório GitHub declarado** — registro a ausência como fato, e exijo a declaração em Q4. |
| D6 | Escrita e apresentação | 10% | **5** | 5–6 (razoável) | Estrutura clara e figures legíveis, mas densidade de erros que um revisor de segurança lê como pressa: "vanila", "Anaswer", "Seperator", "Pursueing", "generateing product websit", "WEHRE" no SQL da Fig. 3 (irônico num paper cuja analogia central é SQLi), "DECISIOAI", "we does not", "Despite mechanisms … have been introduced" (§8.1, agramatical). Prosa inflada ("groundbreaking", "Imaginatively", "meticulously", "alarming") onde dados bastariam. Não bloqueia leitura; não é impecável. |
| — | **WAvg = Σ(peso×nota)** | 100% | **4,6 / 10** | | Conta: 0,20×4 + 0,15×4 + 0,25×4 + 0,15×8 + 0,15×3 + 0,10×5 = 0,80 + 0,60 + 1,00 + 1,20 + 0,45 + 0,50 = **4,55 → 4,6** |

**Gates de integridade:**
- ( ) Fora de escopo do WCIA (D1 ≤ 2) — **não**; escopo "Ataques" é central.
- ( ) Quebra de anonimato na versão revisada — **não acionado**: a versão fornecida é a arXiv nominal; assume-se submissão anonímizada ao WCIA. Se a versão submetida ao comitê for esta, o gate dispara e a recomendação passa a ser R− forçada independentemente do que segue.
- ( ) Indícios de plágio/autoplágio/submissão múltipla — não observados (trabalho coeso com o grupo dos autores; auto-citação [33] declarada).
- ( ) Uso de IA generativa não declarado — não aplicado (artigo pré-2024 na origem; ver Bloco F).

## BLOCO C — Julgamento qualitativo

| Campo | Resposta |
|---|---|
| C1. Resumo do artigo em 2–3 frases | Os autores mostram que injeções diretas conhecidas ("ignore previous instructions", caracteres de escape) falham contra a maioria das aplicações LLM comerciais porque o input do usuário é tratado como *dado* e não como comando. Propõem o HOUYI, um ataque black-box em três fases (inferência do contexto, geração de payload com Framework/Separator/Disruptor, refinamento iterativo com feedback de LLM) inspirado em SQLi/XSS, no qual o segredo é "fechar" o contexto anterior antes de emitir a pergunta maliciosa. Aplicado a 36 serviços reais, o toolkit reporta 86,1% de sucesso (31 apps vulneráveis), com roubo de prompt (prompt leak) e uso gratuito da capacidade de LLM (prompt abuse), validados por 10 fornecedores, incluindo Notion. |
| C2. Principal contribuição (1 frase) | Evidência empírica de grande porte (36 apps, 10 confirmações de fornecedores) de que injeção de prompt sistemática, guiada por separação de contexto, é viável contra aplicações comerciais black-box, com dois cenários de dano concretos (leak/abuse). |
| C3. Principal fraqueza (1 frase) | A métrica de sucesso é inflada por um critério inconsistente (explorar = fazer o LLM responder qualquer coisa, inclusive o que é a função do app), saturada (quase tudo 5/5) e verificada por um oráculo-LLM circular, com o prompt furtado nunca desambiguado de alucinação fora dos 10 casos confirmados — e nada é publicamente reprodutível. |
| C4. Para artigo em andamento/position: o desenho proposto é plausível? | O desenho experimental executed existe e foi executado — não é position paper. Para virar artigo *curto* de 4 páginas aceitável: cortar pilot §3 para 0,5 p. (manter a tipologia de falhas), Tabela 4 resumida por categoria, manter Fig. 4 + um caso (Writesonic), §7.1 resumida a duas linhas. Para artigo completo aceito em venue A: refazer ASR com critério de sucesso unificado (dano funcional demonstrado, não mera resposta fora do escopo), baseline automatizado, oráculo independente do atacante, IC, e artefato público. |
| C5. O que um leitor leigo do SBSeg entende deste artigo? | Não obrigatório (perfil P2), mas registro: um leitor não-especialista sai entendendo a mensagem central ("instruções escondidas atrás de texto disfarçado enganam assistentes de IA e podem vazar o prompt do produto") — os exemplos em alemão/inglês da Fig. 4 e do caso DECISIONAI são bons vetores de divulgação. |

## BLOCO D — Confiança do revisor

| Campo | Resposta |
|---|---|
| D-C. **Confiança global na avaliação (C, 1–5)** | **4** — especialista na área de ataque (prompt injection/jailbreak é meu subdomínio de P2); não 5 apenas porque os artefatos ausentes impedem auditoria de detalhes de implementação. |
| D1c–D6c. Confiança por dimensão (1–5) | D1 **4** D2 **5** D3 **5** D4 **4** D5 **4** D6 **3** |
| Dimensões N/A (fora da competência — renormaliza pesos) | Nenhuma (P2 tem autoridade plena em D1–D5; D6 pontuada apenas por clareza técnica, conforme protocolo §5). |

## BLOCO E — Questões para os autores

| # | Questão | Tipo |
|---|---|---|
| Q1 | **Consistência do critério de sucesso:** na §3.2 vós descartais o sucesso de Q2 nos chatbots porque "responder a consultas é a função pretendida", e na Tabela 4 contais CODE GENERATION (quicksort) e CONTENT MANIPULATION em apps cuja função é exatamente gerar texto/código como exploração bem-sucedida. Reconciliai os dois padrões: para cada app, definia "vulnerável" por *desvio demonstrado da finalidade com dano* ou por *qualquer resposta fora do script*? Recontai o ASR sob o primeiro padrão e reportai o Δ. | (x) obrigatória |
| Q2 **Prompt leak vs. alucinação:** vós admitis (§3.2, §5.6) que o prompt impresso pode ser alucinação e que não o verificastes no pilot. Para os 21 apps vulneráveis a PROMPT LEAKING sem confirmação de fornecedor, que evidência independentes de que o texto revelado é o prompt real (hash/substring conhecida? comparação com vazamento posterior?)? Quantos dos 31 "vulneráveis" o são *apenas* por leak não confirmado? | (x) obrigatória |
| Q3 **Oráculo circular e verificação:** o feedback/sucesso é avaliado por GPT-3.5 (temp=1) — o mesmo tipo de modelo usado para gerar payloads. Qual a concordância entre o oráculo LLM e a verificação manual (Cohen's kappa ou equivalente)? A Tabela 4 mudaria com oráculo humano-cego ou modelo-judge de família distinta? | (x) obrigatória |
| Q4 **Artefato:** nenhum repositório ou link de artefato aparece no texto. Publicai (ou declarai política de liberação para) o toolkit, os prompts de guidance do Context Inferrer/Separator/judge, a Algorithm 1 implementada e os payloads vencedores por app — sem isso a vossa §7.3 "not only reproducible but also straightforward" (§5.2) não tem substrato. Se existe repositório GitHub dos autores, citai-o formalmente. | (x) obrigatória |
| Q5 **Defesas (§7.1):** alegais que HOUYI contorna as 6 defesas "por inspeção manual". Publicai a tabela defesas×apps×cenários com os prompts usados; sem isso a afirmação não é avaliável, sobretudo porque as defesas foram testadas apenas em "some open-source projects" não listados no texto. | (x) obrigatória |
| Q6 **Baseline automatizado e estatística:** comparai HOUYI com pelo menos um gerador automático de prompt-injection publicado (p. ex. GPTFuzzer/PAIR) no mesmo corpus, e reportai IC binomiais por célula da Tabela 4 (n=5 não distingue 5/5 de 4/5 com nenhum poder). | (x) obrigatória |
| Q7 *(sugestão)* Reportai custo em tokens/dinheiro e número de iterações do loop de refinamento por app — hoje o leitor não sabe quantas consultas o "86,1%" custou ao fornecedor, o que tensiona vossa própria nota de "avoiding mass repetitive experimentation". | ( ) sugestão |
| Q8 *(sugestão)* Atualizai a discussão de mitigação (v3 é de dez/2025): desde 2023 há defesas treinadas (classificadores de injeção, spot-lighting/prompt-masknet) e o cenário "app com guardrail" é a norma — sem isso, a relevância 2026 do snapshot 2023 fica frágil para o WCIA. | ( ) sugestão |
| Q9 *(sugestão)* Corrigir o inglês (vanila/Anaswer/Seperator/WEHRE/DECISIOAI/"we does not") — a Fig. 3 com "WEHRE" na analogia de SQLi é um troféu para qualquer revisor hostil. | ( ) sugestão |

## BLOCO F — Risco de texto gerado por IA (apoio ao editor — nunca critério de nota)

| Campo | Resposta |
|---|---|
| F1. Sinais qualitativos observados no texto | (x) outros (mistos): prosa com adjetivação hiperbólica recorrente e estruturas paralelas ("meticulously", "Imaginatively", "groundbreaking", tricolons em série) — compatíveis tanto com prosa acadêmica de autores não-nativos quanto com rascunho assistido; porém os numerosos erros de digitação/ortografia ("vanila", "Anaswer", "Seperator", "WEHRE", "generateing", "websit", "Pursueing") são **anti-signais** fortes de texto LLM finalizado, que tipicamente não erra assim. Sem mudança abrupta de registro entre seções; citações verificáveis (todas conferem com a literatura de 2022–2023 que conheço de P2: [44] Perez & Ribeiro, [20] Greshake et al., [33] Jailbreak ChatGPT dos próprios autores). |
| F2. Usou detector automático? Qual / resultado | (x) não — detectores são inúteis aqui: texto de 2023 possivelmente reeditado em 2025 (v3), exatamente a condição fora de distribuição que Mitchell et al. documentam como falha [R14 do protocolo]. |
| F3. **Risco global de texto IA no artigo** | (**x**) baixo — evidência concreta: densidade de typos fonéticos humanos, citações exatas e verificáveis, nomes internos de produtos consistentes; nada no texto sugere geração por LLM; a v3 (dez/2025) pode ter trechos revisados com ajuda de IA, o que seria uso legítimo declarado por norma SBC. |
| F4. O artigo DECLARA uso de IA generativa (Código SBC Art. 2º III)? | (x) não declara — irrelevante para o original de 2023, mas **se reenviado ao WCIA 2026 deverá declarar** (o artigo usa GPT-3.5 como componente metodológico do ataque, o que a chamada atual provavelmente pede para declarar no corpo, como parcialmente já ocorre em §6.1). |

## BLOCO G — Recomendação e pós-revisão

| Campo | Resposta |
|---|---|
| G1. **Recomendação** | ( ) A++ ( ) A+ ( ) A− (**x**) **R− Rejeite** |
| G2. WAvg deste revisor | **4,6 / 10** |
| G3. Justificativa da recomendação em ≤5 linhas | O material submetido viola a restrição de 4 páginas por um fator de ~4,5, e a condensação honesta apagaria a evidência tabular que sustenta o claim central. O conteúdo peca onde um revisor de segurança olha primeiro: ASR inflado por critério de sucesso auto-contraditório com o próprio pilot, saturado (5/5 generalizado, sem IC), julgado por LLM circular, com prompt-leak não desambiguado de alucinação em 2/3 dos casos e zero artefato público — as correções (Q1–Q6) são re-experimentação, não reescrita. A validação por 10 fornecedores é o mérito real e recomenda submissão futura, condensada e com artefato, a categoria completa. |
| G4. **Usei IA generativa nesta revisão?** | (x) **sim — na forma desta própria simulação:** a revisão é redigida por agente de IA (qwen3.8-flash-next-iq3_s) encenando a persona P2, exercício pedagógico da PCS5917. As notas, âncoras e recomendação refletem o julgamento técnico da persona conforme o protocolo; numa aplicação real do protocolo §7.1 este campo deveria registrar revisão humana com apoio de IA apenas para redação/sumarização/busca de referências. |
| G5. Enviei trechos do artigo a serviço externo? | (x) não — o texto foi lido integralmente em ambiente local; nenhuma citação longa foi colada em serviço externo (confidencialidade double blind preservada, protocolo §7.2). |
| G6. Assinatura do revisor (só para o editor) + data | Persona P2 (Segurança/IA Adversarial), revisão 1 de ART2 — sessão isolada — 23/11/2026 |

---

### Memória de cálculo (para a aba de consolidação do editor)

WAvg = 0,20×4 + 0,15×4 + 0,25×4 + 0,15×8 + 0,15×3 + 0,10×5
     = 0,80 + 0,60 + 1,00 + 1,20 + 0,45 + 0,50 = 4,55 ≈ **4,6**
Recomendação em 2 categorias (aceita/não) para kappa: **não**.
