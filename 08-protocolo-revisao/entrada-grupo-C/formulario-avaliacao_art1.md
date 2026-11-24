# Formulário de Avaliação — Artigo Curto WCIA 2026 (v1.0)

> Instrução de uso: preencher **uma folha por revisor por artigo**. Todas as notas usam as âncoras da tabela D1–D6 do `protocolo-revisao.md` §4 (o revisor marca a âncora; a banda 1–10 vem dela). Recomendação é **escolha obrigatória** — sem "não sei": na dúvida entre duas bandas, escolha a inferior e explique no comentário.

---

## BLOCO A — Metadados (preencher antes de ler o artigo)

| Campo | Resposta |
|---|---|
| A1. ID do artigo (nº JEMS/anonimizado) | |
| A2. Título | Quanto custa defender um chatbot bancário? Cascatas de guard models e juı́zes LLM |
| A3. Autores declarados ao editor (invisível ao revisor — double blind) | *(campo do editor)* |
| A4. Categoria declarada | ( ) Completo (x) Curto ( ) Position paper |
| A5. Nº de páginas / dentro do limite SBC? | 4 p. — (x) sim ( ) não |
| A6. Idioma | (x) PT ( ) EN |
| A7. Bloco de tópicos do WCIA em que se enquadra | ( ) Ataques (x) Defesa/robustez ( ) Sistemas/eng. IA ( ) Privacidade ( ) Avaliação/métricas/reprod. ( ) Governança/XAI ( ) nenhum → ver D1 |
| A8. Perfil do revisor (M0 do protocolo §5) | ( ) P1 CS geral (x) P2 Segurança/IA adversarial ( ) P3 Leigo na área |
| A9. Conflito de interesse declarado | (x) nenhum ( ) possível: ____________ |
| A10. Tempo gasto na revisão (min) | 40min |

## BLOCO B — Scores por dimensão (âncoras do protocolo §4)

| Dim | Dimensão | Peso | Nota (1–10) | Âncora escolhida (1–2/3–4/5–6/7–8/9–10) | Comentário obrigatório p/ nota ≤4 ou ≥9 |
|---|---|---|---|---|---|
| D1 | Aderência à chamada e ao formato | 20% | 10 | 10 | Paper aderente ao tema da conferência |
| D2 | Originalidade da contribuição | 15% | 7 | 6/7 | |
| D3 | Rigor metodológico/técnico | 25% | 6 | 6/7 | |
| D4 | Relevância prática / realismo | 15% | 5 | 4/5 | chatbot é um modelo concreto e implementado no mercado, porém os dados usados nos ataques são na maior parte sintéticos |
| D5 | Reprodutibilidade | 15% | 3 | 2/3 | artigos e card models são citados, mas sem código explícito do pipeline apresentado no artigo |
| D6 | Escrita e apresentação | 10% | 6 | 6/7 | |
| — | **WAvg = Σ(peso×nota)** | 100% | 6.35 / 10** | *(se dimensão N/A: renormalizar pesos das demais)* | |

**Gates de integridade (qualquer "sim" ⇒ recomendação forçada "Rejeite" + escalar editor):**
- ( ) Fora de escopo do WCIA (D1 ≤ 2)
- ( ) Quebra de anonimato na versão revisada
- ( ) Indícios de plágio/autoplágio/submissão múltipla (Código SBC Art. 1º)
- ( ) Uso de IA generativa não declarado quando evidently empregada (Código SBC Art. 2º III)

## BLOCO C — Julgamento qualitativo

| Campo | Resposta |
|---|---|
| C1. Resumo do artigo em 2–3 frases (com as próprias palavras do revisor) | Artigo trabalha na defesa de prompts adversariais a um chatbot de grande uso no mercado (setor bancário). A proposta é testar o uso de pipeline de guards de defesa vis-a-vis a utilizacão de apenas um modelo. Métricas como perda financeira e latência são fatores de otimizacao. |
| C2. Principal contribuição (1 frase) | Agregacao de modelos na defesa a prompts adversariais combinando guards e LLM como juízes. |
| C3. Principal fraqueza (1 frase) | Dados sintéticos pouco realistas, viés na traducão para portugues, e abertura de novas superfícies de ataque com o uso de modelosno pipeline. |
| C4. Para artigo em andamento/position: o desenho proposto é plausível? O que precisaria faltar estar pronto para virar artigo completo? | |
| C5. O que um leitor leigo do SBSeg entende deste artigo? (obrigatório p/ perfil P3) | |

## BLOCO D — Confiança do revisor

| Campo | Resposta |
|---|---|
| D-C. **Confiança global na avaliação (C, 1–5)** | 3 |
| D1c–D6c. Confiança por dimensão (1–5) | D1 8 D2 5 D3 6 D4 9 D5 9 D6 7 |
| Dimensões N/A (fora da competência — renormaliza pesos) | ____________ |

*(Lembrete protocolo §6: recomendação com C ≤ 2 nunca sozinha sustenta rejeição; dispara novo revisor.)*

## BLOCO E — Questões para os autores

| # | Questão (numerar; separar obrigatórios de sugestões) | Tipo |
|---|---|---|
| Q1 | Qual a identificacão correta do percentual da inferência no cenário vencedor? | (x) obrigatória ( ) sugestão |
| Q2 | Apresentacão da estimativa de Cfp. Como esse valor é estimado? | ( ) obrigatória (x) sugestão |
| Q3 | Qual o valor máximo de latência dentro dos 5% piores casos? | ( ) obrigatória (x) sugestão |

## BLOCO F — Risco de texto gerado por IA (apoio ao editor — nunca critério de nota)

| Campo | Resposta |
|---|---|
| F1. Sinais qualitativos observados no texto | ( ) nenhum ( ) mudança abrupta de registro ( ) citações não verificáveis ( ) listas genéricas/estruturas de template de LLM ( ) outros: ______ |
| F2. Usou detector automático? Qual / resultado | ( ) não ( ) sim: ____________ — escore: ____ |
| F3. **Risco global de texto IA no artigo** | ( ) baixo ( ) médio ( ) alto — **evidência concreta que sustenta a classificação:** |
| F4. O artigo DECLARA uso de IA generativa (Código SBC Art. 2º III)? | ( ) sim, conforme ( ) declara mas fora do padrão ( ) não declara ( ) irrelevante/nenhum uso |

## BLOCO G — Recomendação e pós-revisão

| Campo | Resposta |
|---|---|
| G1. **Recomendação** | ( ) A++ Aceite forte ( ) A+ Aceite (x) A− Rejeite fraca (revise-e-reenvie) ( ) R− Rejeite |
| G2. WAvg deste revisor | 6.35 / 10 |
| G3. Justificativa da recomendação em ≤5 linhas | Artigo traz novas contribuicões ao agregar modelos guards e LLMs como juíz para defesa contra prompt injection. O tema é aderente a conferência. Os modelos utilizados foram citados e referenciados, porém sem divulgacão de artefato científico para reproducão. |
| G4. **Usei IA generativa nesta revisão?** | ( ) não (x) sim — onde e o quê: ajuda em aspectos específicos de terminologias da área. |
| G5. Enviei trechos do artigo a serviço externo? | ( ) não (x) sim — risco de confidencialidade avaliado: sem risco de re-uso de dados para treinamento. |
| G6. Assinatura do revisor (só para o editor) + data | |

---

### Aba de consolidação (preenchida pelo editor)

| Artigo | Revisor 1 (perfil) WAvg/rec/C | Revisor 2 (perfil) WAvg/rec/C | Adjudicador WAvg/rec | Δ = \|WAvg₁−WAvg₂\| | Kappa entre revisores (≥3) | Regra aplicada (§6) | **Decisão final** |
|---|---|---|---|---|---|---|---|
| A1 | 6.40/A- | 6.80/A- | 6.35/A- | 0.40 |  | | A- |

*Escala de leitura do kappa: faixas de Landis & Koch (1977) — <0,20 fraco; 0,21–0,40 regular; 0,41–0,60 moderado; 0,61–0,80 quase perfeito; >0,80 quase-perfeito total.*
