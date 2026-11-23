# Ata de Consolidação — Atividade "Protocolo de Revisão de Artigo" (PCS5917)

**Editor:** Leonardo Kawakami Hissanaga — NUSP 11374864 (trabalho individual; aluno atua como editor, nunca como revisor do próprio artigo — blind mantido)
**Data da consolidação:** 23/11/2026
**Matéria-prima:** 5 formulários em `e-reviews/` (preenchimento independente; o formulário humano foi escrito antes de qualquer proxy)

## Painéis

| Artigo | Rev 1 | Rev 2 | Rev 3 |
|---|---|---|---|
| ART-1 (aluno, guardrails) | P2-proxy: **6,4 / A− / C4** | P3-proxy: **6,8 / A− / C2** (D3=N/A, pesos renormalizados) | — (autor é editor) |
| ART-2 (HOUYI arXiv) | P2-proxy: **4,6 / R− / C4** | P3-proxy: **4,8 / R− / C3** (D3=N/A) | **humano P2: 7,1 / A+ / C4** |

## Regra aplicada por artigo (protocolo §6)

### ART-1
- Δ(R1,R2) = |6,4 − 6,8| = **0,4 < 1,5**; recomendações à 0 banda de distância (ambas A−).
- Regra 1 da tabela §6: decide a **média das WAvg = (6,4+6,8)/2 = 6,6** → banda 5,5–7,4 → **REJEITE FRACA (revise-e-reenvie)**.
- Nota do editor sobre a regra "C ≤ 2 nunca sustenta rejeição sozinha": R2 tem C=2, mas a rejeição fraca **não** se sustenta sozinha nele — R1 (C=4) converge na mesma recomendação e na mesma banda de média. Sem gatilho de substituição; registrado na ata (protocolo §6 linha 4 lida com rejeição *baseada* em review C≤2, não com convergência corroborada).
- Kappa: painel tem 2 revisores apenas → kappa de recomendação não calculável (par único, n=1 artigo; ver nota metodológica abaixo). Calculou-se kappa **sobre as âncoras D1–D6** (ver §Kappa).

### ART-2
- Δ(R1,R2) = |4,6 − 4,8| = **0,2 < 1,5**; ambas R− → Regra 1: média **4,7 < 5,5 → rejeite**.
- Porém o painel tem 3 revisores e R3 (humano) diverge: Δ(R2,R3) = |4,8 − 7,1| = **2,3 ∈ [1,5; 3,0]** e recomendações a 3 bandas → gatilho de adjudicação. O protocolo diz: terceiro revisor P2 adjudica e decide a **mediana das três WAvg**. R1 (P2) já revisou de forma independente *antes* de ver os demais formulários — cumpre a ordem "revisão sozinho → leitura dos pares" — e o editor o converte em adjudicador com essa ressalva registrada.
- **Mediana(4,6; 4,8; 7,1) = 4,8** → **REJEITE** na categoria artigo curto.
- **Gate de integridade registrado (R2, D1=2 ⇒ fora de formato):** vai direto ao editor e não se resolve por média. Nota do editor: o gate aqui é **administrativo, não científico** — o PDF fornecido é a versão arXiv nominal de 18 páginas de um trabalho cujo conteúdo é forte; a rejeição vale *para a categoria artigo curto as-submitted*. Meta-review do editor: **"rejeite com convite de reenvio na categoria artigo completo"** — decisão final.
- Os três revisores convergem no conteúdo quando o gate é posto de lado: R2 (leigo) escreve que o conteúdo é forte e sugere tratamento administrativo; R3 (humano) dá aceite condicionado a condensação; R1 (P2) estima que a condensação honesta para 4 p. destruiria a evidência tabular — ou seja, a discordância de recomendação é quase inteiramente explicada por **como cada painel lê a regra de formato**, não pelo artigo.

## Kappa (recomendação binarizada aceita {A++,A+} vs. não {A−,R−})

- Par R1↔R2 (ambos revisaram os 2 artigos): acordo 2/2 = 100%; **kappa indefinido** (todas as categorias num só lado — sem variância; limitação reportada, não escondida).
- Pares com R3 (1 artigo comum cada): acordo 0/1; kappa indefinido com n=1.
- **Nota metodológica para o relatório:** com 2 artigos e painéis de 2–3 revisores, kappa de recomendação é estatisticamente vazio. O protocolo previa essa fragilidade (≥3 revisores por artigo *e* painel maior). Como substituto auditável, calculou-se kappa **sobre as âncoras de banda das dimensões** (1–2/3–4/5–6/7–8/9–10), que multiplica os itens por painel:

| Par (artigo) | itens comuns (bandas D) | acordo | p_e (chance) | kappa | Landis & Koch |
|---|---|---|---|---|---|
| R1-P2 ↔ R2-P3 (ART-1) | 5 dims (D3=N/A no P3) | 4/5 | 0,48 | **+0,62** | quase perfeito |
| R1-P2 ↔ R2-P3 (ART-2) | 5 dims (D3=N/A no P3) | 3/5 | 0,24 | **+0,47** | moderado |
| R1-P2 ↔ R3-humano (ART-2) | 6 dims | 0/6 | 0,14 | **−0,16** | fraco |
| R2-P3 ↔ R3-humano (ART-2) | 5 dims | 0/5 | 0,24 | **−0,32** | fraco |

- Cálculo: bandas de âncora do protocolo §4 (1–2/3–4/5–6/7–8/9–10) por dimensão; kappa de Cohen com p_e empírica dos próprios painéis; dimensões N/A excluídas do par.
- Leitura: os dois **proxies** (mesmo instrumento, personas diferentes) concordam entre si (0,47–0,62); **ambos discordam do humano** em todas as dimensões pareadas do ART-2 (kappa negativo — pior que o acaso — viés sistemático de instrumento). O humano deu nota mais alta em 11/11 dimensões comparáveis: o especialista humano lê "86,1% com confirmação de vendor" como força; os proxies lêem o mesmo número como métrica não auditada. É o viés previsto por Zheng et al. 2023 manifestando-se **dentro do experimento** — e vira achado central do relatório (§5.4), não ruído escondido.

## Decisões finais

| Artigo | Decisão | Fundamento |
|---|---|---|
| ART-1 | **Rejeite fraca (revise-e-reenvie)** — média 6,6 | Δ=0,4; consenso P2+P3; questões Q1–Q7 do revisor P2 como lista de correção para a entrega de 02/12 |
| ART-2 | **Rejeite na categoria curta, com convite de reenvio como artigo completo** | mediana 4,8; gate de formato (administrativo); conteúdo reconhecido forte pelos 3 revisores |

## Ações geradas
1. **[para a At. Escrita, 02/12]** Aplicar as Q1–Q7 de `art1-rev1-P2.md` no artigo do aluno: corrigir "2,1%" (é da rota sem SLA, não da cascata-headline), unidades da col. Inf. da Tab. 2, contradição rπ≤5% vs. rotas com 30%/12%, IC pareado, derivação de Cfp, sensibilidade de π.
2. **[troca]** Pacote de saída em `saida/pacote-troca/` — enviar a outro grupo; receber a decisão editorial deles.
3. **[entrega]** PDF do relatório no Moodle até 25/11 14h.
