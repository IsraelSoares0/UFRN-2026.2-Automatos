# Analisador de Símbolos de Expressões Aritméticas

**Atividade:** 3ª Lista de Programação

**Vídeo de apresentação:** _<link do vídeo aqui>_

---

## Descrição

Programa em Python que, usando **expressões regulares** (módulo `re`), analisa uma expressão aritmética e:

- identifica e conta os **símbolos válidos**;
- lista os **símbolos inválidos**;
- ignora espaços em branco entre os símbolos.

O alfabeto válido é:

Σ = { `(`, `)`, `+`, `-`, `*`, `/`, `num` }

| Símbolo | Nome na saída   |
|---------|-----------------|
| `(`     | `PAR_ABERTURA`  |
| `)`     | `PAR_FECHAMENTO`|
| `+`     | `OP_SOMA`       |
| `-`     | `OP_SUBTRACAO`  |
| `*`     | `OP_PRODUTO`    |
| `/`     | `OP_DIVISAO`    |
| número  | `NUMERO`        |

### Definição de número (`num`)

O enunciado define o número como `d*.d*`, onde `d` é um dígito de 0 a 9. Como os exemplos tratam inteiros (como `2`) como número válido, o ponto decimal é opcional. São aceitos:

- inteiros: `2`, `20`
- decimais: `20.3`, `20.`, `.5`

Um ponto isolado (`.`) **não** é um número válido.

### Desafio: notação científica

Além do formato básico, o programa aceita um expoente opcional `[eE][+-]?d+`, como em `10.0e+02` e `9e-1`. Esse modo vem **ativado por padrão** e pode ser desativado com a opção `--basico`.

---

## Requisitos

- Python 3.6 ou superior
- Nenhuma biblioteca externa (usa apenas `re` e `sys` da biblioteca padrão)

---

## Como executar

**Passando a expressão na linha de comando:**

```bash
python analisador_simbolos.py "(20.3 * 2 (4+3))!"
```

**Modo interativo** (digite expressões; linha vazia encerra):

```bash
python analisador_simbolos.py
```

**Desativando a notação científica:**

```bash
python analisador_simbolos.py --basico "9e-1"
```

---

## Exemplos

**Entrada:** `(20.3 + 2)`

```
Símbolos válidos (01 PAR_ABERTURA, 01 PAR_FECHAMENTO, 01 OP_SOMA, 02 NUMERO) Símbolos inválidos (não há símbolos inválidos)
```

**Entrada:** `(20.3 * 2 (4+3))!`

```
Símbolos válidos (02 PAR_ABERTURA, 02 PAR_FECHAMENTO, 01 OP_SOMA, 01 OP_PRODUTO, 04 NUMERO) Símbolos inválidos (01 símbolo inválido - !)
```

**Entrada (desafio):** `10.0e+02 + 9e-1`

```
Símbolos válidos (01 OP_SOMA, 02 NUMERO) Símbolos inválidos (não há símbolos inválidos)
```

**Entrada:** `3 - 2 / x @ 4.`

```
Símbolos válidos (01 OP_SUBTRACAO, 01 OP_DIVISAO, 03 NUMERO) Símbolos inválidos (02 símbolos inválidos - x @)
```

**Entrada com `--basico`:** `9e-1`

```
Símbolos válidos (01 OP_SUBTRACAO, 02 NUMERO) Símbolos inválidos (01 símbolo inválido - e)
```

---

## Como a solução funciona

### 1. Regex mestra com grupos nomeados

Cada tipo de símbolo é um grupo nomeado `(?P<NOME>...)`, e todos são unidos por `|` em uma única expressão regular. O `re.finditer` percorre a entrada da esquerda para a direita e o atributo `m.lastgroup` informa qual grupo casou em cada posição.

### 2. Ordem dos grupos

A ordem das alternativas é importante, pois o `re` escolhe a primeira que casa:

1. `NUMERO` vem primeiro, para que o sinal do expoente em `9e-1` seja consumido pelo número e não contado como operador.
2. Em seguida vêm parênteses e operadores.
3. `ESPACO` (`\s+`) é casado e descartado, o que implementa a regra de ignorar espaços em branco.
4. `INVALIDO` (`.`) fica por último e captura qualquer caractere que não casou com nada antes.

### 3. Expressões regulares dos números

```python
NUM_BASICO     = r"(?:\d+\.?\d*|\.\d+)"
NUM_CIENTIFICO = NUM_BASICO + r"(?:[eE][+-]?\d+)?"
```

Se o expoente estiver incompleto (por exemplo `2e` ou `2e+`), o expoente opcional não casa. O número `2` é reconhecido normalmente e o `e` é tratado como símbolo inválido.

### 4. Contagem e saída

- Um dicionário conta as ocorrências de cada tipo válido, exibidas sempre na mesma ordem (a dos exemplos do enunciado), apenas quando a contagem é maior que zero.
- Os símbolos inválidos são guardados em uma lista, na ordem em que aparecem.
- A função `formatar_saida` monta o texto final, com contagens de dois dígitos (`01`, `02`...) e o singular/plural correto de "símbolo inválido".

---

## Estrutura do código

| Elemento              | Função                                                              |
|-----------------------|---------------------------------------------------------------------|
| `NUM_BASICO`, `NUM_CIENTIFICO` | Padrões regex para os formatos de número                   |
| `montar_regex(cientifico)`     | Monta a regex mestra, com ou sem notação científica        |
| `analisar(expressao, cientifico)` | Retorna a contagem dos válidos e a lista de inválidos   |
| `formatar_saida(contagem, invalidos)` | Gera a string de saída no formato do enunciado      |
| `main()`              | Trata os argumentos de linha de comando e o modo interativo         |

---

## Limitações

- O programa faz **análise léxica**: reconhece os símbolos, mas **não valida a sintaxe** da expressão. Por exemplo, `(3 + ` é lido como símbolos válidos, embora seja uma expressão malformada.
- Sinais unários (como o `-` em `-5`) são contados como `OP_SUBTRACAO`, seguido de `NUMERO`.
- Caracteres inválidos consecutivos (como `abc`) são contados individualmente.

---

## Arquivos

- `analisador_simbolos.py` – código-fonte da solução
- `README.md` – este documento