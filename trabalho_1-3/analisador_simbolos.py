"""
DCA-3705 - Autômatos e Linguagens Formais
3a Lista de Programação - Questão 1

Identifica símbolos válidos e inválidos em uma expressão aritmética
usando expressões regulares (módulo re do Python).

Alfabeto válido: Σ = { (, ), +, -, *, /, num }
Número válido (d*.d*): dígitos, com parte decimal opcional.
Desafio: notação científica (ex.: 10.0e+02, 9e-1), ativada por padrão.
"""

import re
import sys

# --- Definição dos padrões -------------------------------------------------

# Número básico (d*.d*): "20", "20.3", "20.", ".5"  (um "." sozinho NÃO é número)
NUM_BASICO = r"(?:\d+\.?\d*|\.\d+)"

# Número com notação científica: mantissa + expoente opcional [eE][+-]?d+
NUM_CIENTIFICO = NUM_BASICO + r"(?:[eE][+-]?\d+)?"


def montar_regex(cientifico: bool = True) -> re.Pattern:
    """Monta a regex mestra com um grupo nomeado por tipo de símbolo.

    A ordem importa: NUMERO vem antes de OP_SUBTRACAO/OP_SOMA para que
    o sinal do expoente (1e-3) seja consumido pelo número, e INVALIDO
    fica por último, capturando qualquer caractere restante.
    """
    num = NUM_CIENTIFICO if cientifico else NUM_BASICO
    padrao = "|".join([
        rf"(?P<NUMERO>{num})",
        r"(?P<PAR_ABERTURA>\()",
        r"(?P<PAR_FECHAMENTO>\))",
        r"(?P<OP_SOMA>\+)",
        r"(?P<OP_SUBTRACAO>-)",
        r"(?P<OP_PRODUTO>\*)",
        r"(?P<OP_DIVISAO>/)",
        r"(?P<ESPACO>\s+)",       # espaços em branco são ignorados
        r"(?P<INVALIDO>.)",       # qualquer outro caractere é inválido
    ])
    return re.compile(padrao)


# Ordem de exibição dos símbolos válidos (igual aos exemplos do enunciado)
ORDEM_SIMBOLOS = [
    "PAR_ABERTURA", "PAR_FECHAMENTO", "OP_SOMA",
    "OP_SUBTRACAO", "OP_PRODUTO", "OP_DIVISAO", "NUMERO",
]


# --- Análise ---------------------------------------------------------------

def analisar(expressao: str, cientifico: bool = True):
    """Retorna (contagem_validos, lista_invalidos)."""
    regex = montar_regex(cientifico)
    contagem = {s: 0 for s in ORDEM_SIMBOLOS}
    invalidos = []

    for m in regex.finditer(expressao):
        tipo = m.lastgroup
        if tipo == "ESPACO":
            continue
        if tipo == "INVALIDO":
            invalidos.append(m.group())
        else:
            contagem[tipo] += 1

    return contagem, invalidos


def formatar_saida(contagem: dict, invalidos: list) -> str:
    validos = [f"{contagem[s]:02d} {s}" for s in ORDEM_SIMBOLOS if contagem[s] > 0]
    txt_validos = ", ".join(validos) if validos else "não há símbolos válidos"

    if not invalidos:
        txt_invalidos = "não há símbolos inválidos"
    else:
        plural = "símbolo inválido" if len(invalidos) == 1 else "símbolos inválidos"
        txt_invalidos = f"{len(invalidos):02d} {plural} - {' '.join(invalidos)}"

    return f"Símbolos válidos ({txt_validos}) Símbolos inválidos ({txt_invalidos})"


# --- Programa principal ----------------------------------------------------

def main():
    # Uso: python analisador_simbolos.py [--basico] ["expressão"]
    args = sys.argv[1:]
    cientifico = True
    if "--basico" in args:
        cientifico = False
        args.remove("--basico")

    modo = "com notação científica" if cientifico else "somente números d*.d*"
    print(f"Analisador de símbolos ({modo})")

    if args:  # expressão passada na linha de comando
        entradas = [" ".join(args)]
        for e in entradas:
            print(f"Entrada: {e}")
            print("Saída:", formatar_saida(*analisar(e, cientifico)))
        return

    print("Digite uma expressão (ou linha vazia para sair).")
    while True:
        try:
            e = input("\nEntrada: ")
        except EOFError:
            break
        if not e.strip():
            break
        print("Saída:", formatar_saida(*analisar(e, cientifico)))


if __name__ == "__main__":
    main()