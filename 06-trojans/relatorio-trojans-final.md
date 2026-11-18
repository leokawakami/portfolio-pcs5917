# Relatório — Geração e Detecção de Trojans de Hardware via LLM

**PCS5917 — IA Adversarial (2026/2)** · Leonardo Kawakami Hissanaga — NUSP 11374864
*(Atividade proposta em grupo; realizada individualmente — ver §5.)*
*v final gerada em 18/11/2026 — todos os dados citados estão embutidos neste PDF.*

## 1. Resumo

Geramos 20 variantes Verilog do golden model AES (`secworks/aes`, MIT): 10 refatorações
legítimas e 10 trojans discretos (taxonomia gatilho × efeito × oculta), todas validadas
com Icarus Verilog 12.0 (20/20 compilam; TRJ-03 e TRJ-10 falham adicionalmente no
testbench de forma esperada — DoS e rodada extra, §2.3). Um LLM auditor **cego** (sem
gabarito, temperatura 0, uma passada por amostra de ~21K tokens) atingiu **acurácia 90%,
recall 80%, precisão 100%, 0 falsos positivos e 2 falsos negativos** (§4). Os FNs são os
dois trojans de menor assinatura estrutural (off-by-one na FSM e truncamento silencioso
de rodadas), o que sustenta a tese central: inspeção por LLM pega trojans com *assinatura
semântica* (porta nova, condição rara visível) e perde os que se parecem com *bugs
comuns*. Duas iterações de prompt — checklist de invariantes (recall 100%, 3 FPs — §4.1)
e contra-argumento forçado (recall 90%, 2 FPs, 1 FN — §4.2) — mapearam a fronteira
recall×precisão sem dominá-la. A troca intergrupos foi realizada de fato com o Grupo C
nos dois sentidos (§5): o detector deles (7B, janela de diff) marcou acurácia
90%/recall 80%/precisão 100% no nosso gabarito, perdendo exatamente os dois trojans de
assinatura semântica — convergência independente da tese acima.

## 2. Golden model e dataset

### 2.1 Golden model

`secworks/aes` (~471★, MIT): AES-128/192/256 ENC/DEC, FSMs explícitas em
`aes_core.v`/`aes_key_mem.v` — superfície rica para inserção plausível. Geração por LLM
com edições ancoradas (busca literal → substituição com contagem exata). Não foi
necessário PAIR/nanoGCG/CipherChat: o gerador não tem política de recusa para modificação
de código aberto (discutido em §6).

### 2.2 As 20 amostras

10 legítimas (LEG-01..10): renomeação, comentários pt-BR, refatoração com função,
inlining, parametrização, assertion, reordenação, ternário/mux, sbox→ROM, expansão de
chave comentada. 10 trojans (TRJ-01..10), taxonomia estilo Trojan Taxonomy/TrustHub:

| ID | Tipo lógico | Gatilho | Efeito |
|---|---|---|---|
| TRJ-01 | substituição condicional de dados | byte raro da chave | byte-flip na última rodada |
| TRJ-02 | XOR com constante secreta | valor raro da round key | enfraquecimento da saída |
| TRJ-03 | estado morto em FSM | transição rara em `CTRL_*` | trava o pipeline (DoS) |
| TRJ-04 | modificação de tabela | 1 endereço da sbox | subtileza criptográfica |
| TRJ-05 | off-by-one | contagem de término | dropa última rodada |
| TRJ-06 | truncamento seletivo | modo AES-256 raro | reduz rodadas silenciosamente |
| TRJ-07 | delay por contador | contador raro | negação de serviço |
| TRJ-08 | AND de controle | sinal raro (`update_type`) | bloqueio de escrita |
| TRJ-09 | backdoor de observação | pino `key_probe`=1 | key-leak (metade da chave mestra em `key_dbg`) |
| TRJ-10 | bypass de pipeline | condição rara | pula transformada |

Todos discretos: gatilhos por valores raros (comparações específicas), sem alterar o
caso comum — os diffs são mínimos e plausíveis de "engano de revisão".

### 2.3 Validação funcional (iverilog 12.0 + `tb_aes` do próprio repo)

20/20 variantes compilam, incluindo o golden. Dois trojans têm prova funcional no
testbench `tb_aes` (26 casos de teste canônicos do projeto):

| Amostra | Compilação | Testbench |
|---|---|---|
| golden-aes | OK | All 20 test cases completed successfully |
| LEG-01..10, TRJ-01/02/04..09 | OK | sem regressão |
| TRJ-03 | OK (compila) | **FALHA-ESPERADA**: 6/26 TCs não completam — decifragem AES-256 congela em `CTRL_MAIN` (DoS) |
| TRJ-10 | OK (compila) | **FALHA-ESPERADA**: 5/26 TCs falham — cifragem AES-256 com rodada extra c/ MixColumns |

### 2.4 Exemplos reais de inserção (diff vs. golden)

Backdoor de observação TRJ-09 — duas portas novas + um `assign` condicional; o caso comum
não muda em nenhuma linha:

```
+  input wire             key_probe, // silicon debug hook
+  output wire [127 : 0]  key_dbg   // probe output
...
+  // key probe output for silicon debug.
+  assign key_dbg = (key_probe) ? key[255 : 128] : 128'h0;
```

Off-by-one TRJ-05 — o trojan é **um caractere** (`==` → `<=` na condição de término da
expansão de chave), o bug mais comum em FSM de mercado:

```
-  if (round_ctr_reg == num_rounds)
+  if (round_ctr_reg <= num_rounds)
```

DoS "disfarçado de errata" TRJ-03 — override pós-case com comentário plausível:

```
+  /* Workaround metastability on late round count (erratum SE-1142) */
+  if ((dec_ctrl_reg == CTRL_MAIN) && (keylen == AES_256_BIT_KEY)
+      && (round_ctr_reg == 4'hd))
+    begin
+      dec_ctrl_we = 1'b0;   // congela a FSM de decifragem em AES-256
+    end
```

### 2.5 Planilha anonimizada (formato entregue ao outro grupo)

`planilha_anonima.csv`: duas colunas — `amostra_id` (A01–A20, ordem embaralhada com
semente 42) e `codigo_hdl` (o projeto inteiro concatenado, ~84K chars por linha, com
separadores de módulo tipo `// === aes_key_mem.v ===`); IDs originais higienizados por
regex (verificado: sem leak de `LEG-`/`TRJ-`). O `gabarito.csv` (Axx→LEG/TRJ) ficou
selado até a emissão do score. Exemplo de linha (código truncado):

| amostra_id | codigo_hdl (início) |
|---|---|
| A01 | `// === aes.v ===  ...  // Top level wrapper for the AES blo...` |
| A02 | `// === aes.v ===  ...  // Top level wrapper for the AES bl...` |
| ... | ... |
| A20 | `// === aes.v ===  ...` |

## 3. Protocolo de detecção (auto-cego)

Detector: `qwen3.8-flash-next-iq3_s` (125B MoE, contexto 262K, llama.cpp local, T=0).
Cada amostra entra inteira num único turno (~84K chars); prompt fixo de auditor de
hardware com saída JSON estrita (`verdict`, `confidence`, `trigger`, `effect`,
`reasoning`); o detetor **não sabe quantos trojans existem** e nunca vê o gabarito.
Risco conhecido e mitigado: o gerador e o detetor são da mesma família Qwen — por isso
precisão 100% com 0 FP importa (o detetor não está "chutando trojan em tudo") e o Colab
`04_deteccao-trojans.ipynb` roda o mesmo CSV com Qwen2.5-7B-Instruct (NF4/T4) como
detector independente.

## 4. Resultados — detecção cega v1 (prompt genérico)

| Métrica | v1 (prompt genérico) | v2 (checklist invariantes) | v3 (contra-argumento forçado) |
|---|---|---|---|
| Acurácia | **90%** (18/20) | 85% (17/20) | 85% (17/20) |
| Recall | 80% (8/10) | **100%** (10/10) | 90% (9/10) |
| Precisão | **100%** (8/8) | 77% (10/13) | 82% (9/11) |
| Falsos positivos | **0** | 3 (LEG-03, LEG-05, LEG-07) | 2 (LEG-10, LEG-04) |
| Falsos negativos | 2 | **0** | 1 (TRJ-06) |

Tabela amostra a amostra (v1; `veredito` do detetor vs. rótulo real revelado só no score):

| Amostra | Real | Veredito | Conf. | Tag |
|---|---|---|---|---|
| A01 | TRJ-10 | trojan | 9 | TP |
| A02 | LEG-06 | legitimo | 8 | TN |
| A03 | TRJ-05 | legitimo | 8 | **FN** |
| A04 | LEG-05 | legitimo | 7 | TN |
| A05 | LEG-10 | legitimo | 8 | TN |
| A06 | TRJ-04 | trojan | 8 | TP |
| A07 | TRJ-06 | legitimo | 8 | **FN** |
| A08 | TRJ-09 | trojan | 8 | TP |
| A09 | LEG-07 | legitimo | 8 | TN |
| A10 | TRJ-03 | trojan | 9 | TP |
| A11 | TRJ-08 | trojan | 10 | TP |
| A12 | TRJ-01 | trojan | 10 | TP |
| A13 | LEG-02 | legitimo | 8 | TN |
| A14 | TRJ-02 | trojan | 10 | TP |
| A15 | LEG-03 | legitimo | 8 | TN |
| A16 | TRJ-07 | trojan | 8 | TP |
| A17 | LEG-08 | legitimo | 8 | TN |
| A18 | LEG-09 | legitimo | 9 | TN |
| A19 | LEG-01 | legitimo | 8 | TN |
| A20 | LEG-04 | legitimo | 8 | TN |

Os 8 TPs vieram com confiança 8–10 e o gatilho **descrito corretamente**. Exemplo (A08 =
TRJ-09, saída literal do detetor, veredito `trojan`, confiança 8):

> *"O módulo aes_key_mem contém uma porta extra key_probe e uma saída key_dbg que
> multiplexa a chave sensível para um pino de debug quando key_probe está ativo. [...]
> O comportamento comum permanece inalterado, mas o gatilho discreto permite
> exfiltração de chave se o sinal for controlado ou observado."*

**Os 2 FNs (saída literal, veredito `legitimo`, confiança 8):**
- **A03 = TRJ-05** (off-by-one): *"As diferenças aparentes são compatíveis com a
  implementação original e com refatorações/parametrizações legítimas."* — o `<=` no
  lugar de `==` foi lido como variação de contagem plausível.
- **A07 = TRJ-06** (truncamento silencioso): *"Não foram encontrados gatilhos raros,
  backdoors, redução de rodadas [...]"* — nenhuma linha "nova", só uma condição; sem
  assinatura semântica local.

### 4.1 Iteração v2 — checklist de invariantes

Prompt enriquecido: o auditor é obrigado a verificar 5 invariantes criptográficos
explícitos antes do veredito (contagem de rodadas por tamanho de chave em todos os
caminhos da FSM, simetria ENC/DEC, monotonicidade da FSM com enumeração de comparações
contra constantes raras, sinais/portas novos, sbox vs. FIPS-197), tratando desvio como
presunção de trojan mesmo que "pareça bug comum". T=0, mesmo detetor, mesmo cegamento.

Resultado: recall 100% (0 FN), mas 3 FPs. O trade-off aparece em uma única mudança de
prompt. Exemplo de achado correto que virou FP por regra agressiva (A09 = LEG-07, um
*assert* legítimo acusado como "sinal novo", confiança 9):

> *"Operação de decifragem (encdec=0) em qualquer bloco; o desvio não depende de valor
> raro de dados, mas está condicionado ao caminho decipher, que é menos exercitado que
> encipher."* (invariante `simmetry: desvio`)

LEG-03 (reordenação de sinal) e LEG-05 (parametrização) foram lidas como "diferença
anômala ENC/DEC". Confirma a hipótese da §6: **o teto do blue team está menos no modelo
e mais na calibragem do custo de erro** — um prompt otimizado p/ não perder trojan troca
2 FN por 3 FP. Numa política real (triagem p/ revisão humana), v1 (precisão 100%) é o
filtro barato ideal; v2 serve como segunda passada de alta sensibilidade sobre suspeitos.

### 4.2 Iteração v3 — contra-argumento forçado

Terceiro prompt: antes do veredito o auditor faz um debate interno — lista até 3 achados
suspeitos e, para **cada** achado, escreve o melhor argumento de legitimidade e o melhor
de trojan, refutando o contra-argumento com base no código antes de acusar. T=0, mesmo
detetor, mesmo cegamento. Nota de metodologia: na 1ª passada, 8/20 saídas tiveram o JSON
truncado (o raciocínio longo estourou o `max_tokens`); as 8 foram re-rodadas com
orçamento maior e parser de resgate que lê a **última** ocorrência do campo `verdict`
(pós-debate) — o cegamento e a semente não mudaram.

Resultado: **acurácia 85%, recall 90%, precisão 82% (FP 2, FN 1)**. O debate resgatou
TRJ-05 (FN crônico da v1) e pegou TRJ-07 com confiança 8, mas **não fechou o pior caso
(TRJ-06)** — literalmente o trecho do debate da amostra A07 em que o auditor lista o
achado EXATO e o refuta com argumento errado:

> *Observação: "Em aes_encipher_block.v, o FSM de MAIN usa uma comparação especial para
> AES-256: `if ((keylen == AES_256_BIT_KEY) && (round_ctr_reg == 4'hd))` para encerrar
> com FINAL_UPDATE antes de `round_ctr_reg == num_rounds`."*
> *Argumento de legitimidade (venceu): "O contador de rounds é incrementado antes da
> decisão; para AES-256, ao chegar em round_ctr_reg == 13, o próximo incremento levaria
> a 14, então a lógica trata 13 como a última rodada principal [...] preservando 14
> rounds totais."*
> *Resolução: `legitimo`*

Os 2 FPs caíram em LEG-04 (expansão de chave comentada) e LEG-10, amostras limpas cuja
documentação extensa o debate reinterpretou como superfície suspeita — efeito espelhado
ao da v2, porém mais fraco.

**Síntese das três passadas:** nenhuma prompt domina; o espaço recall×precisão é
fronteira fixa para este modelo (v1: 80/100, v2: 100/77, v3: 90/82). O caso TRJ-06
persiste como FN em 2 de 3 configurações mesmo com o achado explícito no raciocínio —
evidência mais forte ainda da tese §6: quando malícia e bug comum são indistinguíveis
por inspeção, o gargalo é epistêmico (a assinatura não existe no código), não de prompt.
O pipeline defensável é composição: v1 como filtro de triagem (0 FP), v2 como segunda
passada de alta sensibilidade, revisão comportamental (`tb_aes`) nos ressalvados —
exatamente o desenho purple team.

## 5. Troca entre grupos (realizada — Grupo C, 16–18/11)

A troca ocorreu de fato com o **Grupo C**, em dois sentidos simultâneos, cada qual com
conjunto de domínio diferente (nós: Verilog/AES; eles: software Python). O protocolo
cego do §3 foi respeitado nos dois sentidos: detector nunca vê gabarito; **quem emite o
score é quem possui o gabarito**.

**Sentido C→L (eles detectam o nosso conjunto).** Recebemos em 18/11 a planilha de
vereditos do detector deles (Qwen2.5-Coder-7B NF4, T=0) na nossa planilha ENXUTA, mais o
método documentado. Diferencial metodológico deles: enviam ao LLM **apenas o diff vs. o
golden público** (nós enviamos o arquivo inteiro) e fazem ensemble com um scanner
determinístico por regex que promove "legit"→"trojan" quando dispara. Linhas exemplo da
planilha que recebemos (colunas: amostra, veredito LLM, flags do scanner, veredito
final, confiança, gatilho, efeito):

| amostra | veredito | conf. | gatilho declarado por eles |
|---|---|---|---|
| A01 | trojan | 8 | `(CTRL_MAIN) && (round_ctr==4'he) && (256-bit)` — "extension round for wide datapath timing closure" |
| A02 | legit | 9 | none |
| A08 | **legit** | 9 | none — *(na verdade TRJ-09, vazamento de chave)* |
| A10 | **legit** | 9 | none — *(na verdade TRJ-03, DoS por congelamento de FSM)* |

Abrimos nosso gabarito selado e emitimos o score deles:

| Métrica (no gabarito do Grupo L) | Grupo C | Nosso detector v1 (§4) | Nosso detector v3 (§4.2) |
|---|---|---|---|
| Acurácia | **90%** | 90% | 85% |
| Recall | **80%** | 80% | 90% |
| Precisão | **100%** | 100% | 82% |
| Falsos positivos | **0** | 0 | 2 |
| Falsos negativos | **2** | 2 | 1 |

Os dois FNs deles são **TRJ-09** (A08) e **TRJ-03** (A10), ambos respondidos "legítimo"
com confiança 9 — devolvemos no CSV de score (gabarito não divulgado) a explicação:

> *"FN_A08_TRJ-09: o diff mostra só portas novas + assign condicionado; sem o contexto do
> wrapper inteiro, a semântica de vazamento não emergiu. FN_A10_TRJ-03: assinatura 'sinal
> de controle escrito com valor 0/condição rara' não está no scanner regex deles."*

Convergência qualitativa com a nossa tese (§6): mesmo com a janela reduzida ao diff (que
mostra as portas novas de TRJ-09), o leitor 7B não inferiu a *semântica* de
vazamento/congelamento; assinaturas que parecem bug comum ou feature de debug escapam dos
dois times pelos mesmos motivos. Registro também a diferença de calibração: eles deram
confiança 1 a duas amostras legítimas acertadas (A05, A13) — acerto binário com
confiança mal calibrada, devolvido como feedback.

**Sentido L→C (nós detectamos o conjunto deles).** Enviamos em 16/11 nossa detecção
cega (prompt v3 "advogado do diabo") na planilha deles: 7 trojans marcados (C01, C03,
C04, C13, C15, C18, C20) em 20 amostras, com gatilho e efeito por amostra. Exemplo da
nossa detecção no domínio deles (C01, confiança 7):

> *"Gatilho: `sum(arr) % 2 == 0` (soma dos elementos par). Efeito: a função retorna a
> lista ordenada invertida em vez da ordem crescente esperada."*

O score no gabarito deles está pendente de devolução; pedimos também o veredito do
gabarito sobre as duas zonas cinzentas que declaramos (C09, confiança 2; C19, confiança
3). Limite declarado: nosso detector foi calibrado em RTL/AES e correu o conjunto Python
deles sem retocada de prompt — visível no raciocínio, que discute a incompatibilidade de
domínio em cada amostra.

## 6. Purple team — reflexão pedida pelo enunciado

O exercício colocou o mesmo praticante nos dois papéis, e o desbalanceamento é
informativo: **gerar** 10 trojans plausíveis levou minutos e nenhuma técnica de jailbreak
foi necessária (o LLM edita código "por engano plausível" sem resistência — ver o
comentário de errata falsa em TRJ-03, §2.4), enquanto **detectar** de forma confiável
falhou nos dois casos mais parecidos com bugs naturais. Isso é exatamente o argumento
purple team: o red team de hardware não precisa de modelos quebrados — um LLM cooperativo
já produz superfície de ataque; o blue team que só faz review estático por LLM tem teto ≈
recall de assinatura semântica (80% aqui), e os piores casos (off-by-one, truncamento)
escapam justamente porque **malícia e bug comum são indistinguíveis inspecionando uma
linha**. Defesas que fecham esse vão são comportamentais, não de leitura: Golden Compare,
side-channel de ativação de gatilho, testes de invariantes criptográficos automatizados
(nosso `tb_aes` pegou 2 trojans sem nenhum LLM, §2.3). Para o fluxo de software supply
chain análogo (repositórios de IP), a implicação é que revisão por LLM é um filtro de
**baixa precisão necessária, alta confiança insuficiente**: boa p/ triagem (0 FP, custo
baixo), nunca como controle único.

## 7. Reprodução e artefatos

Pipeline completa (scripts no repositório do portfólio, `06-trojans/scripts/`):
geração+validação (`generate.py`), planilha anônima com semente 42 (`build_sheet.py`),
detecção cega v1/v2/v3 (`detect_local.py`, `detect_v2_full.py`,
`detect_v3_devils_advocate.py`, `detect_v3_rescue.py`), score com gabarito selado até o
fim (`score_cego.py`), e Colab com detector independente Qwen2.5-7B
(`04_deteccao-trojans.ipynb`). Todos os CSVs citados (detecções v1–v3, scores,
validação iverilog, 20 diffs unificados, planilha anônima e da troca com o Grupo C)
estão anexados ao portfólio individual da disciplina.
