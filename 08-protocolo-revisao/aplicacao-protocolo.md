# Aplicação do Protocolo — Plano Operacional (aluno sozinho)

**Disciplina:** PCS5917 — IA Adversarial (2026/2) · **Autor:** Leonardo Kawakami Hissanaga — NUSP 11374864
**Parceiros de documento:** `wcia-estudo.md` · `protocolo-revisao.md` · `formulario-avaliacao.md`

---

## 1. O que o enunciado exige e qual é o gargalo real

O enunciado pede: (a) aplicar o protocolo em **≥2 artigos submetidos ao WCIA**; (b) cada artigo avaliado por **≥2 pessoas diferentes**; (c) trocar formulários + artigos + scores com outro grupo, que devolve a **decisão editorial**. Como o aluno é individual, "artigos submetidos ao WCIA" se resolve de forma honesta com (i) o artigo próprio do aluno (submetido conceitualmente ao WCIA, prazo 02/12 — v0 já existe em `produto/artigo-wcia-v0.md`) e (ii) um segundo texto alinhado ao escopo do WCIA; e "duas pessoas diferentes" se resolve com **perfis de revisor declarados + proxy documentado** (opções em §4), com a limitação assumida por escrito no relatório.

## 2. Artigo-alvo 1 — o artigo do próprio aluno (definido)

- **Texto:** `produto/artigo-wcia-v0.md` — *"Segurança Adversarial de LLMs na Prática de Sala de Aula: Um Estudo Empírico de Jailbreaks, Defesas a Nível de Prompt e Trojan em Hardware com Avaliação por Juiz LLM"* (rascunho v0; categoria-alvo: **artigo curto**, ≤4 páginas SBC).
- Enquadramento WCIA verificado: bloco de tópicos "Ataques e exploração de vulnerabilidades" + "Avaliação, métricas e reprodutibilidade" (`wcia-estudo.md` §2).
- **Ressalva de blind:** o autor não pode revisar o próprio texto; nas duas revisões do artigo 1 o autor entra apenas como **editor** (consolidação), nunca como revisor. Isso inclusive reforça a narrativa do relatório: um revisor humano externo e um revisor-proxy (ou dois proxies com perfis distintos) revisam o texto do aluno.
- Condição: até 25/11 o v0 deve estar estável o bastante para revisão (versão congelada com data/hora; marca `[PENDENTE]` é aceitável e será tratada como "trabalho em andamento" pela regra do protocolo §4).

## 3. Artigo-alvo 2 — candidatos reais (todos verificados em 15/11/2026)

Critérios: alinhamento aos tópicos do WCIA, PDF público, tamanho compatível com a carga da atividade. **A escolha final é do aluno**; recomenda-se o C1.

| # | Candidato | URL | Perfil de esforço | Observação |
|---|-----------|-----|-------------------|------------|
| **C1 (recomendado)** | Liu, Y. et al. *Prompt Injection attack against LLM-integrated Applications.* arXiv:2306.05499 (v3, dez/2025). | <https://arxiv.org/abs/2306.05499> | Médio (lê-se ~§1–4 + avaliação) | Ataque com ASR/estatísticas — exercita D3/D4/D5 do formulário em cheio; tema idêntico ao da disciplina. |
| **C2** | Greshake, K. et al. *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.* arXiv:2302.12173. | <https://arxiv.org/abs/2302.12173> | Médio | Mesmo bloco de tópicos; boa base para comparação com o artigo do aluno (que usa injecção indireta em T5? não — comparação de método). |
| **C3** | Um dos **artigos curtos aceitos** publicados nos anais SOL do SBSeg 2026 (p.ex. "From Implicit Trust to Continuous Verification..." — UNIPAMPA; lista com 4 títulos em `wcia-estudo.md` §6), localizando o PDF em <https://sol.sbc.org.br>. | <https://sol.sbc.org.br> | Baixo (4 páginas) | É literalmente "artigo submetido ao WCIA" na categoria curta — maximiza fidelidade ao enunciado; risco: menos material para discordância. |
| **C4** | Mitchell, E. et al. *DetectGPT...* arXiv:2301.11305 (usada no protocolo §7). | <https://arxiv.org/abs/2301.11305> | Alto (técnico) | Só se o revisor humano tiver fôlego; bom para testar o perfil P3 (leigo) com confidence baixa. |

> Seleção recomendada: **C1** (ou **C3** se o aluno quiser fidelidade literal máxima ao enunciado, podendo consultar os chairs da disciplina antes). Os dois formulários do artigo 2 ficam prontos em uma sessão de ~2 h somando os revisores.

## 4. "Duas pessoas diferentes" — opções (a decisão final é do aluno)

| Opção | Como funciona | Custo | Fidelidade ao enunciado | Risco/limitação a declarar |
|-------|---------------|-------|--------------------------|----------------------------|
| **O1 — Colega de turma** | Um colega da PCS5917 (ou colega de outro curso como P3) assina um dos formulários de cada artigo, após ler `protocolo-revisao.md` e sem ver o formulário do aluno (ordem: revisão independente primeiro). | Depende de disponibilidade | **Alta** — é literalmente a segunda pessoa | se o colega tiver o mesmo background, o pareamento P1/P2/P3 (§5 do protocolo) fica fraco; pedir um P3 real (ex. colega de outra engenharia) |
| **O2 — Duplo julgamento por LLM como proxy documentado** | O aluno roda **duas sessões independentes** de LLMs distintos (idealmente modelos/escalas diferentes; na infra local da disciplina: p.ex. Qwen2.5 via vLLM/llama.cpp e um segundo endpoint), cada uma instruída com (a) o protocolo, (b) um perfil de persona (P2 segurança; P3 leigo), (c) o PDF, e preenchendo o formulário. As transcrições integrais vão como anexo. | Baixo (infra já existe) | **Média** — dois revisores são sistemas diferentes, mas não duas pessoas | deve ser **declarado como limitação** no relatório; cite Zheng et al. (2023, arXiv:2306.05685) — LLM-as-judge tem viés posicionamento/verbosidade — como justificativa de por que é proxy e não equivalência |
| **O3 — Duplo perfil humano-simulado pelo próprio aluno** | O aluno preenche dois formulários em momentos distintos, declarando perfis diferentes (P2 e P3), cego ao primeiro preenchimento. | Nulo | **Baixa** | é autocrítica, não revisão por pares; aceitável apenas como complemento |

**Combinação recomendada (O1+O2):** se conseguir 1 colega (O1), cada artigo tem revisor humano + revisor-LLM (proxy) → 2 avaliações independentes por artigo com origem metodológica diferente, e a discordância (Δ) alimenta a tabela de adjudicação do protocolo de verdade. Se não houver colega, O2 puro: dois LLMs distintos + o aluno como editor, com a seção "Limitações" do relatório afirmando explicitamente que "avaliação por dois agentes de IA não satisfaz plenamente o requisito de duas pessoas; protocolo e formulário são, no entanto, aplicáveis sem mudança a revisores humanos". **Opcionalmente**, as duas passagens de O2 (e a de O1 se houver) também disparam a regra de adjudicação com Δ > 1,5 usando o aluno-adjudicador P2 — demonstrando o mecanismo de terceiro revisor.

## 5. Cronograma até 25/11 14h (BRT)

| Dia | Ação |
|-----|------|
| 16–17/11 | Congelar `artigo-wcia-v0` (snapshot datado); escolher candidato do artigo 2; convidar colega (O1) com prazo 20/11 |
| 18–19/11 | Rodar revisão-LLM (O2) dos 2 artigos (sessões isoladas, transcrições salvas); enviar PDF + formulário em branco ao colega |
| 20–21/11 | Receber formulário do colega (fallback 22/11: reforçar O2 com 3º modelo); preencher formulário do aluno (como editor não revisa o próprio artigo 1; revisa o artigo 2 como P2) |
| 22/11 | Consolidação: aba do editor, Δ, kappa (se 3+), adjudicações; decisão final por artigo |
| 23–24/11 | Redigir relatório em grupo (versão individual): protocolo + justificativa citada, formulários próprios e "recebidos" (os dos proxies/colega), links dos artigos, decisões; gerar PDF |
| 25/11 ≤14h | Entrega. Enviar pacote ao outro grupo/aluno parceiro: formulários preenchidos + 2 artigos + scores + decisões, e registrar o pacote recebido de volta |

## 6. Pacote de troca (checklist do que sai e do que entra)

**Sai (para o outro grupo):** formulário vazio (`formulario-avaliacao.md`), os 2 artigos (PDF/MD com link), os formulários preenchidos pelo nosso "grupo", a aba de consolidação com WAvg/Δ. **Entra (recebido de volta):** as decisões finais deles sobre os mesmos artigos + comentários de meta-review. **Assimétria importante a registrar no relatório:** como a troca é feita depois das nossas decisões, cada lado vê primeiro só os insumos, não as decisões do outro — mantendo a independência pedida pelo enunciado.

## 7. Limitações conhecidas (para transcrever no relatório)

1. Revisores-LLM proxies: vieses documentados de LLM-as-judge (posição, verbosidade, auto-preferência) — Zheng et al. 2023, arXiv:2306.05685 (título/autores verificados em 15/11/2026 na página do arXiv).
2. O artigo 2 real (arXiv) **não foi submetido ao WCIA**; a aplicação é analógica ("texto no escopo do WCIA"); a alternativa C3 resolveria isso com artigo curto real dos anais SOL.
3. O artigo 1 contém resultados `[PENDENTE]` — avaliado como "trabalho em andamento" (categoria legítima de artigo curto do WCIA), não como artigo acabado.
4. O WCIA 2026 não publica rubrica oficial; pesos/faixas de adjudicação são proposta desta disciplina, calibrada nas estatísticas oficiais (WAvg, ≥3 revisões) — não confundir com regra oficial do evento.
