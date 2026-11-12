#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py — Gera as 20 variantes (10 legítimas + 10 trojans) a partir do
golden model secworks/aes, aplicando edições pontuais (diff mínimo rastreável),
gravando meta.json e diffs/ em unified diff.

PCS5917 — IA Adversarial (USP) — Atividade "Geração e Detecção de Trojans"
Gerador: agente LLM local Hermes (qwen3.8-flash-next). Data: 2026-11-09.
"""
import json
import difflib
import shutil
from datetime import date
from pathlib import Path

RAIZ = Path("/opt/data/projetos/ia-adversarial/trojans")
GOLDEN = RAIZ / "golden-aes" / "src" / "rtl"
HOJE = date.today().isoformat()
MODELO = "agente LLM local Hermes (qwen3.8-flash-next, IQ3_XS, dual RTX 3090)"

ARQS = ["aes.v", "aes_core.v", "aes_encipher_block.v", "aes_decipher_block.v",
        "aes_key_mem.v", "aes_sbox.v", "aes_inv_sbox.v"]

MAGIC = "128'h6a09e667f3bcc909bbed77ed391a1a16"

# ---------------------------------------------------------------------------
# Especificações. Cada variante: id, label, categoria/tipo, descricao,
# alvos = [(arquivo, [(busca, substituição, contagem_esperada), ...]), ...]
# ---------------------------------------------------------------------------

def r(busca, subst, n=1):
    return (busca, subst, n)

LEGIT = [
    dict(
        id="LEG-01",
        label="Renomeacao de parametros de numero de rodadas",
        categoria="renomeacao de sinais",
        arquivo_alvo="aes_encipher_block.v",
        descricao=("Renomeia os localparams AES128_ROUNDS/AES256_ROUNDS para "
                   "AES128_ROUND_COUNT/AES256_ROUND_COUNT em aes_encipher_block.v "
                   "(refatoracao cosmetica, sem mudanca funcional)."),
        alvos=[("aes_encipher_block.v", [
            r("localparam AES128_ROUNDS = 4'ha;", "localparam AES128_ROUND_COUNT = 4'ha;"),
            r("localparam AES256_ROUNDS = 4'he;", "localparam AES256_ROUND_COUNT = 4'he;"),
            r("num_rounds = AES256_ROUNDS;", "num_rounds = AES256_ROUND_COUNT;"),
            r("num_rounds = AES128_ROUNDS;", "num_rounds = AES128_ROUND_COUNT;"),
        ])],
    ),
    dict(
        id="LEG-02",
        label="Comentarios explicativos em portugues",
        categoria="documentacao",
        arquivo_alvo="aes.v",
        descricao=("Adiciona cabecalho de documentacao em portugues no topo do "
                   "wrapper aes.v descrevendo a interface APB e o datapath AES. "
                   "Somente comentarios."),
        alvos=[("aes.v", [
            r("`default_nettype none",
              "// ---------------------------------------------------------------------\n"
              "// Variante LEG-02 (PCS5917): documento de suporte em portugues.\n"
              "// Este modulo e o wrapper de nivel superior do core AES da secworks:\n"
              "// expoe um barramento APB e instancia aes_core, que contem a\n"
              "// expansao de chaves (aes_key_mem), os blocos de cifra/decifra\n"
              "// (aes_encipher_block / aes_decipher_block) e as S-boxes\n"
              "// (aes_sbox / aes_inv_sbox) compartilhadas.\n"
              "// ---------------------------------------------------------------------\n"
              "`default_nettype none"),
        ])],
    ),
    dict(
        id="LEG-03",
        label="Refatoracao da funcao shiftrows",
        categoria="refatoracao",
        arquivo_alvo="aes_encipher_block.v",
        descricao=("Refatora a funcao shiftrows() de aes_encipher_block.v trocando a"
                   "\nconcatenacao direta por atribuicoes intermediarias com\n"
                   "comentario didatico. Funcao logicamente identica."),
        alvos=[("aes_encipher_block.v", [
            r("      ws0 = {w0[31 : 24], w1[23 : 16], w2[15 : 08], w3[07 : 00]};\n"
              "      ws1 = {w1[31 : 24], w2[23 : 16], w3[15 : 08], w0[07 : 00]};\n"
              "      ws2 = {w2[31 : 24], w3[23 : 16], w0[15 : 08], w1[07 : 00]};\n"
              "      ws3 = {w3[31 : 24], w0[23 : 16], w1[15 : 08], w2[07 : 00]};",
              "      // Shiftrows: linha r desloca r posicoes para a esquerda.\n"
              "      ws0 = {w0[31 : 24], w1[23 : 16], w2[15 : 08], w3[07 : 00]}; // linha 0: sem shift\n"
              "      ws1 = {w1[31 : 24], w2[23 : 16], w3[15 : 08], w0[07 : 00]}; // linha 1: shift 1\n"
              "      ws2 = {w2[31 : 24], w3[23 : 16], w0[15 : 08], w1[07 : 00]}; // linha 2: shift 2\n"
              "      ws3 = {w3[31 : 24], w0[23 : 16], w1[15 : 08], w2[07 : 00]}; // linha 3: shift 3"),
        ])],
    ),
    dict(
        id="LEG-04",
        label="Inline da funcao addroundkey",
        categoria="otimizacao/inline",
        arquivo_alvo="aes_encipher_block.v",
        descricao=("Remove a funcao auxiliar addroundkey() de aes_encipher_block.v e\n"
                   "inlineda a operacao XOR diretamente nos tres sinais de bloco.\n"
                   "Reducao de nivel de abstracao, comportamento identico."),
        alvos=[("aes_encipher_block.v", [
            r("  function automatic [127 : 0] addroundkey(input [127 : 0] data, input [127 : 0] rkey);\n"
              "    begin\n"
              "      addroundkey = data ^ rkey;\n"
              "    end\n"
              "  endfunction // addroundkey\n\n", ""),
            r("      addkey_init_block  = addroundkey(block, round_key);\n"
              "      addkey_main_block  = addroundkey(mixcolumns_block, round_key);\n"
              "      addkey_final_block = addroundkey(shiftrows_block, round_key);",
              "      // AddRoundKey = XOR direto com a round key (funcao inlineada).\n"
              "      addkey_init_block  = block           ^ round_key;\n"
              "      addkey_main_block  = mixcolumns_block ^ round_key;\n"
              "      addkey_final_block = shiftrows_block  ^ round_key;"),
        ])],
    ),
    dict(
        id="LEG-05",
        label="Parameterizacao das constantes de rodadas",
        categoria="parametrizacao",
        arquivo_alvo="aes_encipher_block.v",
        descricao=("Converte os localparams de contagem de rodadas em parameters\n"
                   "sobrescritaveis (AES128_ROUNDS_P / AES256_ROUNDS_P) em\n"
                   "aes_encipher_block.v, permitindo reconfiguracao na sintese."),
        alvos=[("aes_encipher_block.v", [
            r("  localparam AES128_ROUNDS = 4'ha;\n  localparam AES256_ROUNDS = 4'he;",
              "  // Parameters sobrescritaveis na sintese (variante parametrizada).\n"
              "  parameter AES128_ROUNDS_P = 4'ha;\n"
              "  parameter AES256_ROUNDS_P = 4'he;"),
            r("num_rounds = AES256_ROUNDS;", "num_rounds = AES256_ROUNDS_P;"),
            r("num_rounds = AES128_ROUNDS;", "num_rounds = AES128_ROUNDS_P;"),
        ])],
    ),
    dict(
        id="LEG-06",
        label="Assertion de range do contador de rodadas",
        categoria="insercao de assertiva",
        arquivo_alvo="aes_key_mem.v",
        descricao=("Adiciona, dentro de `ifndef SYNTHESIS, uma assertiva em\n"
                   "aes_key_mem.v que sinaliza erro de simulacao se round_ctr_reg\n"
                   "ultrapassar o numero maximo de rodadas (14)."),
        alvos=[("aes_key_mem.v", [
            r("    end // key_mem_ctrl\nendmodule // aes_key_mem",
              "    end // key_mem_ctrl\n\n"
              "/* verilator lint_off WIDTH */\n"
              "`ifndef SYNTHESIS\n"
              "    // Assertion legítima (LEG-06): o contador nunca pode ultrapassar\n"
              "    // o numero maximo de rodadas suportado pela memoria de chaves.\n"
              "    // (asserção imediata p/ compatibilidade com Icarus Verilog)\n"
              "    always @(posedge clk) begin\n"
              "      if (reset_n && (round_ctr_reg > AES_256_NUM_ROUNDS))\n"
              "        $error(\"round_ctr_reg fora do range permitido.\");\n"
              "    end\n"
              "`endif\n"
              "/* verilator lint_on WIDTH */\n"
              "endmodule // aes_key_mem"),
        ])],
    ),
    dict(
        id="LEG-07",
        label="Reordenacao das portas do modulo sbox",
        categoria="reordenacao de portas",
        arquivo_alvo="aes_sbox.v",
        descricao=("Reordena a lista de portas de aes_sbox.v (saida new_sboxw antes\n"
                   "da entrada sboxw) com comentario de estilo. Instancias usam\n"
                   "conexao por nome, entao nao ha mudanca funcional."),
        alvos=[("aes_sbox.v", [
            r("module aes_sbox(\n                input wire [31 : 0]  sboxw,\n                output wire [31 : 0] new_sboxw\n               );",
              "module aes_sbox(\n"
              "                // Estilo: saidas declaradas antes das entradas (LEG-07).\n"
              "                output wire [31 : 0] new_sboxw,\n"
              "                input  wire [31 : 0] sboxw\n"
              "               );"),
        ])],
    ),
    dict(
        id="LEG-08",
        label="Reescrita do seletor de rodadas como operador ternario",
        categoria="otimizacao de mux",
        arquivo_alvo="aes_encipher_block.v",
        descricao=("Substitui o if/else que escolhe num_rounds em\n"
                   "aes_encipher_block.v por um unico operador ternario\n"
                   "(reescreve o mux de configuracao, mesma logica)."),
        alvos=[("aes_encipher_block.v", [
            r("      if (keylen == AES_256_BIT_KEY)\n"
              "        begin\n"
              "          num_rounds = AES256_ROUNDS;\n"
              "        end\n"
              "      else\n"
              "        begin\n"
              "          num_rounds = AES128_ROUNDS;\n"
              "        end",
              "      // Mux de configuracao reescrito como atribuicao ternaria (LEG-08).\n"
              "      num_rounds = (keylen == AES_256_BIT_KEY) ? AES256_ROUNDS : AES128_ROUNDS;"),
        ])],
    ),
    dict(
        id="LEG-09",
        label="S-box convertida para estilo ROM procedural",
        categoria="movimento de implementacao (sbox p/ ROM)",
        arquivo_alvo="aes_sbox.v",
        descricao=("Converte as 256 atribuicoes contínuas `assign sbox[..]` de\n"
                   "aes_sbox.v para uma ROM procedural descrita num unico bloco\n"
                   "always @* (array vira reg). Conteudo byte-a-byte identico."),
        alvos=[("aes_sbox.v", [
            r("  wire [7 : 0] sbox [0 : 255];", "  reg [7 : 0] sbox [0 : 255];"),
            r("  assign sbox[", "  always @* begin\n", 0),  # placeholder, tratado abaixo
        ]),],
    ),
    dict(
        id="LEG-10",
        label="Reagrupamento comentado da expansao de chaves",
        categoria="refatoracao com comentarios",
        arquivo_alvo="aes_key_mem.v",
        descricao=("Reagrupa com comentarios explicativos o bloco round_key_gen de\n"
                   "aes_key_mem.v (palavras w0..w7, rcon, rotação), sem alterar a\n"
                   "logica de expansao de chaves AES-128/AES-256."),
        alvos=[("aes_key_mem.v", [
            r("      // Extract words and calculate intermediate values.\n"
              "      // Perform rotation of sbox word etc.\n",
              "      // --- Bloco A: extrai as 8 palavras da chave anterior (LEG-10) ---\n"
              "      // w0..w3 vem de prev_key0_reg; w4..w7 vem de prev_key1_reg.\n"
              "      // --- Bloco B: rcon, word rotacionada e XORs intermediarios ---\n"
              "      // (rotw = RotWord aplicado a saida da sbox; rconw = Rcon alinhado)\n"),
        ])],
    ),
]

TROJANS = [
    dict(
        id="TRJ-01",
        label="Substituicao sutil de byte na ultima rodada condicionada a round key magica",
        tipo_logico="harm conditioned (substituicao de 1 byte)",
        gatilho="comparacao de round_key == 128'h6a09e667f3bcc909bbed77ed391a16 no FINAL_UPDATE",
        dano="um byte do ciphertext final e invertido (XOR 8'hff) somente para essa round key; "
             "com chave normal o circito e bit-exato, logo testes de vetor padrao nao pegam",
        ocultacao="inserido dentro do case já existente; constante magica parece um valor de teste; "
                  "gatilho depende da chave secreta, raro por construcao",
        arquivo_alvo="aes_encipher_block.v",
        descricao="No ramo FINAL_UPDATE, se round_key for igual a constante magica, aplica XOR 0xff no byte mais significativo do bloco final.",
        alvos=[("aes_encipher_block.v", [
            r("        FINAL_UPDATE:\n"
              "          begin\n"
              "            block_new    = addkey_final_block;\n"
              "            block_w0_we  = 1'b1;\n"
              "            block_w1_we  = 1'b1;\n"
              "            block_w2_we  = 1'b1;\n"
              "            block_w3_we  = 1'b1;\n"
              "          end",
              "        FINAL_UPDATE:\n"
              "          begin\n"
              "            block_new    = addkey_final_block;\n"
              "            block_w0_we  = 1'b1;\n"
              "            block_w1_we  = 1'b1;\n"
              "            block_w2_we  = 1'b1;\n"
              "            block_w3_we  = 1'b1;\n"
              "            if (round_key == " + MAGIC + ")\n"
              "              block_new[127 : 120] = block_new[127 : 120] ^ 8'hff;\n"
              "          end"),
        ])],
    ),
    dict(
        id="TRJ-02",
        label="XOR da round key com constante secreta quando round_key assume valor raro",
        tipo_logico="backdoor / oraculo de recuperacao de chave",
        gatilho="round_key == constante magica dentro da funcao addroundkey",
        dano="para esse valor rarissimo de round key, o texto cifra com key^K; atacante que "
             "observa ciphertext com plaintext conhecido pode confirmar uma candidata da "
             "ultima round key, reduzindo drasticamente o espaco de busca da chave secreta",
        ocultacao="uma linha dentro de funcao de 5 linhas; K = ~magic parece lixo aleatorio; "
                  "so dispara para 1 entre 2^128 round keys",
        arquivo_alvo="aes_encipher_block.v",
        descricao="A funcao addroundkey aplica XOR com constante secreta K apenas quando round_key coincide com valor magico de 128 bits.",
        alvos=[("aes_encipher_block.v", [
            r("  function automatic [127 : 0] addroundkey(input [127 : 0] data, input [127 : 0] rkey);\n"
              "    begin\n"
              "      addroundkey = data ^ rkey;\n"
              "    end\n"
              "  endfunction // addroundkey",
              "  function automatic [127 : 0] addroundkey(input [127 : 0] data, input [127 : 0] rkey);\n"
              "    reg [127 : 0] k_eff;\n"
              "    begin\n"
              "      k_eff = rkey;\n"
              "      if (rkey == " + MAGIC + ")\n"
              "        k_eff = rkey ^ 128'h95f619980c4326f544129812c6e5e7e9; // K = ~magic\n"
              "      addroundkey = data ^ k_eff;\n"
              "    end\n"
              "  endfunction // addroundkey"),
        ])],
    ),
    dict(
        id="TRJ-03",
        label="Trava da FSM do decifrador em contador de rodadas raro",
        tipo_logico="DoS por trava de FSM (write-enable inibido)",
        gatilho="keylen == AES_256_BIT_KEY, dec_ctrl_reg == CTRL_MAIN e round_ctr_reg == 4'hd (rodada 13 de 14 do AES-256)",
        dano="o write-enable da FSM de decifragem e inibido em CTRL_MAIN na rodada 13 do AES-256: "
             "a maquina nunca sai de CTRL_MAIN, o bloco nunca fica ready e a decifragem trava PARA "
             "SEMPRE nesse modo; AES-128 nao e afetado",
        ocultacao="override apos o endcase mascarado de workaround de errata de silicio (SE-1142); "
                  "reusa estados e sinais existentes; apenas um bit de write-enable muda",
        arquivo_alvo="aes_decipher_block.v",
        descricao="Apos o endcase da FSM decifrador, um override rotulado workaround de errata zera "
                  "dec_ctrl_we quando keylen=256, CTRL_MAIN e round_ctr_reg=13: a FSM congela e a "
                  "decifragem AES-256 nunca completa (DoS silencioso).",
        alvos=[("aes_decipher_block.v", [
            r("      endcase // case (dec_ctrl_reg)\n    end // decipher_ctrl",
              "      endcase // case (dec_ctrl_reg)\n\n"
              "      /* Workaround metastability on late round count (erratum SE-1142) */\n"
              "      if ((dec_ctrl_reg == CTRL_MAIN) && (keylen == AES_256_BIT_KEY)\n"
              "          && (round_ctr_reg == 4'hd))\n"
              "        begin\n"
              "          dec_ctrl_we = 1'b0;\n"
              "        end\n"
              "    end // decipher_ctrl"),
        ])],
    ),
    dict(
        id="TRJ-04",
        label="Flip de 1 bit em uma entrada da S-box publica",
        tipo_logico="alteracao de tabela (substituicao sutil de 1 entrada)",
        gatilho="nenhum (sempre ativo), mas so afeta blocos que contenham os bytes 0x01/0x7d",
        dano="sbox[8'h01] muda de 8'h7c para 8'h7d (1 bit): cifra fica incorreta apenas para "
             "entradas raras, dificultando deteccao por testes de conformidade que usam poucos vetores",
        ocultacao="erro de 1 bit parece defeito de fabricacao/typo em tabela de 256 linhas; "
                  "troca e quase simetrica (7c<->7d parecem vizinhos plausiveis)",
        arquivo_alvo="aes_sbox.v",
        descricao="A entrada sbox[8'h01] da tabela AES publica e alterada de 0x7c para 0x7d — flip de um bit.",
        alvos=[("aes_sbox.v", [
            r("assign sbox[8'h01] = 8'h7c;", "assign sbox[8'h01] = 8'h7d;"),
        ])],
    ),
    dict(
        id="TRJ-05",
        label="Off-by-one na condicao de termino da expansao de chaves",
        tipo_logico="off-by-one em condicao de encerramento",
        gatilho="round_ctr_reg == 4'he (14), so alcancavel quando keylen=256 bits",
        dano="a comparacao == por <= faz o contador ultrapassar o numero de rodadas em um ciclo "
             "extra para AES-256, gravando round key corrompida no indice 15 fora do range da "
             "memoria; a FSM pode nunca alcancar CTRL_DONE (hang) em certas configuracoes",
        ocultacao="mudanca de um simbolo (= para <=) em condicao de limite; parece correcao de "
                  "boundary-condition legítima; so AFETA o caminho AES-256, raramente testado",
        arquivo_alvo="aes_key_mem.v",
        descricao="A condicao 'round_ctr_reg == num_rounds' da FSM key_mem_ctrl vira '<=', causando um ciclo extra e overflow do contador no modo AES-256.",
        alvos=[("aes_key_mem.v", [
            r("            if (round_ctr_reg == num_rounds)",
              "            if (round_ctr_reg <= num_rounds)"),
        ])],
    ),
    dict(
        id="TRJ-06",
        label="Truncamento de rodada so no modo AES-256 (off-by-one discreto)",
        tipo_logico="reducao silenciosa de forca (off-by-one)",
        gatilho="keylen == AES_256_BIT_KEY e round_ctr_reg == 4'hd (rodada 13 de 14)",
        dano="no modo AES-256 a cifra encerra na rodada 13 em vez de 14: produz ciphertexts com "
             "uma rodada a menos (ataque de reducao de rodadas trivial). AES-128 permanece correto, "
             "entao toda a suíte de testes padrao passa",
        ocultacao="injetado como ramo if adicional dentro de CTRL_MAIN ja existente; o valor 4'hd "
                  "parece um ajuste de pipeline; invisivel para testes apenas com chave de 128 bits",
        arquivo_alvo="aes_encipher_block.v",
        descricao="Em CTRL_MAIN, quando keylen=256 e round_ctr_reg==13, o bloco antecipa FINAL_UPDATE e encerra uma rodada antes.",
        alvos=[("aes_encipher_block.v", [
            r("            if (round_ctr_reg < num_rounds)\n"
              "              begin\n"
              "                update_type   = MAIN_UPDATE;\n"
              "                enc_ctrl_new  = CTRL_SBOX;\n"
              "                enc_ctrl_we   = 1'b1;\n"
              "              end\n"
              "            else",
              "            if (round_ctr_reg < num_rounds)\n"
              "              begin\n"
              "                if ((keylen == AES_256_BIT_KEY) && (round_ctr_reg == 4'hd))\n"
              "                  begin\n"
              "                    update_type  = FINAL_UPDATE;\n"
              "                    ready_new    = 1'b1;\n"
              "                    ready_we     = 1'b1;\n"
              "                    enc_ctrl_new = CTRL_IDLE;\n"
              "                    enc_ctrl_we  = 1'b1;\n"
              "                  end\n"
              "                else\n"
              "                  begin\n"
              "                    update_type   = MAIN_UPDATE;\n"
              "                    enc_ctrl_new  = CTRL_SBOX;\n"
              "                    enc_ctrl_we   = 1'b1;\n"
              "                  end\n"
              "              end\n"
              "            else"),
        ])],
    ),
    dict(
        id="TRJ-07",
        label="Prorrogacao do sinal ready por contador raro (delay off)",
        tipo_logico="timing trojan / negacao de servicio temporizada",
        gatilho="round_ctr_reg == 4'h8 no momento em que o bloco ficaria pronto",
        dano="o sinal ready externamente visível e suprimido quando o contador de rodadas vale "
             "0x8, atrasando/derrubando handshakes do protocolo; em integracoes com timeout, "
             "causa falha de comunicacao intermitente",
        ocultacao="uma AND-gate em assign no topo do modulo com comentario de 'power management "
                  "mode'; o valor raro so ocorre num instante especifico da operacao",
        arquivo_alvo="aes_encipher_block.v",
        descricao="Novo fio pronto_raro e pronto_ok; o assign de 'ready' passa a ser pronto_ok & ~pronto_raro, suprimindo o handshake quando round_ctr_reg==8.",
        alvos=[("aes_encipher_block.v", [
            r("  assign round     = round_ctr_reg;\n"
              "  assign sboxw     = muxed_sboxw;\n"
              "  assign new_block = {block_w0_reg, block_w1_reg, block_w2_reg, block_w3_reg};\n"
              "  assign ready     = ready_reg;",
              "  wire pronto_raro;\n"
              "  wire pronto_ok;\n\n"
              "  // Ready qualified for power management mode.\n"
              "  assign pronto_raro = ((round_ctr_reg == 4'h8) & ready_reg);\n"
              "  assign pronto_ok   = ready_reg;\n\n"
              "  assign round     = round_ctr_reg;\n"
              "  assign sboxw     = muxed_sboxw;\n"
              "  assign new_block = {block_w0_reg, block_w1_reg, block_w2_reg, block_w3_reg};\n"
              "  assign ready     = pronto_ok & ~pronto_raro;"),
        ])],
    ),
    dict(
        id="TRJ-08",
        label="AND da habilitacao da FSM com condicao rara de chave",
        tipo_logico="inibicao de write-enable por gatilho raro",
        gatilho="round_ctr_reg == 4'h7 e round_key[127:120] == 8'ha5",
        dano="a habilitacao de escrita da FSM de decifragem e forçada a 0 num ciclo critico, "
             "congelando o estado interno da maquina (trava da operacao de decifragem) para keys "
             "com esse prefixo raro",
        ocultacao="parece gating de economia de energia ('test power savings mode'); combina dois "
                  "sinais internos ja existentes, sem fio novo",
        arquivo_alvo="aes_decipher_block.v",
        descricao="Em reg_update, 'dec_ctrl_we' e ANDado com ~(raro): quando round_ctr_reg==7 e o byte mais alto da round key vale 0xa5, a FSM nunca mais e escrita.",
        alvos=[("aes_decipher_block.v", [
            r("          if (dec_ctrl_we)\n"
              "            dec_ctrl_reg <= dec_ctrl_new;",
              "          if (dec_ctrl_we & ~((round_ctr_reg == 4'h7) & (round_key[127 : 120] == 8'ha5)))\n"
              "            // test power savings mode\n"
              "            dec_ctrl_reg <= dec_ctrl_new;"),
        ])],
    ),
    dict(
        id="TRJ-09",
        label="Backdoor de vazamento de chave por pino auxiliar",
        tipo_logico="canal encoberto / key leaking por pino",
        gatilho="key_probe assertedido pelo integrador (pino 'nao usado' amarrado a 0 no SoC)",
        dano="expoe 128 bits da chave secreta diretamente em um pino fisico adicional; se o pino "
             "for roteado para um pad externo, header de debug ou placa de teste, a chave vaza sem "
             "qualquer operacao criptografica",
        ocultacao="pino com nome plausivel de debug/verificacao (key_probe) que integraores "
                  "tendem a deixar flutuando ou amarrar; comentarios de 'silicon debug' mascaram a intencao",
        arquivo_alvo="aes_key_mem.v",
        descricao="Adiciona input 'key_probe' e output 'key_dbg' a aes_key_mem; quando key_probe=1, key_dbg espelha key[255:128] (metade da chave mestra).",
        alvos=[("aes_key_mem.v", [
            r("                   input wire    [3 : 0] round,",
              "                   input wire             key_probe, // silicon debug hook\n"
              "                   input wire    [3 : 0]  round,"),
            r("                   output wire [31 : 0]  sboxw,\n"
              "                   input wire  [31 : 0]  new_sboxw",
              "                   output wire [31 : 0]  sboxw,\n"
              "                   input wire  [31 : 0]  new_sboxw,\n"
              "                   output wire [127 : 0] key_dbg // probe output"),
            r("  assign round_key = tmp_round_key;\n"
              "  assign ready     = ready_reg;\n"
              "  assign sboxw     = tmp_sboxw;",
              "  assign round_key = tmp_round_key;\n"
              "  assign ready     = ready_reg;\n"
              "  assign sboxw     = tmp_sboxw;\n"
              "  // key probe output for silicon debug.\n"
              "  assign key_dbg   = (key_probe) ? key[255 : 128] : 128'h0;"),
        ])],
    ),
    dict(
        id="TRJ-10",
        label="Extensao de rodadas alem da especificacao em modo AES-256",
        tipo_logico="corrupcao silenciosa de saida (rodada extra com MixColumns)",
        gatilho="keylen == AES_256_BIT_KEY, enc_ctrl_reg == CTRL_MAIN e round_ctr_reg == 4'he "
                "(rodada final do AES-256, onde o golden aplica FINAL_UPDATE; inalcancavel no AES-128)",
        dano="na rodada final do AES-256, em vez de FINAL_UPDATE a FSM aplica MAIN_UPDATE: o "
             "MixColumns da ultima rodada corroi o AddRoundKey e o ciphertext sai silenciosamente "
             "errado (o bloco ainda completa, em 15 rodadas); AES-128 nao e afetado",
        ocultacao="override apos o endcase rotulado extension round for wide datapath timing "
                  "(SE-1108); reusa update_type e transicoes ja existentes; um contador de 4 bits "
                  "decide a anomalia",
        arquivo_alvo="aes_encipher_block.v",
        descricao="Apos o endcase da FSM cifrador, um override em CTRL_MAIN com round_ctr_reg=14 e "
                  "keylen=256 troca FINAL_UPDATE por MAIN_UPDATE e reencaminha para CTRL_SBOX: "
                  "rodada extra com MixColumns => ciphertext AES-256 errado e silencioso.",
        alvos=[("aes_encipher_block.v", [
            r("      endcase // case (enc_ctrl_reg)\n    end // encipher_ctrl",
              "      endcase // case (enc_ctrl_reg)\n\n"
              "      /* extension round for wide datapath timing closure (SE-1108) */\n"
              "      if ((enc_ctrl_reg == CTRL_MAIN) && (round_ctr_reg == 4'he)\n"
              "          && (keylen == AES_256_BIT_KEY))\n"
              "        begin\n"
              "          update_type  = MAIN_UPDATE;\n"
              "          enc_ctrl_new = CTRL_SBOX;\n"
              "          enc_ctrl_we  = 1'b1;\n"
              "        end\n"
              "    end // encipher_ctrl"),
        ])],
    ),
]


def apply_edits(src_text, edits, vid, fname):
    """Aplica (busca, substituição, n) em ordem; exige contagem exata."""
    txt = src_text
    for (busca, subst, n) in edits:
        cnt = txt.count(busca)
        if n == 0:
            # n=0 é usado apenas no caso especial LEG-09 (tratado fora)
            raise RuntimeError(f"{vid}/{fname}: marcador n=0 nao suportado aqui")
        if cnt != n:
            raise RuntimeError(
                f"{vid}/{fname}: trecho nao encontrado {n}x (achado {cnt}x): {busca[:60]!r}")
        txt = txt.replace(busca, subst)
    return txt


def fix_leg09(txt):
    """Converte as 256 atribuicoes `assign sbox[..]` de aes_sbox.v para uma
    ROM procedural descrita num unico bloco always @* (array vira reg).
    Conteudo byte-a-byte identico. Implementacao por regex ancorado."""
    import re
    pat = re.compile(r"^  assign (sbox\[8'h[0-9a-fA-F]{2}\] = 8'h[0-9a-fA-F]{2};)$", re.M)
    matches = list(pat.finditer(txt))
    assert len(matches) == 256, f"esperava 256 assigns, achei {len(matches)}"
    first, last = matches[0], matches[-1]
    body = txt[first.start():last.end()]
    new_body = pat.sub(lambda m: "    " + m.group(1), body)
    new_body = ("  always @*\n    begin : sbox_rom\n" + new_body +
                "\n    end // sbox_rom")
    return txt[:first.start()] + new_body + txt[last.end():]


def write_variant(kind, spec):
    base = RAIZ / kind / spec["id"]
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)

    textos = {}
    for f in ARQS:
        textos[f] = (GOLDEN / f).read_text()

    for (fname, edits) in spec["alvos"]:
        if spec["id"] == "LEG-09" and fname == "aes_sbox.v":
            # tratamento especial: reconversao estrutural
            src = textos[fname].replace("  wire [7 : 0] sbox [0 : 255];",
                                        "  reg [7 : 0] sbox [0 : 255];")
            textos[fname] = fix_leg09(src)
        else:
            textos[fname] = apply_edits(textos[fname], edits, spec["id"], fname)

    for f in ARQS:
        (base / f).write_text(textos[f])

    # diffs vs golden
    ddir = RAIZ / "diffs"
    ddir.mkdir(exist_ok=True)
    for f in ARQS:
        g = (GOLDEN / f).read_text().splitlines(keepends=True)
        v = textos[f].splitlines(keepends=True)
        diff = list(difflib.unified_diff(
            g, v, fromfile=f"golden-aes/src/rtl/{f}",
            tofile=f"{kind}/{spec['id']}/{f}"))
        if diff:
            (ddir / f"{spec['id']}__{f}.diff").write_text("".join(diff))

    # meta.json
    meta = {
        "id": spec["id"],
        "tipo": "legitimo" if kind == "legitimate" else "trojan",
        "label": spec["label"],
        "data_geracao": HOJE,
        "modelo_llm": MODELO,
        "base": "secworks/aes golden-aes @ MIT (clonado localmente)",
        "arquivo_alvo": spec["arquivo_alvo"],
        "descricao": spec["descricao"],
    }
    if kind == "legitimate":
        meta["categoria"] = spec["categoria"]
    else:
        for k in ("tipo_logico", "gatilho", "dano", "ocultacao"):
            meta[k] = spec[k]
    (base / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    return base


def main():
    import subprocess
    IVL = "/opt/data/projetos/ia-adversarial/.tools/iverilog-root/usr/bin/iverilog"
    ok, falhas = 0, []
    for kind, specs in (("legitimate", LEGIT), ("trojans", TROJANS)):
        for spec in specs:
            base = write_variant(kind, spec)
            try:
                r = subprocess.run(
                    [IVL, "-t", "null"] + [str(base / a) for a in ARQS],
                    capture_output=True, text=True, timeout=60)
                if r.returncode != 0:
                    raise RuntimeError(r.stderr.strip().splitlines()[0][:160])
                print(f"[OK]      {spec['id']} gerada e validada (iverilog)")
                ok += 1
            except Exception as e:
                msg = str(e).splitlines()[-1] if str(e) else repr(e)
                falhas.append((spec["id"], msg[:200]))
                print(f"[FALHOU]  {spec['id']}: {msg[:120]}")
    print(f"\nGeradas/validadas inline: {ok}/20; falhas: {len(falhas)}")
    for f in falhas:
        print("  -", f)


if __name__ == "__main__":
    main()
