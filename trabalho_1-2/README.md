# Número por Extenso

Programa que converte um número inteiro entre `0` e `999.999` para sua forma
por extenso, em **português** ou em **inglês**, modelando a conversão de
cada grupo de dígitos como uma **Máquina de Estados Finitos (Máquina de
Mealy)**. Feito para o **Trabalho 1-2** da disciplina
**Autômatos e Linguagens Formais (DCA-3705)** — UFRN, 2026.2.

## Como funciona

O programa recebe um número digitado pelo usuário e devolve sua forma por
extenso, ou informa que a entrada é inválida quando o valor não é um inteiro
entre 0 e 999.999.

A conversão de cada grupo de três dígitos (centena, dezena, unidade) é
modelada como uma máquina de Mealy: os dígitos do grupo são a entrada, os
estados representam a posição dentro do grupo (`CENTENA -> DEZENA -> FIM`)
e, a cada transição, a máquina emite a palavra por extenso correspondente.
O número completo é formado por, no máximo, dois grupos desse tipo — o dos
milhares e o das unidades simples — unidos pela palavra "mil" (pt) ou
"thousand" (en).

Ao rodar o programa, é possível:

- escolher o idioma da saída (`pt` ou `en`)
- digitar um número (ex: `204.328` ou `204328`) e ver o resultado por extenso
- digitar `sair` (pt) ou `exit` (en) para encerrar

## Estrutura de arquivos

```
trabalho_1-2/
├── numero.py
└── README.md
```

| Arquivo | Descrição |
|---|---|
| `numero.py` | Programa principal (validação, conversores PT/EN e loop interativo) |

## Como executar

```bash
python3 numero.py
```

## Formato de entrada

- Inteiro entre `0` e `999.999`, positivo.
- Aceita o ponto como separador de milhar (ex: `204.328` ou `204328`).
- Qualquer outro valor (negativo, decimal, texto, fora do intervalo) é
  tratado como entrada inválida.

## Exemplo de uso

```
$ python3 extenso.py
Escolha o idioma [pt/en]: pt
Digite um número (0 a 999.999), ou 'sair' para encerrar: 204.328
Saída: duzentos e quatro mil, trezentos e vinte e oito.
Digite um número (0 a 999.999), ou 'sair' para encerrar: 11
Saída: onze.
Digite um número (0 a 999.999), ou 'sair' para encerrar: -215
entrada inválida (só respondo se a entrada for um número entre 0 e 999.999).
Digite um número (0 a 999.999), ou 'sair' para encerrar: casa
entrada inválida (só respondo se a entrada for um número entre 0 e 999.999).
Digite um número (0 a 999.999), ou 'sair' para encerrar: sair
```