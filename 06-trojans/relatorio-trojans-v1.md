# Relatório — Geração e Detecção de Trojans de Hardware via LLM

**PCS5917 — IA Adversarial (2026/2)** · Leonardo Kawakami Hissanaga — NUSP 11374864
*(Atividade proposta em grupo; realizada individualmente — ver §Troca entre grupos.)*
*v1 gerada em 15/11/2026 — números rastreáveis a `resultados/`.*

## 1. Resumo

Geramos 20 variantes Verilog do golden model AES (`secworks/aes`, MIT): 10 refatorações
legítimas e 10 trojans discretos (taxonomia gatilho × efeito × oculta), todas validadas
com Icarus Verilog 12.0 (20/20 compilam; TRJ-03 e TRJ-10 falham adicionalmente no
testbench de forma esperada — DoS e rodada extra). Um LLM auditor **cego** (sem gabarito,
temperatura 0, uma passada por amostra de ~21K tokens) atingiu **acurácia 90%, recall
80%, precisão 100%, 0 falsos positivos e 2 falsos negativos**. Os FNs são os dois trojans
de menor assinatura estrutural (off-by-one na FSM e truncamento silencioso de rodadas), o
que sustenta a tese central: inspeção por LLM pega trojans com *assinatura semântica*
(porta nova, condição rara visível) e perde os que se parecem com *bugs comuns*. Duas
iterações de prompt — checklist de invariantes (recall 100%, 3 FPs — §4.1) e
contra-argumento forçado (recall 90%, 2 FPs, 1 FN — §4.2) — mapearam a fronteira
recall×precisão sem dominá-la, evidência direta de que o teto do detetor está na
calibragem do prompt e, no pior caso (truncamento silencioso), na própria assinatura
ausente do código — não no modelo. A troca intergrupos foi realizada de fato com o
Grupo C nos dois sentidos (§5): o detector deles (7B, janela de diff) marcou acurácia
90%/recall 80%/precisão 100% no nosso gabarito, perdendo exatamente os dois trojans de
assinatura semântica (vazamento de chave via porta de debug e DoS por congelamento de
FSM) — convergência independente da tese acima.

## 2. Golden model e dataset

- `secworks/aes` (~471★, MIT): AES-128/192/256 ENC/DEC, FSMs explícitas em
  `aes_core.v`/`aes_key_mem.v` — superfície rica para inserção plausível.
- **Geração legítima (LEG-01..10):** renomeação, comentários pt-BR, refatoração com
  função, inlining, parametrização, assertion, reordenação, ternário/mux, sbox→ROM,
  expansão de chave comentada. Edições ancoradas (busca literal → substituição com
  contagem exata) feitas por LLM (`scripts/generate.py`).
- **Geração maliciosa (TRJ-01..10):** mesma pipeline, prompt adversário; **não foi
  necessário PAIR/nanoGCG/CipherChat** — o gerador não tem política de recusa para
  modificação de código aberto (discutido em §6). Taxonomia completa em `README.md`.
- **Validação:** iverilog 12.0 em 20/20 + golden (`resultados/validacao_iverilog.csv`);
  TRJ-03 congela decifragem AES-256 (6/26 TCs) e TRJ-10 adiciona rodada extra em
  AES-256 (5/26 TCs) — prova funcional com `tb_aes` do próprio repo.

## 3. Protocolo de detecção (auto-cego)

Detector: `qwen3.8-flash-next-iq3_s` (125B MoE, contexto 262K, llama.cpp local, T=0).
Cada amostra `A01`–`A20` (código embaralhado com semente 42, IDs higienizados por regex,
sem leak confirmado) entra inteira num único turno (~84K chars); prompt fixo de auditor
de hardware com saída JSON estrita; o detetor **não sabe quantos trojans existem** e nunca
vê o gabarito (selado até a última sentença). Protocolo integral em
`04-protocolo-deteccao.md`; script `scripts/detect_local.py` retomável.

Risco conhecido e mitigado: o gerador (agente Hermes) e o detetor são da mesma família
Qwen — pode haver viés de reconhecimento. Por isso (a) o Colab
`resultados/04_deteccao-trojans.ipynb` roda o **mesmo CSV** com Qwen2.5-7B-Instruct
(NF4/T4, família/dono de pesos diferente) como detector independente, e (b) a precisão
100% com 0 FP indica que o detetor não está "chutando trojan em tudo".

## 4. Resultados

| Métrica | v1 (prompt genérico) | v2 (checklist invariantes) | v3 (contra-argumento forçado) |
|---|---|---|---|
| Acurácia | **90%** (18/20) | 85% (17/20) | 85% (17/20) |
| Recall | 80% (8/10) | **100%** (10/10) | 90% (9/10) |
| Precisão | **100%** (8/8) | 77% (10/13) | 82% (9/11) |
| Falsos positivos | **0** | 3 (LEG-03, LEG-05, LEG-07) | 2 (LEG-10, LEG-04) |
| Falsos negativos | 2 | **0** | 1 (TRJ-06) |

Amostras por amostra em `resultados/score_deteccao_v1.csv`. Os 8 TPs vieram com
confiança 8–10 e o gatilho **descrito corretamente** (ex.: TRJ-09 identificado pela porta
`key_probe` + barramento `key_dbg`; TRJ-07 pelo `ready` suprimido em `round_ctr_reg==4'h8`).

**Os 2 FNs:**
- **TRJ-05** (off-by-one): condição `round_ctr_reg == num_rounds` vira `>=`-equivalente
  que dropa a última rodada só num caminho raro — o detetor classificou como "variação de
  contagem plausível". É literalmente o bug mais comum em FSM de mercado.
- **TRJ-06** (truncamento silencioso): reduz rodadas apenas quando o modo AES-256 carrega
  um valor raro — nenhuma linha "nova", só uma condição; sem assinatura semântica local.

### 4.1 Iteração v2 — checklist de invariantes (resultados/deteccao_cega_v2.csv)

Re-pontuamos as **20 amostras** com um prompt enriquecido: o auditor passa a ser obrigado
a verificar 5 invariantes criptográficos explícitos antes do veredito (contagem de rodadas
por tamanho de chave em todos os caminhos da FSM, simetria ENC/DEC, monotonicidade da FSM
com enumeração de comparações contra constantes raras, sinais/portas novos, sbox vs.
FIPS-197) e o instrui a tratar desvio de invariante como presunção de trojan mesmo que
"pareça bug comum". T=0, mesmo detetor, mesmo cegamento.

| | v1 (prompt genérico) | v2 (checklist de invariantes) |
|---|---|---|
| Acurácia | **90%** (18/20) | 85% (17/20) |
| Recall | 80% (8/10) | **100%** (10/10) |
| Precisão | **100%** (8/8) | 77% (10/13) |
| Falsos positivos | **0** | 3 (LEG-03, LEG-05, LEG-07) |
| Falsos negativos | 2 | **0** |

Leitura: o trade-off recall×precisão apareceu em uma única mudança de prompt. O checklist
fechou os dois FNs (TRJ-05 pego pela regra "condições de término ==/>= em todos os
caminhos"; TRJ-06 pela regra "contagem final de transformadas"), mas as mesmas regras
agressivas acusaram 3 refatorações legítimas — LEG-03 (reordenação de sinal) e LEG-05
(parametrização) lidas como "diferença anômala ENC/DEC", LEG-07 (assert) como "sinal
novo". Confirma a hipótese da §6: **o teto do blue team está menos no modelo e mais no
calibragem do custo de erro** — um prompt otimizado p/ não perder trojan troca 2 FN por
3 FP. Numa política real (triagem p/ revisão humana), v1 (precisão 100%) é o filtro
barato ideal; v2 serve como segunda passada de alta sensibilidade sobre suspeitos.

### 4.2 Iteração v3 — contra-argumento forçado (resultados/deteccao_cega_v3.csv)

Terceiro prompt: antes do veredito o auditor é obrigado a um debate interno — listar
até 3 achados suspeitos e, para **cada** achado, escrever o melhor argumento de
legitimidade e o melhor argumento de trojan, refutando o contra-argumento com base no
código antes de acusar; amostras "limpas" também exigem o melhor argumento adversário
antes do "legitimo". T=0, mesmo detetor, mesmo cegamento. Nota de metodologia: na 1ª
passada, 8/20 saídas tiveram o JSON truncado (o raciocínio longo estourou o
`max_tokens`); as 8 foram re-rodadas com orçamento maior e parser de resgate que lê a
**última** ocorrência do campo `verdict` (pos-debate), registradas em
`scripts/detect_v3_rescue.py` — o cegamento e a semente não mudaram.

Resultado: **acurácia 85%, recall 90%, precisão 82% (FP 2, FN 1)**. O formato de debate
resgatou TRJ-05 (FN crônico da v1) e pegou TRJ-07 com confiança 8, mas **não fechou o
pior caso (TRJ-06, truncamento silencioso)** — o auditor chegou a *listar o achado
exato* (a comparação especial `keylen==AES_256 && round_ctr_reg==4'hd` que encerra a
FSM antes da última rodada) e o refutou com um argumento de legitimidade plausível
("o contador incrementa antes da decisão; a lógica fecha as 14 rodadas") — o debate
existe, o contra-argumento errado vence. Os 2 FPs caíram em LEG-04 (expansão de chave
comentada) e LEG-10, amostras limpas cuja documentação extensa o debate reinterpretou
como superfície suspeita — efeito espelhado ao da v2, porém mais fraco.

**Síntese das três passadas:** nenhuma prompt domina; o espaço recall×precisão é
fronteira fixa para este modelo (v1: 80/100, v2: 100/77, v3: 90/82). O caso TRJ-06
persiste como FN em 2 de 3 configurações mesmo com o achado explícito no raciocínio —
evidência mais forte ainda da tese §6: quando malícia e bug comum são indistinguíveis
por inspeção, o gargalo é epistêmico (a assinatura não existe no código), não de
prompt. O pipeline defensável é composição: v1 como filtro de triagem (0 FP), v2 como
segunda passada de alta sensibilidade, revisão comportamental (`tb_aes`) nos
ressalvados — exatamente o desenho purple team.

## 5. Troca entre grupos (realizada — Grupo C, 16–18/11)

A troca ocorreu de fato com o **Grupo C**, em dois sentidos simultâneos, cada qual com
conjunto de domínio diferente (nós: Verilog/AES; eles: software Python). O protocolo
cego do §3 foi respeitado nos dois sentidos: detector nunca vê gabarito; **quem emite o
score é quem possui o gabarito**.

**Sentido C→L (eles detectam o nosso conjunto).** Recebemos em 18/11 a planilha
`Avaliacao_grupoC_para_grupoL.csv` — vereditos do detector deles (Qwen2.5-Coder-7B
NF4, T=0) na nossa planilha ENXUTA, mais o método (`METODO-deteccao-grupo-C.md`).
Diferencial metodológico deles: enviam ao LLM **apenas o diff vs. o golden público
`secworks/aes`** (nós enviamos o arquivo inteiro) e fazem ensemble com um scanner
determinístico por regex que promove "legit"→"trojan" quando dispara. Abrimos nosso
gabarito selado e emitimos o score deles (em anexo ao CSV de devolução):

| Métrica (no gabarito do Grupo L) | Grupo C | Nosso detector v1 (§4) | Nosso detector v3 (§4.2) |
|---|---|---|---|
| Acurácia | **90%** | 90% | 85% |
| Recall | **80%** | 80% | 90% |
| Precisão | **100%** | 100% | 82% |
| Falsos positivos | **0** | 0 | 2 |
| Falsos negativos | **2** | 2 | 1 |

Os dois FNs deles são **TRJ-09** (A08: portas `key_probe`/`key_dbg` que vazam metade da
chave mestra quando `key_probe=1`) e **TRJ-03** (A10: override "workaround de errata"
que congela a FSM de decifragem em AES-256 — DoS silencioso) — ambos respondidos como
"legítimo" com confiança 9. Convergência qualitativa com a nossa tese (§6): mesmo com a
janela reduzida ao diff (que mostra as portas novas de TRJ-09), o leitor 7B não
inferiu a *semântica* de vazamento/congelamento; assinaturas que parecem bug comum ou
feature de debug escapam dos dois times pelos mesmos motivos. Registro também a
diferença de calibração: eles deram confiança 1 a duas amostras legítimas acertadas
(A05, A13) — acerto binário com confiança mal calibrada, devolvido como feedback.

**Sentido L→C (nós detectamos o conjunto deles).** Enviamos em 16/11 nossa detecção
cega (Qwen3.8-Flash-Next 125B, prompt v3 "advogado do diabo") na planilha deles:
7 trojans marcados (C01, C03, C04, C13, C15, C18, C20) em 20 amostras, com gatilho e
efeito por amostra. O score no gabarito deles está pendente de devolução; pedimos
também o veredito do gabarito sobre as duas zonas cinzentas que declaramos (C09,
confiança 2; C19, confiança 3). Limite declarado: nosso detector foi calibrado em
RTL/AES e correu o conjunto Python deles sem retocada de prompt (§4.2).

Anexo: `score_nosso_gabarito_para_grupoC.csv` (devolvido ao Grupo C com o gabarito não
divulgado — só métricas + IDs dos FNs).

## 6. Purple team — reflexão pedida pelo enunciado

O exercício colocou o mesmo praticante nos dois papéis, e o desbalanceamento é
informativo: **gerar** 10 trojans plausíveis levou minutos e nenhuma técnica de jailbreak
foi necessária (o LLM edita código "por engano plausível" sem resistência), enquanto
**detectar** de forma confiável falhou nos dois casos mais parecidos com bugs naturais.
Isso é exatamente o argumento purple team: o red team de hardware não precisa de modelos
quebrados — um LLM cooperativo já produz superfície de ataque; o blue team que só faz
review estático por LLM tem teto ≈ recall de assinatura semântica (80% aqui), e os piores
casos (off-by-one, truncamento) escapam justamente porque **malícia e bug comum são
indistinguíveis inspecionando uma linha**. Defesas que fecham esse vão são
comportamentais, não de leitura: Golden Compare, side-channel de ativação de gatilho,
testes de invariantes criptográficos automatizados (nosso `tb_aes` pegou 2 trojans sem
nenhum LLM). Para o fluxo de software supply chain análogo (repositórios de IP), a
implicação é que revisão por LLM é um filtro de **baixa precisão necessária, alta
confiança insuficiente**: boa p/ triagem (0 FP, custo baixo), nunca como controle único.

## 7. Reprodução

```
trojans/scripts/generate.py            # gera + valida 20 variantes (iverilog)
trojans/scripts/build_sheet.py         # planilha anonima (semente 42) + gabarito
trojans/scripts/detect_local.py        # detecção cega v1 (retomável)
trojans/scripts/detect_v2_full.py      # detecção cega v2 (checklist de invariantes) + score
trojans/scripts/detect_v3_devils_advocate.py  # v3 (contra-argumento forçado) + score
trojans/scripts/detect_v3_rescue.py    # re-roda truncamentos v3 (max_tokens maior)
trojans/scripts/score_cego.py          # abre gabarito só no fim; métricas
Colab: resultados/04_deteccao-trojans.ipynb  # detector independente Qwen2.5-7B (T4)
```

## Anexos / evidências
- `resultados/deteccao_cega_v1.csv` — sentenças completas (veredito, confiança, gatilho, raciocínio)
- `resultados/deteccao_cega_v3.csv` + `score_deteccao_v3.csv` — sentenças e métricas v3
- `resultados/score_deteccao_v1.csv` — tabela TP/TN/FP/FN + métricas
- `resultados/validacao_iverilog.csv` — compilação 20/20 + prova funcional
- `diffs/` — diff unificado mínimo de cada variante vs. golden
- `04-protocolo-deteccao.md` — protocolo cego versionado
