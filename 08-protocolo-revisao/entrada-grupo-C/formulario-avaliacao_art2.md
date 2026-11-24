# Formulário de Avaliação — Artigo Curto WCIA 2026 (v1.0)

> Instrução de uso: preencher **uma folha por revisor por artigo**. Todas as notas usam as âncoras da tabela D1–D6 do `protocolo-revisao.md` §4 (o revisor marca a âncora; a banda 1–10 vem dela). Recomendação é **escolha obrigatória** — sem "não sei": na dúvida entre duas bandas, escolha a inferior e explique no comentário.

---

## BLOCO A — Metadados (preencher antes de ler o artigo)

| Campo | Resposta |
| :---- | :---- |
| A1. ID do artigo (nº JEMS/anonimizado) |  |
| A2. Título | Prompt Injection attack against LLM-integrated Applications&nbsp; |
| A3. Autores declarados ao editor (invisível ao revisor — double blind) | *Yi Liu et al.&nbsp;* |
| A4. Categoria declarada | () Completo (x) Curto ( ) Position paper |
| A5. Nº de páginas / dentro do limite SBC? | 18 p. — ( ) sim (x) não |
| A6. Idioma | ( ) PT (x) EN |
| A7. Bloco de tópicos do WCIA em que se enquadra | (x) Ataques ( ) Defesa/robustez ( ) Sistemas/eng. IA ( ) Privacidade (x ) Avaliação/métricas/reprod. () Governança/XAI ( ) nenhum → ver D1 |
| A8. Perfil do revisor (M0 do protocolo §5) | N/A \- revisor |
| A9. Conflito de interesse declarado | (x) nenhum ( ) possível: \_\_\_\_\_\_\_\_\_\_\_\_ |
| A10. Tempo gasto na revisão (min) | 40 |

BLOCO B — Scores por dimensão (âncoras do protocolo §4)

| Dim | Dimensão | Peso | Nota (1–10) | Âncora escolhida (1–2/3–4/5–6/7–8/9–10) | Comentário obrigatório p/ nota ≤4 ou ≥9 |
| :---- | :---- | :---- | :---- | :---- | :---- |
| D1 | Aderência à chamada e ao formato | 20% | 4 | 3-4 | Embora o artigo esteja alinhado ao escopo temático do WCIA, excede significativamente o limite de páginas e não atende à exigência de anonimato.&nbsp; |
| D2 | Originalidade da contribuição | 15% | 6 | 5-6 |  |
| D3 | Rigor metodológico/técnico | 25% | 5,5 | 5-6 |  |
| D4 | Relevância prática / realismo | 15% | 8 | 7-8 |  |
| D5 | Reprodutibilidade | 15% | 4 | 3-4 | A disponibilidade limitada de artefatos experimentais e a dependência de aplicações comerciais dificultam a reprodução independente e a validação dos resultados apresentados.&nbsp; |
| D6 | Escrita e apresentação | 10% | 5 | 5-6 |  |
| — | **«Mediana dos WAvg dos revisores**&nbsp; | 100% | **4,8  / 10** | *(se dimensão N/A: renormalizar pesos das demais)* |  |

**Gates de integridade (qualquer "sim" ⇒ recomendação forçada "Rejeite" \+ escalar editor):**

- ( ) Fora de escopo do WCIA (D1 ≤ 2\)  
- (x) Quebra de anonimato na versão revisada  
- ( ) Indícios de plágio/autoplágio/submissão múltipla (Código SBC Art. 1º)  
- ( ) Uso de IA generativa não declarado quando evidently empregada (Código SBC Art. 2º III)

## BLOCO C — Julgamento qualitativo

| Campo | Resposta |
| :---- | :---- |
| C1. Resumo do artigo em 2–3 frases (com as próprias palavras do revisor) | O artigo investiga vulnerabilidades de segurança em aplicações integradas a (LLMs, focando em ataques de prompt injection. Os autores apresentam o HOUYI, uma abordagem para avaliar essas vulnerabilidades. Os experimentos realizados em 36 aplicações comerciais identificaram vulnerabilidades em 31 delas, com a confirmação de dez fornecedores. |
| C2. Principal contribuição (1 frase) | Avaliação sistemática de vulnerabilidades em aplicações reais integradas a LLMs, demonstrando a relevância prática dos ataques de injeção de prompts.&nbsp; |
| C3. Principal fraqueza (1 frase) | Limitações na reprodutibilidade experimental, devido à dependência de aplicações comerciais e à disponibilidade limitada de artefatos.&nbsp; |
| C4. Para artigo em andamento/position: o desenho proposto é plausível? O que precisaria faltar estar pronto para virar artigo completo? |  |
| C5. O que um leitor leigo do SBSeg entende deste artigo? (obrigatório p/ perfil P3) |  |

BLOCO D — Confiança do revisor

| Campo | Resposta |
| :---- | :---- |
| D-C. **Confiança global na avaliação (C, 1–5)** | 4 |
| D1c–D6c. Confiança por dimensão (1–5) | N/A \- Editorial |
| Dimensões N/A (fora da competência — renormaliza pesos) | D3 não avaliada pelo revisor R2 (P3) |

*(Lembrete protocolo §6: recomendação com C ≤ 2 nunca sozinha sustenta rejeição; dispara novo revisor.)*

## BLOCO E — Questões para os autores

| \# | Questão (numerar; separar obrigatórios de sugestões) | Tipo |
| :---- | :---- | :---- |
| Q1 | Adequar a extensão e a formatação do artigo às normas do WCIA.&nbsp; | (x) obrigatória ( ) sugestão |
| Q2 | Garantir o anonimato dos autores na versão submetida.&nbsp; | (x ) obrigatória ( ) sugestão |
| Q3 |  | ( ) obrigatória ( ) sugestão |

BLOCO F — Risco de texto gerado por IA (apoio ao editor — nunca critério de nota)

| Campo | Resposta |
| :---- | :---- |
| F1. Sinais qualitativos observados no texto | (x) nenhum ( ) mudança abrupta de registro ( ) citações não verificáveis ( ) listas genéricas/estruturas de template de LLM ( ) outros: \_\_\_\_\_\_ |
| F2. Usou detector automático? Qual / resultado | (x) não ( ) sim: \_\_\_\_\_\_\_\_\_\_\_\_ — escore: \_\_\_\_ |
| F3. **Risco global de texto IA no artigo** | (x) baixo ( ) médio ( ) alto — **evidência concreta que sustenta a classificação:** |
| F4. O artigo DECLARA uso de IA generativa (Código SBC Art. 2º III)? | ( ) sim, conforme ( ) declara mas fora do padrão (x) não declara ( ) irrelevante/nenhum uso |

BLOCO G — Recomendação e pós-revisão

| Campo | Resposta |
| :---- | :---- |
| G1. **Recomendação** | ( ) A++ Aceite forte ( ) A+ Aceite ( ) A− Rejeite fraca (revise-e-reenvie) (x) R− Rejeite |
| G2. WAvg deste revisor | 4,8 / 10 |
| G3. Justificativa da recomendação em ≤5 linhas | O artigo apresenta relevância prática e aderência temática ao evento. Entretanto, não atende aos requisitos de extensão e anonimato. A nota consolidada também indica rejeição, recomendando-se o reenvio na categoria de artigo completo.&nbsp; |
| G4. **Usei IA generativa nesta revisão?** | ( ) não (x ) sim — onde e o quê:  sumarização de informações específicas da área |
| G5. Enviei trechos do artigo a serviço externo? | ( ) não (x) sim — risco de confidencialidade avaliado: Nenhum |
| G6. Assinatura do revisor (só para o editor) \+ data | Mario G. Batista, 23/11/2026 |

---

### Aba de consolidação (preenchida pelo editor)

| Artigo | Revisor 1 (perfil) WAvg/rec/C | Revisor 2 (perfil) WAvg/rec/C | Adjudicador WAvg/rec | Δ \= \|WAvg₁−WAvg₂\| | Kappa entre revisores (≥3) | Regra aplicada (§6) | Decisão final |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| A2 | P2 — 4,6 / R− / 4&nbsp; | P3 — 4,8 / R− / 3&nbsp; | 4,6 / R− (R1)&nbsp; | 0,2 |  |  |  |

*Escala de leitura do kappa: faixas de Landis & Koch (1977) — \<0,20 fraco; 0,21–0,40 regular; 0,41–0,60 moderado; 0,61–0,80 quase perfeito; \>0,80 quase-perfeito total.*