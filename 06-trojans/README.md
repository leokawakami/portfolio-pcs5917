# Atividade: Geração e Detecção de Trojans — PCS5917 IA Adversarial (2026)

**Estudante:** Leonardo Kawakami Hissanaga — NUSP 11374864
*(Atividade proposta para grupos; realizada individualmente, ver seção "Troca entre grupos".)*

## Golden model

[`secworks/aes`](https://github.com/secworks/aes) (MIT, ~471★) — implementação Verilog completa de AES-128/192/256 (ENC/DEC), modular e didática, com FSMs explícitas em `aes_core.v`/`aes_key_mem.v` — superfície rica para inserção plausível. Clonado em `golden-aes/` (pinned 2026-11-09).

## Método de geração

- **LLM gerador:** agente LLM local (Qwen3.8-Flash-Next via Hermes, perfil orquestrador) — especificado no enunciado da disciplina ("utilize um LLM de sua escolha"); prompts e especificações por variante em `scripts/generate.py` (edições ancoradas: busca literal → substituição, com contagem exata obrigatória).
- **Validação:** TODAS as 20 amostras compilam com **Icarus Verilog 12.0** (`iverilog -t null`, mesmo binário usado pelo desafio de compilação; ver `resultados_gen.log`) — 20/20 OK, incluindo o golden.
- **Rastreabilidade:** diff unificado mínimo vs. golden em `diffs/`, e `meta.json` por variante (descrição, arquivo-alvo, e no caso de trojan: tipo lógico, gatilho, dano, ocultação).

## As 20 amostras

10 legítimas (`legitimate/LEG-01..10`): renomeação, comentários pt-BR, refatoração com função, inlining, parametrização, assertion (imediata, compatível Icarus), reordenação, ternário/mux, sbox→ROM, expansão de chave comentada.

10 trojans (`trojans/TRJ-01..10`), taxonomia estilo Trojan Taxonomy/TrustHub (gatilho × efeito × oculta):

| ID | Tipo lógico | Gatilho | Efeito |
|---|---|---|---|
| TRJ-01 | substituição condicional de dados | byte raro da chave | byte-flip na última rodada |
| TRJ-02 | XOR com constante secreta | valor raro da round key | enfraquecimento da saída |
| TRJ-03 | estado morto em FSM | transição rara em `CTRL_*` | trava o pipeline |
| TRJ-04 | modificação de tabela | 1 endereço da sbox | subtileza criptográfica |
| TRJ-05 | off-by-one | contagem de término | dropa última rodada |
| TRJ-06 | truncamento seletivo | modo AES-256 raro | reduz rodadas silenciosamente |
| TRJ-07 | delay por contador | contador raro | negação de serviço |
| TRJ-08 | AND de controle | sinal raro (`update_type`) | bloqueio de escrita |
| TRJ-09 | backdoor de observação | pino `key_probe`=1 | key-leak (metade da chave mestra em `key_dbg`) |
| TRJ-10 | bypass de pipeline | condição rara | pula transformada |

Todos discretos: gatilhos por valores raros (comparações específicas), sem alterar comportamento no caso comum — os diffs são mínimos e plausíveis de "engano de revisão".

## Planilhas (`resultados/`)

- `planilha_anonima.csv` / aba **ANONIMA** do `planilha_trojans.xlsx` → para trocar (código HDL + id A01..A20 embaralhado com semente 42; IDs originais anonimizados por regex; verificado: sem leak de LEG-/TRJ-)
- `gabarito.csv` → única fonte do gabarito rotulado (nunca enviar). O `planilha_trojans.xlsx` contém **apenas** a aba ANONIMA (a aba GABARITO foi removida em 10/11 para eliminar risco de leak — revisão PCS5917)

## Troca entre grupos (adaptado — estudante individual)

Sem grupo próprio: proposto ao professor (1) receber a planilha anonimizada de um grupo para eu rodar a **detecção via LLM** e devolver score (acurácia, recall, FP/FN), e/ou (2) enviar a minha para detecção de ida e vinda. Enquanto não definido, a detecção rodará em **modo auto-cego**: o detetor LLM recebe a planilha anonimizada SEM o gabarito (o gabarito só é aberto para o score ao final — protocolo em `04-protocolo-deteccao.md`, a gerar junto do Colab de detecção).

## Desafio de compilação (opcional) — FEITO

Todas as 20 + golden compilam com Icarus Verilog 12.0. (Simulação completa com testbenches `src/tb/` e síntese com yosys: não executadas — documentado como fora do escopo do mínimo.)
