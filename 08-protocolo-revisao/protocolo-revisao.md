# Protocolo de Revisão de Artigos Curtos — WCIA 2026 (adaptação didática, PCS5917)

**Disciplina:** PCS5917 — Inteligência Artificial Adversarial (2026/2)
**Autor:** Leonardo Kawakami Hissanaga — NUSP 11374864 (trabalho individual; o enunciado previa grupos, a entrega é individual)
**Versão:** 1.0 — 15/11/2026
**Documento companheiro:** `wcia-estudo.md` (fatos do WCIA), `formulario-avaliacao.md` (formulário), `aplicacao-protocolo.md` (aplicação)

---

## 1. Contexto e restrições projetuais

O WCIA 2026 **não publica rubrica de revisão**; mas publica três pistas oficiais (ver `wcia-estudo.md` §5): (i) revisão **double blind**; (ii) **todo artigo recebeu ≥3 revisões independentes**; (iii) decisão por **"média ponderada das avaliações (WAvg)"** na casa de 0–10 (dois artigos > 8,0). O protocolo abaixo é construído para ser *compatível com esse processo* e *robusto ao problema conhecido de baixa concordância entre revisores* (justificativa em §2). Ele é deliberadamente curto o bastante para ser aplicado a artigos de ≤4 páginas em ≤45 min por revisor.

**Escopo de aplicação:** artigos curtos do WCIA — até 4 páginas SBC (3 de corpo + 1 de referências), trabalhos em andamento, propostas e position papers, em português ou inglês (URL: https://www.sbseg2026.uff.br/workshops/wcia/).

## 2. Justificativa (por que cada regra existe — literatura verificada)

Cada regra do protocolo aponta para a evidência que a motiva. Todas as referências abaixo foram verificadas em 15/11/2026 (DOI/URL conferidos em Crossref, OpenAlex ou página do arXiv; lista completa em §8).

**R1 — O desacordo entre revisores é estrutural, não ruído removível; o protocolo precisa medir o desacordo, não fingi-lo.**
Estudo clássico de 135 revisores/66 propostas do NIH mostrou que a recomendação de um revisor prediz quase nada a do outro e a decisão final (Cole, Cole & Simon, *Science*, 1981) [R1]. Réplica moderna em periódico: entre 2.264 manuscritos e 5.881 revisões, o acordo chance-corrigido dos revisores sobre rejeitar vs. aceitar foi **kappa = 0,11** (Kravitz et al., *PLoS ONE*, 2010) [R2]; análise de 134 mil revisões de quatro financiadores confirma que o desacordo tem estrutura estável, não é aleatório (Hesselberg et al., *PLOS ONE*, 2026) [R3]. **Consequência:** (a) dois revisores é piso, não teto; (b) o protocolo define *a priori* gatilhos de adjudicação por delta de score (§6); (c) o formulário calcula concordância (kappa de Cohen [R4]; faixas de interpretação de Landis & Koch [R5]) — os mesmos instrumentos já usados no protocolo humano–juiz da própria disciplina (produto/protocolo-avaliacao-humana.md), mantendo coerência metodológica do portfólio.

**R2 — Reviewers são melhores com rubrica estruturada do que com texto livre.**
Revisões com formulário estruturado/checklist aumentam a qualidade e a cobertura da revisão frente a texto livre (Mehmani & Malički, *European Science Editing*, 2024) [R6]; o toolkit de revisão da EASE (European Association of Science Editors, 2025) consolida a mesma recomendação prática [R7]. Treinamento guiado por instruções explícitas melhora a qualidade mediana das revisões em ensaio randomizado (Schröter, Black, Evans & Carpenter, *BMJ*, 2004) [R8]. **Consequência:** formulário com âncoras de escala por dimensão (não só números) — o revisor escolhe a âncora que descreve o artigo e o número vem junto, o que padroniza critérios entre avaliadores de backgrounds distintos (§4).

**R3 — O anonimato e a responsabilidade alteram o comportamento do revisor.**
Ensaios randomizados mostram que abrir a identidade do revisor não degrada e pode elevar a qualidade/construtividade da revisão (van Rooyen, Godlee, Evans & Black, *BMJ*, 1999; van Rooyen, Delamothe & Evans, *BMJ*, 2010) [R9][R10]. Como o WCIA exige double blind, mantemos sigilo de autorias e adicionamos **assinatura nominal interna do revisor** (conhecida só pelo "editor"/professor), replicando o efeito de responsabilização sem violar o blind. **Consequência:** campo "identificação do revisor (para o editor)" no formulário.

**R4 — Dimensões: quais e por quê.**
As seis dimensões abaixo cobrem os critérios recorrentes catalogados na literatura sobre peer review (Bornmann, *Annual Review of Information Science and Technology*, 2011) [R11] e foram filtradas pelo escopo oficial do WCIA (ênfase em "avaliação empírica, reprodutibilidade e cenários realistas") e pelo Código de Conduta da SBC, que recomenda declarar disponibilidade de dados/código (Art. 2º, I) e o uso de IA generativa (Art. 2º, III) [R12]:
- **Originalidade** — contribuição nova vs. incremental [R11].
- **Rigoro técnico/metodológico** — validade interna do experimento/argumento; em IA adversarial, p.ex.: ASR sem IC, n pequeno, ausência de baseline [R11][R2].
- **Relevância prática/impacto** — pedido explícito da chamada do WCIA por "cenários realistas" e colaboração academia–indústria [R13].
- **Reprodutibilidade** — código/dados/modelos declarados; é critério editorial recomendável da SBC e tópico explícito da chamada (bloco "Avaliação, métricas e reprodutibilidade") [R12][R13].
- **Escrita/presentation** — clareza para o leitor-alvo do SBSeg.
- **Aderência à chamada** — escopo (um dos 6 blocos de tópicos), formato (4 páginas, template SBC, idioma, anonimato) [R13].

**R5 — Risco de texto gerado por IA: sinal, não veredito.**
Detectores zero-shot de texto de LLM (p.ex. DetectGPT, Mitchell et al., arXiv/ICML, 2023) têm acurácia alta em distribuição mas fragilizam sob edição/adversarial [R14]; ferramentas de detecção já entraram em fluxo editorial de artigos e revisões (nota de notícia na *Nature*, 2025) [R15]. Como o Código da SBC **não proíbe** IA generativa — exige **declaração** —, o protocolo trata "risco de texto IA" como campo descritivo de apoio ao editor, nunca como critério de rejeição automático (§7).

**R6 — Backgrounds diferentes são recursos, não problemas.**
A própria baixa concordância [R1][R2] sugere que painéis heterogêneos amostram critérios complementares; a solução operacional é dar a cada perfil dimensões de autoridade plena e dimensões de autoridade limitada (marcadas por *confidence*), evitando que um leigo em IA adversarial pontifique sobre rigor criptográfico ou que um especialista em segurança ignore legibilidade. Detalhe em §4.

## 3. Processo resumido (visão de 30 segundos)

1. **Atribuição:** cada artigo curto → ≥2 revisores com perfis complementares (regra em §5). O revisor declara seu perfil antes de ler.
2. **Leitura guiada (≤45 min):** revisão 1 completa **sem ver a rubrica preenchida por ninguém**; preenchimento do formulário (`formulario-avaliacao.md`) com âncoras, comentários e recomendação.
3. **Consolidação:** editor calcula WAvg de cada revisor, o delta Δ = |WAvg₁ − WAvg₂| e a concordância de recomendação (kappa quando ≥3 revisores).
4. **Adjudicação:** sem discordância → decisão direta; com discordância → terceiro revisor (adjudicador) ou *meta-review* do editor (§6).
5. **Auditoria de IA:** registro do uso de IA pelos revisores e do risco percebido de texto IA nos artigos (§7).

## 4. Dimensões, escalas e pesos

Cada dimensão é pontuada de **1 a 10** com âncoras fixas (o revisor marca a âncora; o número é derivado, reduzindo deriva pessoal de escala). O score final é a **média ponderada (WAvg, 0–10)** — formatamente compatível com a "média ponderada (WAvg) > 8,0" reportada pelo WCIA [R13].

| # | Dimensão | Peso | 1–2 | 3–4 | 5–6 | 7–8 | 9–10 |
|---|----------|-----|-----|-----|-----|-----|------|
| D1 | **Aderência à chamada e ao formato** (escopo, template SBC, limite de páginas, idioma, anonimato) | 20% | fora de escopo ou fora de formato | escopo marginal / formatação irregular | dentro do escopo com desvios leves | bem enquadrado | exemplo de submissão WCIA |
| D2 | **Originalidade da contribuição** | 15% | repetição do já publicado | variação menor | incremento claro e pequeno | novidade notável | direção nova/métrica nova |
| D3 | **Rigor metodológico/técnico** (desenho, baseline, n, métricas, ameaças à validade) | 25% | falha fatal de método | falhas graves | falhas corrigíveis | sólido | exemplar p/ artigo curto |
| D4 | **Relevância prática / realismo do cenário** | 15% | puramente hipotético | pouca conexão com prática | aplicável com ressalvas | cenário realista | deployável/perturba prática |
| D5 | **Reprodutibilidade** (dados, código, modelos, comandos declarados) | 15% | nada declarado | só menção vaga | parte essencial descrita | artefatos anunciados | artefatos públicos |
| D6 | **Escrita e apresentação** (clareza, estrutura, figuras, idioma) | 10% | ilegível | difícil | razoável | clara | impecável |

**Regras de pontuação:**
- **Artigo em andamento/position paper:** D3 e D4 são avaliadas pelo *desenho proposto* (plausibilidade do protocolo experimental), não por resultados ausentes — coerente com a definição oficial de artigo curto do WCIA ("trabalhos em andamento ou propostas... position papers") [R13]. Nota obrigatória no comentário.
- **Gate duro:** D1 ≤ 2 (fora de escopo) ou violação de anonimato/plágio ⇒ recomendação forçada "Rejeite" com justificativa, qualquer que seja a WAvg (critério de integridade, Código SBC Art. 1º [R12]).
- **WAvg** = Σ(peso × score), arredondada a 1 casa decimal.

## 5. Regras para avaliadores com backgrounds diferentes

Cada revisor auto-classifica-se (campo M0 do formulário):

| Perfil | Definição | Autoridade plena | Autoridade limitada |
|--------|-----------|------------------|---------------------|
| **P1 — Computação geral** | CS sem especialização em segurança/IA | D1, D3 (método geral), D5, D6 | D2, D4 (marcar confidence ≤ 3 se fora da zona) |
| **P2 — Segurança/IA adversarial** | pesquisa ou prática em segurança ofensiva/defensiva, ML de segurança | D1–D4, D5 | D6 apenas para clareza técnica |
| **P3 — Leigo na área** | CS ou profissional de outra área, sem contato com o tópico do artigo | D1, D4, D6 | D2, D3, D5 — pontuar pelo texto e obrigatoriamente confidence ≤ 2; comentar "o que um leitor do SBSeg leigo entende" |

- **Pareamento obrigatório:** todo artigo deve ser lido por um P1/P2 **e** um revisor de outra linha (P2+P3 ou P1+P2 de subáreas distintas) — espelha o painel de 45 membros do PC do WCIA com origens acadêmica e de mercado [R13] e operacionaliza R6.
- **Confidence (C, 1–5):** o revisor autoavalia 1 (chute informado) a 5 (certeza de especialista). Recomendação com C ≤ 2 nunca sozinha sustenta rejeição: o editor deve chamar adjudicador (§6). É o campo "confiança do revisor" presente em formulários de PC de conferências; aqui é decisivo porque a heterogeneidade é declarada [R6].
- Revisor **leigo tem direito a abstensão por dimensão** (campo "N/A — fora da minha competência"), que redistribui o peso das demais dimensões *daquele revisor* proporcionalmente, em vez de forçar nota inflada/degradada [R2].

## 6. Adjudicação com 2+ revisores e discordância

Sejam WAvg₁, WAvg₂ as médias ponderadas dos dois revisores e **Δ = |WAvg₁ − WAvg₂|**. Faixas de recomendação (o formulário converte a escolha do revisor em banda): **Aceite forte (A++) / Aceite (A+) / Rejeite fraca — revise-e-reenvie (A−) / Rejeite (R−)**.

| Situação | Regra de decisão |
|---|---|
| Δ < 1,5 **e** recomendações a no máx. 1 banda de distância | Decide a **média das WAvg**: ≥7,5 aceite; 5,5–7,4 rejeite fraca; <5,5 rejeite. |
| Δ ∈ [1,5, 3,0] **ou** recomendações a ≥2 bandas | **Terceiro revisor (adjudicador)**, sempre P2, lê o artigo e os dois formulários *depois* de revisar sozinho (ordem: revisão → leitura dos pares) e emite WAvg₃. Decisão pela mediana das três WAvg. |
| Δ > 3,0 | Adjudicador **obrigatório**, com meta-review obrigatório explicando a discordância. |
| Qualquer revisor com C ≤ 2 na recomendação-gatilho | Substitui por novo revisor em vez de adjudicar (evita desempatar com chute). |
| Gates de integridade disparados por qualquer revisor | Vão direto ao editor (não se resolvem por média) [R12]. |
| ≥3 revisores no painel | Registrar **kappa de Cohen** [R4] entre pares sobre a recomendação em 2 categorias (aceita / não) e interpretar pelas faixas de Landis & Koch [R5]; kappa < 0,21 (acordo "fraco") dispara nota metodológica na ata, independentemente da decisão — honestidade editorial recomendada pela literatura [R1][R2]. |

**Mecânica editorial da atividade (simulação):** o "editor" é o aluno sozinho; ele roda a tabela acima mecanicamente e registra a ata com os deltas. A troca entre grupos do enunciado equivale a o outro grupo ser o "comitê" que recebe formulários + artigos + scores e devolve a decisão.

## 7. Política de uso/detecção de IA generativa pelo REVISOR

Simetria com o Código da SBC, que vincula autores (declaração explícita, ferramentas nunca autoras, responsabilidade integral humana — Art. 2º, III [R12]) e, na ausência de norma para revisores no WCIA 2026 [R13], estabelece para este protocolo:

1. **Permitido e declarado:** a revisão pode usar IA generativa para (a) clarear a redação dos *próprios comentários* do revisor, (b) resumir seções do artigo para conferência de consistência, (c) procurar referências ausentes (com verificação humana antes de citar). **Proibido:** transferir a tarefa avaliativa — notas, âncoras e recomendação devem ser decisão humana registrada.
2. **Confidencialidade:** artigo em revisão double blind é confidencial; o revisor não deve colar trechos extensos em serviços que reteriam o texto para treino (cláusula de privacidade — a revisão, como a submissão, deve preservar o blind).
3. **Declaração obrigatória:** campo próprio do formulário ("Usei IA generativa nesta revisão? Onde? O quê?") — se o revisor responder "não", responde também se inspecionou indícios.
4. **Risco de texto IA no ARTIGO (campo de apoio, nunca veredito):** o revisor registra sinais qualitativos (mudança de registro, citações não verificáveis, listas genéricas, marcas de template de LLM) e opcionalmente passa detector (p.ex. DetectGPT [R14]; estado da arte e suas fragilidades em [R15]). **Nenhum score por dimensão pode ser reduzido apenas com base em saída de detector**: os detectores falham sob edição e produzem falsos positivos [R14]; o Código da SBC trata IA como uso legítimo declarado, não como falta [R12]. Suspeia grave com evidência concreta ⇒ escalar ao editor como questão de integridade, não como nota.

## 8. Referências (verificadas em 15/11/2026)

| # | Referência | Verificação |
|---|-----------|-------------|
| R1 | Cole, S.; Cole, J.; Simon, G. A. (1981). Chance and Consensus in Peer Review. **Science** 214. DOI: [10.1126/science.7302566](https://doi.org/10.1126/science.7302566) | Crossref ✓ |
| R2 | Kravitz, R. L.; Franks, P.; Feldman, M. D.; Gerrity, M.; Byrne, C.; Tierney, W. M. (2010). Editorial Peer Reviewers' Recommendations at a General Medical Journal: Are They Reliable and Do Editors Care? **PLOS ONE** 5(4):e10072. DOI: [10.1371/journal.pone.0010072](https://doi.org/10.1371/journal.pone.0010072) | Crossref + página do artigo com abstract completo ✓ (kappa 0,11; ICC 0,23) |
| R3 | Hesselberg, J.-O.; Ulleberg, P.; Sørensen, Ø.; Fostervold, K. I.; Ingvaldsen, S. H.; Svege, I. C. (2026). Why do reviewers disagree? Evidence from four funders and 134,000 reviews. **PLOS ONE**. DOI: [10.1371/journal.pone.0356108](https://doi.org/10.1371/journal.pone.0356108) | OpenAlex ✓ (registro com título/autores) |
| R4 | Cohen, J. (1960). A Coefficient of Agreement for Nominal Scales. **Educational and Psychological Measurement** 20. DOI: [10.1177/001316446002000104](https://doi.org/10.1177/001316446002000104) | Crossref ✓ |
| R5 | Landis, J. R.; Koch, G. G. (1977). The Measurement of Observer Agreement for Categorical Data. **Biometrics** 33(1). DOI: [10.2307/2529310](https://doi.org/10.2307/2529310) | Crossref ✓ |
| R6 | Mehmani, B.; Malički, M. (2024). Structured peer review: implementation and checklist development. **European Science Editing** 50. DOI: [10.3897/ese.2024.e137675](https://doi.org/10.3897/ese.2024.e137675) | Crossref + página da revista (CC-BY) ✓ |
| R7 | EASE Peer Review Committee (2025). *EASE Peer Review Toolkit* (Malicki, Mehmani, Horbach, Stojanovski). DOI: [10.14293/ease.2025.027](https://doi.org/10.14293/ease.2025.027) | Crossref ✓ |
| R8 | Schröter, S.; Black, N.; Evans, S.; Carpenter, J. (2004). Effects of training on quality of peer review: randomised controlled trial. **BMJ**. DOI: [10.1136/bmj.38023.700775.ae](https://doi.org/10.1136/bmj.38023.700775.ae) | Crossref ✓ |
| R9 | van Rooyen, S.; Godlee, F.; Evans, S.; Black, N. (1999). Effect of open peer review on quality of reviews and on reviewers' recommendations: a randomised trial. **BMJ** 318:23. DOI: [10.1136/bmj.318.7175.23](https://doi.org/10.1136/bmj.318.7175.23) | Crossref ✓ |
| R10 | van Rooyen, S.; Delamothe, T.; Evans, S. (2010). Effect on peer review of telling reviewers that their signed reviews might be posted on the web: randomised controlled trial. **BMJ**. DOI: [10.1136/bmj.c5729](https://doi.org/10.1136/bmj.c5729) | Crossref ✓ |
| R11 | Bornmann, L. (2011). Scientific peer review. **Annual Review of Information Science and Technology** 45. DOI: [10.1002/aris.2011.1440450112](https://doi.org/10.1002/aris.2011.1440450112) | Crossref ✓ |
| R12 | SBC. *Código de Conduta para Autores em Publicações da SBC* (28/02/2024). <https://sol.sbc.org.br/index.php/indice/conduta> | Página extraída na íntegra ✓ |
| R13 | WCIA 2026 — página oficial (tópicos, instruções, estatísticas WAvg, ≥3 revisões). <https://www.sbseg2026.uff.br/workshops/wcia/> | Página extraída na íntegra ✓ |
| R14 | Mitchell, E.; Lee, Y.; Khazatsky, A.; Manning, C. D.; Finn, C. (2023). DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature. arXiv:2301.11305. <https://arxiv.org/abs/2301.11305> | Página do arXiv ✓ (autores/título; ICML 2023 não re-verificado aqui — citar como arXiv) |
| R15 | Naddaf, M. (2025). AI tool detects LLM-generated text in research papers and peer reviews. **Nature** (notícia). DOI: [10.1038/d41586-025-02936-6](https://doi.org/10.1038/d41586-025-02936-6) | Crossref ✓ (título/veículo/ano no registro) |

**Não incluídas por falha na verificação:** Weller et al., "Peer Review: Inter-Reviewer Disagreement" (PLoS Biology, ~2006) — trabalho citado frequentemente sobre desacordo, mas não localizei registro confiável em Crossref/OpenAlex nesta sessão; foi substituído por Kravitz 2010 [R2] e Hesselberg 2026 [R3], que cobrem o mesmo papel argumentativo com registros verificados.
