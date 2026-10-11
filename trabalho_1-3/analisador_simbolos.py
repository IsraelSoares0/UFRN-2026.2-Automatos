import re
import sys

# --- PADROES ----------------------------

# Números básicos (d*.d*)
NUM_BASICO = r"(?:\d+\.?\d*|\.\d+)"

# Notação Científica
NUM_CIENTIFICO = NUM_BASICO + r"(?:[eE][+-]?\d+)?"


def montar_regex(cientifico: bool = True) -> re.Pattern:
    num = NUM_CIENTIFICO if cientifico else NUM_BASICO
    padrao = "|".join([
        rf"(?P<NUMERO>{num})",
        r"(?P<PAR_ABERTURA>\()",
        r"(?P<PAR_FECHAMENTO>\))"
        r"(?P<OP_SOMA>\+)",
        r"(?P<OP_SUBTRACAO>-)",
        r"(?P<OP_PRODUTO>\*)",
        r"(?P<OP_DIVISAO>/)",
        r"(?P<ESPACO>\s+)",
        r"(?P<INVALIDO>.)",
    ])
    
    return re.compile(padrao)

# Ordem de exibição de símbolos
ORDEM_SIMBOLOS = [
    "PAR_ABERTURA", "PAR_FECHAMENTO", "OP_SOMA",
    "OP_SUBTRACAO", "OP_PRODUTO", "OP_DIVISAO", "NUMERO",
]


# --- ANALISE ----------------------------

def analisar(expressao: str, cientifico: bool = True):
    """Retorna (contagem_validos, lista_invalidos)"""
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

def formatar_saida(contagem: dict, invalidos: str) -> str:
    validos = [f"{contagem[s]:02d} {s}" for s in ORDEM_SIMBOLOS if contagem[s] > 0]
    txt_validos = ", ".join(validos) if validos else "não existem símbolos válidos"
    
    if not invalidos:
        txt_invalidos = "não existem símbolos inválidos"
    else:
        plural = "símbolo inválido" if len(invalidos) == 1 else "símbolos inválidos"
        txt_invalidos = f"{len(invalidos):02d} {plural} - {' '.join(invalidos)}"
    
    return f"Símbolos válidos ({txt_validos}) Símbolos inválidos ({txt_invalidos})"


# --- MAIN ----------------------------

def main():
    # Uso: python analisador_simbolos.py [--basico] ["expressão"]
    args = sys.argv[1:]
    cientifico = True
    if "--basico" in args:
        cientifico = False
        args.remove("--basico")
        
    modo = "com notacao cientifica" if cientifico else "somente numero d*.d*"
    print(f"Analisador de símbolos ({modo})")
    
    if args:
        entradas = [" ".join(args)]
        for e in entradas:
            print(f"Entrada: {e}")
            print("Saida:", formatar_saida(*analisar(e, cientifico)))
        return
    
    print("Digite uma expressao (ou linha vazia para sair)")
    while(True):
        try:
            e = input("\nEntrada: ")
        except EOFError:
            break
        if not e.strip():
            break
        print("Saida:", formatar_saida(*analisar(e, cientifico)))


if __name__ == "__main__":
    main()