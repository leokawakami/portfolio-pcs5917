# PCS5917 – IA Adversarial

## Portfólio Individual

**Aluno:** Leonardo Kawakami Hissanaga (NUSP 11374864)
**Disciplina:** PCS5917 – IA Adversarial
**Período:** 3º período de 2026
**Instituição:** Universidade de São Paulo – Escola Politécnica
**Professor:** Victor Takashi Hayashi

## 1. Objetivo do Portfólio

Este portfólio reúne as principais atividades, estudos, experimentos e reflexões desenvolvidos ao longo da disciplina **PCS5917 – IA Adversarial**.

O objetivo é documentar individualmente o processo de aprendizagem sobre:

- notícias e referências científicas sobre IA Adversarial (Aula 1);
- fundamentos de Inteligência Artificial e Segurança (Aula 2);
- aplicação de IA em cibersegurança (Aula 3);
- ataques adversariais contra sistemas de IA (Aulas 4 e 5);
- avaliação de ataques e uso de LLMs como juiz (Aula 6);
- defesas em Large Language Models (Aula 7).

Os experimentos realizados durante as aulas devem ser complementados por registros individuais, notebooks, respectivos resultados e referências bibliográficas (citações).

## 2. Organização do Repositório

**IMPORTANTE**: somente branch main (demais branches serão desconsideradas na correção).
Faça o desenvolvimento incremental com **commits semanais**, pois a evolução durante as semanas também é critério de avaliação.
Organize seu README focando em ser objetivo, com evidências de resultados e citações às referências utilizadas.

```text
.
├── README.md                       ← este arquivo (índice + resultados-chave)
├── 00-roteiro/                     ← roteiro do portfólio e planejamento
├── 01-aula2-manuais/               ← ataques manuais EN/PT (Aula 2)
├── 02-aula4-nanogcg/               ← nanoGCG (Aula 4): notebook + CSV de resultados
├── 03-pair/                        ← ataque automático PAIR (piloto)
├── 04-defesas/                     ← defesas de prompt: estudo + notebooks + ASR
│   ├── 01-estudo-defesas.md
│   └── (CSVs de ataques/ASR — subir aqui)
├── 05-portfolio-metodo/            ← método do portfólio + planilha única consolidada
│   └── planilha-unica-ataques.csv
└── LICENSE
```

## 3. Resultados-chave (evidências)

| Experimento | Modelo alvo | Método | Resultado principal |
|---|---|---|---|
| Jailbreaks manuais EN/PT (20 casos, Aula 2) | MiniCPM5-2B | Manual + avaliação humana | EN: 7 obedeceu / 1 parcial / 2 recusou; PT: 4 obedeceu / 1 parcial / 5 recusou |
| nanoGCG × 11 templates (Aula 4) | MiniCPM5-2B | nanoGCG (sufixo adversarial, loss 1.59→0.27) | Baseline: 3/11 parciais; com GCG: 1/11 parcial, 10/11 recusou (pessoas com filtro de <think>) |
| PAIR piloto (10 comportamentos × 5 streams) | Llama-2-7B-Chat | PAIR (atacante Qwen3.5 + juiz automático) | ASR do juiz = **10.0%** (1/10 comportamentos; IC 95%: 1.8–40.4%) |
| 10 jailbreaks × 5 tarefas × 3 condições (Aula 7) | Qwen2.5-7B-Instruct (NF4) | Manual + juiz Mistral-7B | ASR: baseline **12.0%**, Intention Analysis **2.0%**, Self-Reminder **0.0%** |
| Ataque Base64 × 5 tarefas × 3 condições (Aula 7) | Qwen2.5-7B-Instruct (NF4) | Encoding (ofuscação) | ASR **0.0%** em todas as condições (0/15) |

Detalhes, protocolos e limitações em cada pasta (`01-` a `04-`). A consolidação por autoria/método está em [`05-portfolio-metodo/planilha-unica-ataques.csv`](05-portfolio-metodo/planilha-unica-ataques.csv).

## Disclaimer de Uso Ético

Este repositório foi desenvolvido exclusivamente para fins acadêmicos e de pesquisa no contexto da disciplina **PCS5917 – IA Adversarial**.

Alguns experimentos, datasets, prompts, códigos e resultados apresentados podem conter **conteúdo potencialmente malicioso**, incluindo exemplos de jailbreaks, payloads e outras técnicas de ataque. Esses materiais são disponibilizados para fins de estudo, análise, reprodução controlada e compreensão de mecanismos de ataque e defesa.

Os conteúdos devem ser utilizados somente em **ambientes autorizados e controlados**, sem direcionamento a sistemas, modelos, redes, dispositivos ou usuários de terceiros. A reprodução dos experimentos deve respeitar as políticas de uso das ferramentas e os termos das plataformas utilizadas.

O conteúdo deste repositório **não constitui recomendação ou incentivo à realização de atividades maliciosas**. O objetivo é compreender riscos de segurança, desenvolver métodos de avaliação e contribuir para o desenvolvimento de sistemas de Inteligência Artificial mais seguros.
