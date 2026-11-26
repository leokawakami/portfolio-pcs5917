# LLM como Juiz na Medição de ASR: Dois Juízes Automáticos, Um Protocolo de Calibração e a Coleta Humana Pendente

**Leonardo Kawakami Hissanaga — NUSP 11374864** — PCS5917 (Poli/USP), 2026/2.
Relatório final da atividade "LLM como Juiz" (entrega atrasada ao portfólio). PDF SBC coluna dupla em 4 páginas (`relatorio-llm-como-juiz-final.pdf`, compilado 26/11, 0 erros); fonte LaTeX canônica no mesmo nome `.tex`.

Uso de IA generativa declarado (Código de Conduta da SBC, Art. 2º, III); nunca como autoria.

## Estrutura
- **Resumo + Introdução** — juiz como objeto de estudo; contribuições (inventário de ASRs por juiz, evidência de não-comparabilidade, protocolo de calibração).
- **Metodologia** — planilha única (146 ataques/5 atividades); Juiz A (Mistral-7B rubrica binária, Aula 7/NB3, 165/165); Juiz B (juiz vendorizado PAIR 1–10, 150 iterações); protocolo humano-juiz (31+18 linhas, cegamento, semente 42, kappa Landis & Koch).
- **Resultados** — Tabelas 1–3 (planilha; ASR Juiz A: manual 12,0 / SR 0,0 / IA 2,0; Base64 0,0; ASR Juiz B: 10,0% IC Wilson 1,8–40,4).
- **Limitações (Seção 4)** — declaração explícita: 0/31 linhas com rótulo humano; nenhum kappa/ASR humano reportado; ASRs permanecem não calibrados. Hayashi et al. 2026 (12,7% discordância, viés de falsos negativos) => ASR de juiz único tende a ser piso, não teto.
- **Conclusão** — ASR é função do juiz; painel multi-juiz + ancoragem humana como rota; integridade: ausência de rótulos como resultado declarado.

## Reprodução
```bash
export PATH=/opt/data/home/.TinyTeX/bin/x86_64-linux:$PATH
latexmk -pdf relatorio-llm-como-juiz-final.tex   # 4 paginas, 0 erros
```
