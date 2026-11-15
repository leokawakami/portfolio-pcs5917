# WCIA 2026 — Estudo do Workshop (fatos extraídos do site oficial)

**Disciplina:** PCS5917 — Inteligência Artificial Adversarial (2026/2), Prof. Victor Takashi Hayashi
**Autor:** Leonardo Kawakami Hissanaga — NUSP 11374864 (trabalho individual)
**Data da coleta:** 15/11/2026
**Fonte primária:** página oficial do WCIA no site do SBSeg 2026 — <https://www.sbseg2026.uff.br/workshops/wcia/> (carregada integralmente em 15/11/2026; todos os fatos abaixo saem dessa página, salvo indicação).

---

## 1. O que é o WCIA 2026

O **Workshop de Cibersegurança em Inteligência Artificial (WCIA)** é um workshop do **SBSeg 2026** (Simpósio Brasileiro em Segurança da Informação e de Sistemas Computacionais), realizado na **UFF (Universidade Federal Fluminense)**. É organizado sob a CESEG da **SBC (Sociedade Brasileira de Computação)**, que é a realização do evento.

- **Coordenação do WCIA:** Victor Hayashi (USP), Oscar Paiva (Bradesco), Diego Kreutz (UNIPAMPA), Rodrigo Sanches Miani (UFU). *(Seção "Coordenação" da página oficial.)*
- **Coordenação Geral do SBSeg 2026:** Dianne Scherly Varela de Medeiros (UFF), Diogo Menezes Ferrazani Mattos (UFF). **Coordenação da CESEG:** Marcos Simplicio (USP), Diego Kreutz (UNIPAMPA).
- **Escopo declarado (seção "Apresentação"):** reunir pesquisadores e profissionais para discutir *"fundamentos, métodos e técnicas experimentais voltados à análise, exploração e mitigação dessas vulnerabilidades, com ênfase em avaliação empírica, reprodutibilidade e cenários realistas"*. Objetivos: (i) fomentar pesquisa em segurança e privacidade em IA; (ii) promover avaliação experimental de ataque/defesa em cenários realistas; (iii) estimular colaboração academia–indústria; (iv) discutir desafios e tendências.
- Observação relevante para a disciplina: o prof. **Victor Takashi Hayashi** (PCS5917) é coordenador do WCIA e aparece como autor de dois artigos aceitos no próprio workshop ("AI, Fill This Form..." e "Diferenciação de Ataques em Português e em Inglês...").

## 2. Tópicos de interesse (seis blocos, transcritos da seção "Tópicos de Interesse")

1. **Ataques e exploração de vulnerabilidades:** modelagem de ameaças em sistemas de IA; exploração de vulnerabilidades em modelos (envenenamento de dados, evasão, backdoors, extração de modelos, membership inference, distillation); ataques a modelos generativos/LLMs (prompt injection, jailbreak, prompt leakage); ataques a modelos multimodais; ataques a visão computacional; ataques a supply chain de IA; red teaming de modelos e sistemas de IA.
2. **Defesa, robustez e mitigação:** robustez em pipelines de treinamento e inferência; detecção/mitigação de ataques adversariais; integração ataque–defesa em IA adversarial; hardening de sistemas LLM (fine-tuning seguro, RAG seguro); monitoramento contínuo e detecção de anomalias em produção.
3. **Sistemas e engenharia de IA:** segurança em pipelines de IA (DevSecOps, MLOps, LLMOps); segurança de sistemas multiagentes; observabilidade de sistemas baseados em IA em produção.
4. **Privacidade e proteção de dados:** privacidade em ML (differential privacy, anonimização); aprendizado federado seguro.
5. **Avaliação, métricas e reprodutibilidade:** métricas, benchmarks e metodologias de avaliação em IA; testbeds, datasets e ambientes experimentais; ferramentas, frameworks e artefatos reprodutíveis.
6. **Interpretação, governança e aplicações:** interpretabilidade/XAI para análise de modelos; aspectos éticos, legais e regulatórios (LGPD, GDPR); aplicações práticas e estudos de caso.

> Nota: o bloco 5 ("Avaliação, métricas e reprodutibilidade") é diretamente relevante à atividade desta disciplina — um protocolo de revisão é, ele mesmo, uma metodologia de avaliação.

## 3. Instruções de submissão (seção "Instruções de Submissão")

- Idioma: **português ou inglês**; formato **estritamente o template SBC de uma coluna** — ZIP oficial: <https://www.sbc.org.br/wp-content/uploads/2024/07/modelosparapublicaodeartigos.zip>.
- **Artigos completos:** até **8 páginas** (corpo do artigo ≤ 6 páginas + 2 páginas adicionais para referências e apêndices).
- **Artigos curtos:** até **4 páginas** (corpo ≤ 3 páginas + 1 página adicional para referências e apêndices); destinam-se a *trabalhos em andamento ou propostas, incluindo position papers*.
- Processo de revisão: **double blind** (sem identificação de autoria nem de revisores/instituições) — *"a SUBMISSÃO DEVE SER ANÔNIMA"*.
- Submissão exclusivamente eletrônica pelo **JEMS3 da SBC**: <https://jems3.sbc.org.br/wcia2026>, somente em **PDF**.
- Publicação: anais estendidos do SBSeg na **SBC-OpenLib (SOL)** <https://sol.sbc.org.br> (acesso aberto). Aceitação requer **inscrição de pelo menos um autor no SBSeg 2026** e **apresentação oral** no evento.
- **Datas:** registro/submissão 27/07/2026; notificação 10/08/2026; versão final 14/08/2026. *(O prazo de 02/12 da disciplina para o artigo do Leonardo é, portanto, posterior ao ciclo real do WCIA 2026 — o artigo serve de alvo didático para a atividade de revisão.)*
- **Apresentação no evento:** artigo curto = 6 min no total (máx. 4 min de fala + 2 min de perguntas); artigo completo = 11 min (máx. 8 + 3).

## 4. Política de uso de IA generativa (seção "Uso de Inteligência Artificial Generativa")

A página do WCIA **não reproduz o texto da política**; ela remete ao **Código de Conduta da SBC**: <https://sol.sbc.org.br/index.php/indice/conduta> (verificado em 15/11/2026). O trecho normativo aplicável é o **Art. 2º, III** do "Código de Conduta para Autores em Publicações da SBC" (Porto Alegre, 28/02/2024), citação verbatim:

> "Uso de Inteligência Artificial (IA) Generativa: a utilização de ferramentas e tecnologias de IA Generativa para geração de conteúdos, na escrita e/ou revisão do conteúdo de artigos, deve ser declarada explicitamente no trabalho. A declaração pode ocorrer na Seção de Agradecimentos, na metodologia ou em uma seção definida especificamente para este fim, de acordo com o template adotado, e deve listar as ferramentas e descrever onde foram empregadas, por exemplo, textos, tabelas, gráficos, citações, etc. Essas ferramentas não podem ser listadas como autores de um artigo. O uso de tais ferramentas não exime os autores da responsabilidade sobre todo o seu conteúdo, inclusive no caso de ser identificado plágio."

Outros pontos do mesmo código relevantes à revisão: **Art. 1º** (plágio, autoplágio e submissão múltipla como condutas antiéticas) e **Art. 2º, I** (recomendação de declarar disponibilidade pública de código/dados para reprodutibilidade — fundamenta a dimensão "reprodutibilidade" do nosso protocolo).

**Implicação para o revisor:** a política vincula *autores* (declaração obrigatória, IA não é autora, responsabilidade permanece humana). Para o *revisor*, o protocolo desta disciplina adota simetria: uso de IA generativa na própria revisão deve ser declarado (ver `protocolo-revisao.md` §5).

## 5. Critérios de avaliação publicados?

A página **não publica um formulário nem critérios explícitos de avaliação** (não há seção "reviewer guidelines"). Os únicos indícios oficiais sobre o processo decisório estão na seção "Estatísticas gerais do WCIA 2026":

- 48 submissões (47 avaliadas): 37 completos (12 aceitos / 24 rejeitados / 1 retirado) e 11 curtos (4 aceitos / 7 rejeitados). **Taxa de aceitação: 33,3% geral; 32,4% completos; 36,4% curtos.**
- 45 membros do Comitê de Programa; **159 atribuições, 144 revisões concluídas**; *"Todos os artigos avaliados receberam pelo menos 3 revisões independentes."*
- Os editores computaram **"média ponderada das avaliações (WAvg)"** — 2 artigos superaram WAvg > 8,0 — evidência de decisão **baseada em scoring ponderado**, o que valida a construção de um formulário com pesos (ver `formulario-avaliacao.md`).

> **Limitação documentada:** como o WCIA 2026 não publica rubrica de revisão, o protocolo desta disciplina é justificado pela literatura de peer review (ver `protocolo-revisao.md` §2) e calibrado nas pistas oficiais acima (≥3 revisões, score ponderado, escopo temático). A estatística "WAvg > 8,0" sugere escala final na casa de 0–10.

## 6. Artigos curtos aceitos (referência de "tamanho-alvo" do que o WCIA aceita)

Da seção "Artigos Aceitos → ARTIGOS CURTOS" (mesma URL):

1. **Além da Segurança do Modelo: Prontidão Institucional para a Adoção Segura de IA no Setor Público** — Ribeiro; Carvalho; Moraes (INSS/UnB).
2. **Adversarial Attacks as a Diagnostic Tool for a Mining Detection Network in the Brazilian Legal Amazon** — Grupioni; Santos; Cugnasca; Almeida (USP).
3. **From Implicit Trust to Continuous Verification: A Position on the Authorization of AI Agents in Production Services** — Araujo; Quincozes; Mansilha (UNIPAMPA).
4. **Diferenciação de Ataques em Português e em Inglês: Análise de Experimento sobre as Barreiras Linguísticas no Alinhamento de LLMs** — Ferreira; Hayashi (USP).

## 7. Fontes utilizadas neste documento

| # | Fato | URL | Como verificado |
|---|------|-----|-----------------|
| S1 | Todo o escopo, tópicos, datas, instruções, estatísticas, programação e artigos aceitos do WCIA 2026 | <https://www.sbseg2026.uff.br/workshops/wcia/> | web_extract em 15/11/2026 (página completa) |
| S2 | Política de IA generativa da SBC (Art. 2º, III, verbatim) e condutas antiéticas | <https://sol.sbc.org.br/index.php/indice/conduta> | web_extract em 15/11/2026 |
| S3 | Template SBC | <https://www.sbc.org.br/wp-content/uploads/2024/07/modelosparapublicaodeartigos.zip> | link publicado em S1 |
| S4 | Sistema de submissão JEMS3 | <https://jems3.sbc.org.br/wcia2026> | link publicado em S1 |

Nenhuma informação deste documento veio de edição anterior do WCIA; tudo é da página do **WCIA 2026**, exceto o código de conduta da SBC (documento geral de 2024, vigente, indicado pelo próprio WCIA).
