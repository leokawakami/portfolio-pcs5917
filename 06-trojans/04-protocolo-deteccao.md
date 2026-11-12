# Protocolo de detecção de trojans via LLM — modo auto-cego

**PCS5917 — IA Adversarial · Atividade: Geração e Detecção de Trojans (prazo 18/11 14h)**
Estudante: Leonardo Kawakami Hissanaga — NUSP 11374864 (individual; troca com outro grupo pendente de definição com o professor).

## Objetivo
Avaliar até que ponto um LLM, sem nenhum conhecimento prévio dos rótulos, consegue
identificar amostras maliciosas (trojans de hardware) entre 20 variantes Verilog de um
golden model AES (`secworks/aes`), distinguindo-as de refatorações legítimas.

## Insumos
- `planilha_anonima.csv` — 20 amostras `A01`–`A20` embaralhadas (semente 42), com apenas
  `amostra_id` + `codigo_hdl` (todos os `.v` da variante concatenados com marcador
  `// === arquivo.v ===`). IDs originais (`LEG-*`/`TRJ-*`) removidos por regex — ver
  verificação de leak no `build_sheet.py`.
- `gabarito.csv` — rótulos (`legitimo`/`trojan`) + descrição do autor. **Selado** até o
  momento da pontuação.

## Detector
- Modelo: `qwen3.8-flash-next-iq3_s` (endpoint local llama.cpp, n_ctx 262144) — o mesmo
  engine que serviu de gerador seria enviesado (autodetecção), por isso na versão final o
  detector deve ser um modelo **distinto do gerador**; nesta iteração local documentamos o
  risco. Paralelamente existe o Colab `04_deteccao-trojans.ipynb` com **Qwen2.5-7B-Instruct
  (NF4, T4)**, que é independente do gerador e serve como segundo detector.
- Estratégia de janela: o projeto completo (~21K tokens por amostra) é analisado **por
  turno por arquivo `.v`** com caderno de notas acumulado (mesmo desenho do Colab 04), ou
  em turno único quando a janela do detector comporta a amostra inteira (caso do endpoint
  local de 262K).
- Temperatura 0 (determinístico), um turno por amostra, sem iteração corretiva.

## Prompt do detetor (fixo, versionado em `scripts/detect_local.py`)
Papel: auditor sênior de confiança de hardware. Recebe **uma** variante do projeto AES com
o enunciado de que cada variante pode ser refatoração legítima OU conter um trojan discreto
(gatilho raro + comportamento malicioso condicionado). Deve responder JSON estrito:
`{"verdict": "legitimo"|"trojan", "confidence": 1-10, "suspect_files": [...], "trigger": "...", "effect": "...", "reasoning": "..."}`.
O prompt não menciona quantos trojans existem (nada de "10 de 20") para não ancorar o
detetor na proporção real.

## Pontuação (aberta apenas após as 20 sentenças saírem, sem re-rodar nenhuma)
- Acurácia, recall (sensibilidade p/ trojan), precisão, falsos positivos (legítimo acusado)
  e falsos negativos (trojan perdido) — métricas pedidas no enunciado da atividade.
- Reportado por amostra em `resultados/deteccao_cega_v1.csv` (detecção + gabarito
  lado a lado, para o outro grupo auditar).

## Iterações (desafio do enunciado)
- v1: turno único com a amostra inteira (janela longa).
- v2 (se FP/FN altos): turno por arquivo com caderno de notas + segunda passada só nos
  arquivos suspeitos.
- Interações de ida e vinda com outro grupo ficam reservadas para quando o professor
  definir a logística de troca.

## Ameaças à validade
- Detetor = mesmo family do gerador → viés de reconhecimento. Mitigação: Colab 04 com
  Qwen2.5-7B (família diferente) rodando o mesmo CSV.
- Diffs mínimos por construção (gerados com âncora literal) → favorecem falsos negativos;
  é um resultado esperado e será discutido no relatório (relevância purple team).
