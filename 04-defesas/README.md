# 04 – Aula 7: Defesas a Nível de Prompt vs. Ataques

## O que foi feito
Três notebooks executados em Colab (GPU T4, 04/11) sobre o **estudo de caso IEEE 11595604** (Hayashi et al., *DeepSeek Under Attack*, IEEE Access 2026):

1. **Notebook 1** — 150 respostas: 5 tarefas maliciosas × 10 jailbreaks manuais (DAN, AIM, AntiGPT, EvilConfidant, Grandma, Hypothetical, DevMode, OppositeDay…) × 3 condições (baseline, Self-Reminder, Intention Analysis).
2. **Notebook 2** — ataque de **ofuscação Base64** × 5 tarefas × 3 condições.
3. **Notebook 3** — **consolidação com LLM-como-juiz**: une manual + encoded e calcula ASR por (família × tarefa × defesa).

Além disso: **estudo documentado das defesas** (`01-estudo-defesas.md`, neste diretório) — mecânica, templates exatos e correção bibliográfica (Self-Reminder = Xie et al., *Nature Machine Intelligence* 5(12):1486–1496, 2023; Intention Analysis = Zhang et al., COLING 2025, arXiv:2401.06561).

## Método
Defesas **sem treino**, só no prompt: **Self-Reminder** (encapsula a query com lembrete de responsabilidade antes e depois) e **Intention Analysis** (pede ao modelo identificar a intenção da query antes de responder). Geração determinística (T=0, seed 42, NF4). Avaliação dupla: regex de recusa (NB1) e **juiz automático Mistral-7B-Instruct-v0.3** (NF4) com rubrica label 0/1 (NB3) — números abaixo usam o juiz.

## Modelo
- **Alvo:** Qwen2.5-7B-Instruct (NF4, T4)
- **Juiz:** Mistral-7B-Instruct-v0.3 (NF4)

## Resultados-chave (juiz, ASR %)
| Ataque | Baseline | Self-Reminder | Intention Analysis |
|---|---|---|---|
| Manual (50 respostas) | **12.0%** (6/50) | **0.0%** (0/50) | **2.0%** (1/50) |
| Base64 encoded (15 respostas) | 0.0% | 0.0% | 0.0% |

- **Self-Reminder zerou o ASR** dos ataques manuais; IA reduziu de 12→2%.
- Base64 sozinho não teve sucesso em nenhuma condição (0/15) neste alvo.
- Por tarefa (baseline): FakeNews e Phishing 20%, EatGlass e BlackMail 10%, SQLInjection 0%.
- Regex de recusa (NB1, consistente com o juiz): none 74% / SR 70% / IA 60% de recusa.

## Arquivos
- Estudo: `01-estudo-defesas.md` (aqui)
- CSVs: _placeholder_ — `manual_attacks.csv`, `encoded_attacks.csv`, `asr_by_task.csv` (a subir via release ZIP).
