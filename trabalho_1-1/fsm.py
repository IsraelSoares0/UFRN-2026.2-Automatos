import sys

class MaquinaEstados:
    def __init__(self, ni, no, ns, estado_inicial, TE, VS):
        self.ni = ni    # Quantidade de eventos de entrada
        self.no = no    # Quantidade de eventos de saida
        self.ns = ns    # Quantidade de estados
        self.estado_inicial = estado_inicial
        self.TE = TE    # TE[estado][entrada]   --> proximo estado
        self.VS = VS    # VS[estado]            --> saida do estado
        self.estado_atual = estado_inicial

    def reset(self):
        self.estado_atual = self.estado_inicial
    
    def saida_atual(self):
        return self.VS[self.estado_atual]
    
    def transitar(self, entrada):
        """Recebe uma entrada (0..ni) e atualiza o estado atual"""
        self.estado_atual = self.TE[self.estado_atual][entrada]
        return self.estado_atual, self.saida_atual()

def ler_configuracao(caminho):
    """
    Le um arquivo de configuracao no formato:
        ni=<int>
        no=<int>
        ns=<int>
        estado_inicial=<int>
        
        TE:
        [ns+1, ni+1]; Separados por espaco
        
        VS:
        [ns+1]; Separados por espaco
    
    Linhas em branco e iniciadas com '#' sao ignoradas.
    """
    with open(caminho, "r", encoding="utf-8") as f:
        linhas_brutas = f.readlines()
    
    linhas = []
    for linha in linhas_brutas:
        linha = linha.strip()
        if linha == "" or linha.startswith("#"):
            continue
        linhas.append(linha)
    
    params = {}
    idx = 0
    
    # Leitura de ni, no, ns, estado_inicial
    while idx < len(linhas) and "=" in linhas[idx]:
        chave, valor = linhas[idx].split("=")
        params[chave.strip()] = int(valor.strip())
        idx += 1
    
    for chave in ("ni", "no", "ns", "estado_inicial"):
        if chave not in params:
            raise ValueError(f"Parâmetro obrigatório ausente no arquivo: {chave}")
    
    ni, no, ns = params["ni"], params["no"], params["ns"]
    estado_inicial = params["estado_inicial"]
    
    # TE:
    if idx >= len(linhas) or not linhas[idx].upper().startswith("TE"):
        raise ValueError("Seção 'TE' não encontrada...")
    idx += 1
    
    TE = []
    for _ in range(ns + 1):
        valores = [int(v) for v in linhas[idx].split()]
        if len(valores) != ni + 1:
            raise ValueError(f"Linha de TE deveria ter {ni + 1} valores, tem {len(valores): {linhas[idx]}}")
        TE.append(valores)
        idx += 1
        
    # VS:
    if idx >= len(linhas) or not linhas[idx].upper().startswith("VS"):
        raise ValueError("Seção 'VS' não encontrada...")
    idx += 1
    
    VS = [int(v) for v in linhas[idx].split()]
    if len(VS) != ns + 1:
        raise ValueError(f"VS deveria ter {ns + 1} valores, tem {len(VS)}")
    
    # Validacoes basicas
    if not (0 <= estado_inicial <= ns):
        raise ValueError("estado_inicial fora do intervalo [0, ns].")
    for s, linha_te in enumerate(TE):
        for e, prox in enumerate(linha_te):
            if not (0 <= prox <= ns):
                raise ValueError(f"TE[{s}][{e}]={prox} fora do intervalo de estados [0, ns].")
    
    for s, saida in enumerate(VS):
        if not (0 <= saida <= no):
            raise ValueError(f"VS[{s}]={saida} fora do intervalo de saídas [0, no].")
    
    return MaquinaEstados(ni, no, ns, estado_inicial, TE, VS)

def processar_palavra(maquina, palavra):
    """Aplica uma palavra inteira (ex: '0111010') simbolo a simbolo, a partir
       do estado atual da máquina, e retorna o caminho percorrido como uma
       lista de tuplas (simbolo, estado_resultante, saida_resultante).

    Args:
        maquina (MaquinaEstados): Maquina de Estados do problema.
        palavra (String): String de símbolos usados como entrada.
    """
    for simbolo in palavra:
        if not simbolo.isdigit() or not (0 <= int(simbolo) <= maquina.ni):
            raise ValueError(f"  [ERRO] Simbolo {simbolo} fora do conjunto de entradas [0..{maquina.ni}]")
    
    caminho = []
    
    for simbolo in palavra:
        estado, saida = maquina.transitar(int(simbolo))
        caminho.append((simbolo, estado, saida))
    return caminho

def imprimir_status(maquina, ciclo):
    print(f"t{ciclo}: estado = s{maquina.estado_atual}  |  saida = {maquina.saida_atual()}")
    
def loop_iterativo(maquina):
    print("=" * 60)
    print("Maquina de Estados Finitos carregada...")
    print(f"  I (entradas)   = {{0, ..., {maquina.ni}}}")
    print(f"  O (saidas)     = {{0, ..., {maquina.no}}}")
    print(f"  Estado inicial = s{maquina.estado_inicial}")
    print("=" * 60)
    print("Digite um valor de entrada (0.."+str(maquina.ni)+"), uma palavra inteira (ex: 0111010), ")
    print("'r' para reset ou 'sair' para encerrar.")
    print()
    
    ciclo = 0
    entrada_antes = "--"
    imprimir_status(maquina, ciclo)
    
    while True:
        entrada = input(f"t{ciclo} - entrada> ").strip().lower()
        
        if entrada == "sair":
            print("Encerrando simulação...")
            break
        
        if entrada == "r":
            maquina.reset()
            ciclo = 0
            print("  [RESET] Voltando ao estado inicial.")
            imprimir_status(maquina, ciclo)
            continue
        
        if entrada == "" or not entrada.isdigit():
            print(f"  [ERRO] Entrada Invalida -- Use um numero entre 0 e {maquina.ni}, ou 'r' para reset...")
            continue
        
        estado_antes = maquina.estado_atual
        saida_antes = maquina.saida_atual()
        
        try:
            caminho = processar_palavra(maquina, entrada)
        except ValueError as e:
            print(f"  [ERRO] Entrada inválida: {e}")
            continue
    
        if len(entrada) > 1:
            print(f"  Processando a palavra '{entrada}':")
            print(f"  {'Ciclo':<8}{'Entrada':<10}{'Estado':<10}{'Saida':<8}")
            if entrada_antes == "--":
                print(f"  {('t' + str(ciclo)):<8}{'--':<10}{('s' + str(estado_antes)):<10}{saida_antes:<8}")
            else:
                print(f"  {('t' + str(ciclo)):<8}{entrada_antes:<10}{('s' + str(estado_antes)):<10}{saida_antes:<8}")
            for simbolo, estado, saida in caminho:
                ciclo += 1
                print(f"  {('t' + str(ciclo)):<8}{simbolo:<10}{('s' + str(estado)):<10}{saida:<8}")
                entrada_antes = simbolo
            print(f"  --> Estado final: s{maquina.estado_atual}  |  Saida final: {maquina.saida_atual()}")
        else:
            ciclo += 1
            imprimir_status(maquina, ciclo)

def main():
    if len(sys.argv) != 2:
        print("  [ERRO] Uso: python fsm.py <configuracao.txt>")
        sys.exit(1)
    
    caminho = sys.argv[1]
    try:
        maquina = ler_configuracao(caminho)
    except (ValueError, FileNotFoundError, IndexError) as e:
        print(f"  [ERRO] Falha ao carregar configuração: {e}")
        sys.exit(1)
    
    loop_iterativo(maquina)

if __name__ == "__main__":
    main()        