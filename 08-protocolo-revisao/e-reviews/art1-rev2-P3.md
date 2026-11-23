# Formulário de Avaliação — Artigo Curto WCIA 2026 (v1.0)

> **Sessão isolada:** revisão produzida em sessão isolada, sem acesso a outras avaliações do artigo (revisão 1 de nenhum outro par foi vista), em conformidade com o protocolo §3 ("revisão completa sem ver a rubrica preenchida por ninguém").
> **Modelo usado:** qwen3.8-flash-next (via Hermes Agent) — simulação da persona P3 autorizada pelo protocolo didático da disciplina PCS5917; notas, âncoras e recomendação registradas conforme as regras §4–§5.
> **Persona:** P3 — engenheiro de software de outra área (engenharia de dados / backends), sem contato com IA adversarial, segurança de LLM ou jailbreaks. Li o artigo de uma vez, como leitor leigo do SBSeg.
> **Data/hora:** 23/11/2026

---

## BLOCO A — Metadados (preencher antes de ler o artigo)

| Campo | Resposta |
|---|---|
| A1. ID do artigo (nº JEMS/anonimizado) | Artigo 1 (versão anonimizada, 4 páginas) |
| A2. Título | "Quanto custa defender um chatbot bancário? Cascatas de guard models e juízes LLM" |
| A3. Autores declarados ao editor (invisível ao revisor — double blind) | *(campo do editor)* |
| A4. Categoria declarada | (X) Curto |
| A5. Nº de páginas / dentro do limite SBC? | 4 p. — (X) sim (3 de corpo + 1 final; ver comentário D1: a p. 4 mistura nota de apêndice com referências) |
| A6. Idioma | (X) PT (com abstract em EN) |
| A7. Bloco de tópicos do WCIA em que se enquadra | (X) Defesa/robustez — secundariamente (X) Avaliação/métricas/reprod. |
| A8. Perfil do revisor (M0 do protocolo §5) | (X) P3 Leigo na área |
| A9. Conflito de interesse declarado | (X) nenhum |
| A10. Tempo gasto na revisão (min) | ~40 min |

## BLOCO B — Scores por dimensão (âncoras do protocolo §4)

| Dim | Dimensão | Peso | Nota (1–10) | Âncora escolhida | Comentário obrigatório p/ nota ≤4 ou ≥9 |
|---|---|---|---|---|---|
| D1 | Aderência à chamada e ao formato | 20% | **8** | 7–8 (bem enquadrado) | — Template SBC respeitado, 4 páginas, PT com abstract EN, anonimato preservado ("Autor anônimo para revisão", afiliação removida). Tema claramente dentro de Defesa/robustez e do bloco "avaliação, métricas e reprodutibilidade" da chamada. Ressonância menor: a nota de contagens de dados (p. 4) aparece entre o fim do corpo e as referências, num espaço que a regra destina só a referências — não é infração evidente, mas fica apertado. |
| D2 | Originalidade da contribuição | 15% | **6** | 5–6 (incremento claro e pequeno) | — Pontuo só pelo que o texto comunica (confidence 2): o artigo mesmo se apresenta como combinação inédita de peças que "cada uma existe isolada" (cascatas + custo de erros + latência). Para mim, leigo, soa como incremento claro e útil mais do que direção nova; não tenho como saber se alguém já publicou isso. |
| D3 | Rigor metodológico/técnico | 25% | **N/A — fora da minha competência** | — | — Abstenção (§5): não tenho como avaliar se AUROC, "recall a 5% de FPR", Clopper–Pearson, ECE, IC bootstrap e o modelo C = c_guard + r_π·c_juíz + π·FNR·L + (1−π)·FPR·C_fp estão corretos ou se o desenho (split 30/70, n=626/185) é suficiente. Qualquer nota minha aqui seria ruído. Peso renormalizado sobre as demais. |
| D4 | Relevância prática / realismo | 15% | **8** | 7–8 (cenário realista) | — Autoridade plena: é exatamente a linguagem de quem opera sistema em produção — custo por 1M de requisições, p95 de latência, SLA de 300 ms, orçamento. A conclusão "a variável de controle do orçamento é a taxa de erro sob a restrição de latência, não o preço do modelo" é uma frase que qualquer time de plataforma entende e aplica. Ressalva: L=US$63 e C_fp=US$2,70 são hipóteses declaradas, e API de juiz a 2,6 s de p95 (T2) dificilmente passaria num SLA real de chatbot — o artigo mesmo diz que o juiz isolado não atende. |
| D5 | Reprodutibilidade | 15% | **6** | 5–6 (parte essencial descrita) | — Pontuo pelo texto (confidence 2): datasets nomeados com referências, model cards linkados (HuggingFace/GitHub com commit), regras de limiar e protocolo de medição descritos, até a contaminação de 3 guards é declarada. Mas não vi link para código/repositório do pipeline — para um artigo cujo produto é um modelo de decisão com números exatos, isso me deixaria na mão se quisesse rodar. |
| D6 | Escrita e apresentação | 10% | **5** | 5–6 (razoável) | — Como P3: a estrutura é boa (pergunta → método → tabelas → conclusão) e o resumo se lê bem, mas do meio do artigo em diante perdi o fio: "AUROC", "FNR/FPR", "recall a 5% de FPR", "cascata", "ECE", "banda [τb, τa]", "Clopper–Pearson" aparecem sem nenhuma explicação para quem não é da área. Numa conferência de segurança com painel misto (academia + mercado), isso é barreira real de leitura: entendi a ideia geral, mas as tabelas 1 e 2 são opacas para mim. Falta uma frase de glossário ou um exemplo numérico guiado. |
| — | **WAvg = Σ(peso×nota)** | 100% | **6,8 / 10** | *(D3=N/A: pesos renormalizados — ver conta abaixo)* | |

**Gates de integridade:**
- ( ) Fora de escopo do WCIA (D1 ≤ 2)
- ( ) Quebra de anonimato na versão revisada — *não vi; a menção a "b.ia (Bradesco)" é do cenário citado em nota de rodapé, não afiliação dos autores*
- ( ) Indícios de plágio/autoplágio/submissão múltipla
- ( ) Uso de IA generativa não declarado — *o artigo declara uso de IA explicitamente (p. 3)*

**Conta da WAvg (renormalização com D3 = N/A):**
- Pesos avaliados: D1 20 + D2 15 + D4 15 + D5 15 + D6 10 = **75**
- Σ(peso×nota) = (0,20×8) + (0,15×6) + (0,15×8) + (0,15×6) + (0,10×5)
- = 1,60 + 0,90 + 1,20 + 0,90 + 0,50 = **5,10**
- WAvg = 5,10 / 0,75 = **6,8**

## BLOCO C — Julgamento qualitativo

| Campo | Resposta |
|---|---|
| C1. Resumo do artigo em 2–3 frases | O artigo mede quanto custa filtrar ataques (jailbreaks e injeções de prompt) contra um chatbot de banco, testando 9 filtros automáticos baratos ("guards") e 3 modelos grandes caros ("juízes") com custo e latência medidos. Propõe um modelo de custo total que soma a conta da inferência com o prejuízo dos ataques que escapam, e mostra que uma "cascata" de três níveis — filtro barato → filtro médio → juiz caro só nos casos duvidosos — fica 2,2× mais barata que o melhor filtro sozinho, respeitando o prazo de resposta (p95 260 ms < SLA 300 ms). A lição prática: o orçamento deve ir para reduzir erros, não para o preço do modelo. |
| C2. Principal contribuição (1 frase) | Colocar custo de inferência, custo de erro e latência na mesma equação de decisão e mostrar, com números medidos, que a cascata multinível vence o guard isolado sob SLA. |
| C3. Principal fraqueza (1 frase) | Os números do cenário (L=US$63, C_fp=US$2,70, prevalência 1%) são hipóteses do próprio artigo, e sem ver o código/method por dentro um leitor externo não consegue checar se os US$ 73,5 mil/1M se sustentam. |
| C4. Para artigo em andamento/position: o desenho proposto é plausível? | O desenho parece plausível até onde posso julgar (como engenheiro de dados: medir custo/latência por rota e calibrar limiares num conjunto de calibração é rotina de ML em produção). Para virar artigo completo precisaria de: dataset financeiro real (não sintético "fácil"), PT traduzido por humanos (o próprio artigo reconhece o viés do tradutor), código público para reproduzir as tabelas, e calibração dos guards — que o artigo já lista como futuro. |
| C5. **O que um leitor leigo do SBSeg entende deste artigo? (obrigatório p/ P3)** | Entendi a mensagem de capa e a conclusão, que aliás são ótimas: "proteger chatbot de banco é dominado pelo custo dos ataques que passam, não pelo preço do filtro; encadear um filtro barato com um juiz caro só para as mensagens duvidosas sai ~2× mais barato e ainda cumpre o SLA". Isso ficou claro no resumo, na introdução e na conclusão. Mas a travessia entre elas é nebulosa para leigos: não sei o que significa AUROC 0,95 vs 0,85 na prática, o que é "recall a 5% de FPR", por que ECE 0,07–0,16 faz a regra teórica "falhar", nem o que "cascata" e "banda [τb, τa]" implicam num sistema real. As Tabelas 1 e 2, que carregam toda a evidência, são ilegíveis sem treinamento na área. Saí da leitura confiando no que os autores afirmam (o texto é honesto sobre limitações, o que ajuda), mas sem conseguir verificar nada — que é justamente a posição de metade provável da audiência do SBSeg. |

## BLOCO D — Confiança do revisor

| Campo | Resposta |
|---|---|
| D-C. **Confiança global na avaliação (C, 1–5)** | **2** |
| D1c–D6c. Confiança por dimensão (1–5) | D1 4 · D2 2 · D3 N/A · D4 4 · D5 2 · D6 4 |
| Dimensões N/A (fora da competência — renormaliza pesos) | **D3 — Rigor metodológico/técnico** |

*(Lembrete protocolo §6: recomendação com C ≤ 2 nunca sozinha sustenta rejeição; dispara novo revisor/adjudicador — é o caso aqui.)*

## BLOCO E — Questões para os autores

| # | Questão | Tipo |
|---|---|---|
| Q1 | Onde está o código/pipeline que gera as Tabelas 1–2? Sem ele, o modelo de custo esperado não é reproduzível por terceiros, que é o principal produto do artigo. (Falar também se a CSV do recorte bancário citada na p. 4 será pública.) | (X) obrigatória |
| Q2 | Podem explicar em uma frase leiga o que "recall a 5% de FPR" significa para o usuário final? Ex.: "de cada 100 golpes, quantos são bloqueados quando no máximo 5 clientes legítimos em 100 são bloqueados por engano"? Isso salvaria o artigo para leitores de fora da área. | (X) obrigatória |
| Q3 | O p95 do juiz T2 isolado é 2.666 ms, mas na cascata o p95 combinado vira 260 ms — qual a fração de requisições do p95 que escala ao juiz (r_π=5%) e como vocês garantem a cauda (requisições lentas escaladas não estourariam o percentil 95)? Deixei como sugestão porque não sei se isso já está coberto no método. | ( ) obrigatória (X) sugestão |

## BLOCO F — Risco de texto gerado por IA (apoio ao editor — nunca critério de nota)

| Campo | Resposta |
|---|---|
| F1. Sinais qualitativos observados no texto | (X) nenhum — o texto tem marcação autoral forte (hipóteses assumidas, limitações confessadas, números com IC largos); não notei mudança abrupta de registro nem listas genéricas de template. Citações não consegui verificar (fora da minha área), o que não é sinal de nada por si só. |
| F2. Usou detector automático? Qual / resultado | (X) não |
| F3. **Risco global de texto IA no artigo** | (X) baixo — evidência concreta: seção explícita "Uso de IA (SBC, Art. 2º, III)" declarando exatamente onde a IA entrou (geração do dataset D4, tradução PT, auxílio em código/redação); esse tipo de autodeclaração cirúrgica é incomum em texto gerado de ponta a ponta. |
| F4. O artigo DECLARA uso de IA generativa (Código SBC Art. 2º III)? | (X) sim, conforme |

## BLOCO G — Recomendação e pós-revisão

| Campo | Resposta |
|---|---|
| G1. **Recomendação** | (X) A− Rejeite fraca (revise-e-reenvie) |
| G2. WAvg deste revisor | **6,8 / 10** |
| G3. Justificativa da recomendação em ≤5 linhas | O problema é real e a mensagem é ótima para o SBSeg: orçamento de defesa deve mirar a taxa de erro sob restrição de latência (D4=8). Mas a escrita fecha o artigo para leitores de fora da bolha (D6=5) e falta o código para reproduzir as tabelas que sustentam tudo (D5=6). Não tenho competência para validar o método (D3=N/A), então confio no texto, que é honesto sobre as limitações. A−, não rejeição: com um glossário/exemplo guiado e artefatos públicos, isso vira um dos artigos mais citáveis do workshop. |
| G4. **Usei IA generativa nesta revisão?** | (X) sim — onde e o quê: esta revisão foi redigida por IA (qwen3.8-flash-next) no âmbito da simulação didática de persona P3 prevista na disciplina; as notas, âncoras, abstenção D3 e a recomendação seguem mecanicamente o protocolo §4–§5 declarado pela persona, sem acesso a outras revisões. |
| G5. Enviei trechos do artigo a serviço externo? | (X) não (o texto do artigo foi processado apenas localmente na sessão de revisão, preservando o blind) |
| G6. Assinatura do revisor (só para o editor) + data | Revisor P3 (sessão isolada art1-rev2) — simulação de persona de engenharia de dados/backends, registrada para o editor nos termos do protocolo §2/R3 — 23/11/2026 |
