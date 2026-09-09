# Máquina de Estados Finitos (FSM)

Simulador genérico de uma máquina de estados finitos (Máquina de Moore), feito para a **1ª Lista de Programação** da disciplina **Autômatos e Linguagens Formais (DCA-3705)** — UFRN, 2026.2.

## Como funciona

O programa lê a definição da máquina (conjuntos de entrada `I`, saída `O`, estados `S`, tabela de transição `TE` e vetor de saída `VS`) a partir de um arquivo texto, e depois permite simular a máquina interativamente:

- digitar um único símbolo de entrada (ex: `1`)
- digitar uma palavra inteira (ex: `0111010`) e ver o caminho percorrido até o resultado final
- digitar `r` para resetar a máquina ao estado inicial
- digitar `sair` para encerrar

## Estrutura de arquivos

```
trabalho_1-1/
├── fsm.py
├── README.md
└── configuracao/
    ├── maquina1.txt
    └── maquina2.txt
```

| Arquivo | Descrição |
|---|---|
| `fsm.py` | Programa principal |
| `configuracao/maquina1.txt` | Máquina de exemplo do enunciado |
| `configuracao/maquina2.txt` | Segunda máquina de teste (verificador de paridade) |

## Como executar

```bash
python fsm.py configuracao/maquina1.txt
python fsm.py configuracao/maquina2.txt
```

## Formato do arquivo de configuração

```
ni=1              # I = {0, ..., ni}
no=1              # O = {0, ..., no}
ns=2              # S = {0, ..., ns}
estado_inicial=0

TE:
1 0               # TE[estado][entrada] -> próximo estado (uma linha por estado)
2 1
2 0

VS:
0 1 1             # saída associada a cada estado (uma posição por estado)
```

## Exemplo de uso

```
$ python3 fsm.py configuracao/maquina1.txt
  t0: estado = s0  |  saída = 0
t0 - entrada> 01101
  Processando a palavra '01101':
  Ciclo   Entrada   Estado    Saída
  t0      --        s0        0
  t1      0         s1        1
  t2      1         s1        1
  t3      1         s1        1
  t4      0         s2        1
  t4      1         s0        0
  -> Estado final: s0   Saída final: 0
```