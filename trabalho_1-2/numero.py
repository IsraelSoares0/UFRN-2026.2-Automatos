from enum import Enum, auto

class Estado(Enum):
    CENTENA = auto()
    DEZENA = auto()
    FIM = auto()
    
class ConversorExtenso:
    """Classe base: converte números de 0 a 999 em palavras por extenso."""
    
    def __init__(self, unidades, dezenas, centenas, cem_especial=None):
        self.unidades = unidades            
        self.dezenas = dezenas              
        self.centenas = centenas            
        self.cem_especial = cem_especial
        
    def _dezena_unidade(self, resto):
        """Converte um valor de 0 a 99 em uma lista de palavras."""
        raise NotImplementedError
    
    def _ligacao(self):
        """Palavra usada para ligar a centena ao restante (ex: 'e')"""
        raise NotImplementedError
    
    def grupo(self, n):
        """Percorre a maquna de estados CENTENA -> DEZENA -> FIM"""
        if not (0 <= n <= 999):
            raise ValueError("Grupo deve estar entre 0 e 999")
        if n == 0:
            return ""
        if n == 100 and self.cem_especial:
            return self.cem_especial
        
        centena, resto = divmod(n, 100)
        palavras = []
        estado = Estado.CENTENA
        
        # Estado CENTENA: le o digito de centena e emite a palavra
        if estado == Estado.CENTENA:
            if centena > 0:
                palavras.append(self.centenas[centena])
            estado = Estado.DEZENA
        
        # Estado DEZENA: le dezena+unidade e emite as palavras restantes
        if estado == Estado.DEZENA:
            partes_resto = self._dezena_unidade(resto)
            if partes_resto:
                if centena > 0:
                    ligacao = self._ligacao()
                    if ligacao:
                        palavras.append(ligacao)
                palavras.extend(partes_resto)
            estado = Estado.FIM
        
        return " ".join(palavras)
    
# --------------------------------------------------- #
# PORTUGUES
# --------------------------------------------------- #

class ConversorPT(ConversorExtenso):
    def __init__(self):
        super().__init__(
            unidades=["zero", "um", "dois", "três", "quatro", "cinco",
                      "seis", "sete", "oito", "nove", "dez", "onze",
                      "doze", "treze", "quatorze", "quinze", "dezesseis",
                      "dezessete", "dezoito", "dezenove"],
            dezenas=["", "", "vinte", "trinta", "quarenta", "cinquenta",
                     "sessenta", "setenta", "oitenta", "noventa"],
            centenas=["", "cento", "duzentos", "trezentos", "quatrocentos",
                      "quinhentos", "seiscentos", "setecentos", "oitocentos",
                      "novecentos"],
            cem_especial="cem",
        )
    
    def _dezena_unidade(self, resto):
        if resto == 0:
            return []
        if resto < 20:
            return [self.unidades[resto]]
        dezena, unidade = divmod(resto, 10)
        if unidade == 0:
            return [self.dezenas[dezena]]
        return [self.dezenas[dezena], "e", self.unidades[unidade]]
    
    def _ligacao(self):
        return "e"
    
    def numero_completo(self, n):
        if n == 0:
            return "zero"
        
        milhar, resto = divmod(n, 1000)
        parte_milhar = ""
        if milhar > 0:
            parte_milhar = "mil" if milhar == 1 else f"{self.grupo(milhar)} mil"
        
        parte_resto = self.grupo(resto)
        
        if parte_milhar and parte_resto:
            if resto < 100 or resto % 100 == 0:
                return f"{parte_milhar} e {parte_resto}"
            return f"{parte_milhar}, {parte_resto}"
    
        return parte_milhar or parte_resto
    
# --------------------------------------------------- #
# INGLES
# --------------------------------------------------- #

class ConversorEN(ConversorExtenso):
    def __init__(self):
        super().__init__(
            unidades=["zero", "one", "two", "three", "four", "five",
                      "six", "seven", "eight", "nine", "ten", "eleven",
                      "twelve", "thirteen", "fourteen", "fifteen",
                      "sixteen", "seventeen", "eighteen", "nineteen"],
            dezenas=["", "", "twenty", "thirty", "forty", "fifty",
                     "sixty", "seventy", "eighty", "ninety"],
            centenas=["", "one hundred", "two hundred", "three hundred",
                      "four hundred", "five hundred", "six hundred",
                      "seven hundred", "eight hundred", "nine hundred"],
            cem_especial=None,
        )
 
    def _dezena_unidade(self, resto):
        if resto == 0:
            return []
        if resto < 20:
            return [self.unidades[resto]]
        dezena, unidade = divmod(resto, 10)
        if unidade == 0:
            return [self.dezenas[dezena]]
        return [f"{self.dezenas[dezena]}-{self.unidades[unidade]}"]
 
    def _ligacao(self):
        return ""
 
    def numero_completo(self, n):
        if n == 0:
            return "zero"
 
        milhar, resto = divmod(n, 1000)
        parte_milhar = ""
        if milhar > 0:
            parte_milhar = f"{self.grupo(milhar)} thousand"
 
        parte_resto = self.grupo(resto)
 
        if parte_milhar and parte_resto:
            return f"{parte_milhar}, {parte_resto}"
 
        return parte_milhar or parte_resto

# --------------------------------------------------- #
# VALIDACAO ENTRADA
# --------------------------------------------------- #

def validar_entrada(texto):
    """Recebe o texto digitado pelo usuario e devolve o numero inteiro correspondente"""
    texto = texto.strip()
    if not texto:
        return None
    
    sem_pontos = texto.replace(".", "")
    
    try:
        valor = int(sem_pontos)
    except ValueError:
        return None
    
    if valor < 0 or valor > 999_999:
        return None
    
    return valor

# --------------------------------------------------------------------------- #
# MAIN
# --------------------------------------------------------------------------- #
 
MENSAGENS = {
    "pt": {
        "invalido": "entrada inválida (Entrada deve ser um "
                    "número entre 0 e 999.999).",
        "pedir_numero": "Digite um número (0 a 999.999), ou 'sair' para "
                         "encerrar: ",
        "pedir_idioma": "Escolha o idioma [pt/en]: ",
        "saida": "Saída: ",
    },
    "en": {
        "invalido": "invalid input (Integer must be between "
                    "0 and 999,999).",
        "pedir_numero": "Enter a number (0 to 999,999), or 'exit' to quit: ",
        "pedir_idioma": "Choose the language [pt/en]: ",
        "saida": "Output: ",
    },
}
 
CONVERSORES = {
    "pt": ConversorPT(),
    "en": ConversorEN(),
}

def converter(numero, idioma):
    return CONVERSORES[idioma].numero_completo(numero)

def main():
    idioma = ""
    while idioma not in ("pt", "en"):
        idioma = input(MENSAGENS["pt"]["pedir_idioma"]).strip().lower()
 
    msgs = MENSAGENS[idioma]
    palavras_sair = {"sair", "exit", "quit"}
 
    while True:
        entrada = input(msgs["pedir_numero"]).strip()
        if entrada.lower() in palavras_sair:
            break
 
        numero = validar_entrada(entrada)
        if numero is None:
            print(msgs["invalido"])
            continue
 
        print(msgs["saida"] + converter(numero, idioma) + ".")
 
 
if __name__ == "__main__":
    main()
