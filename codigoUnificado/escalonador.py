# Trabalho sobre Escalonamento de Processos
# Aluna: Aline da Conceição Ferreira Lima - 22250366
# Linguagem utilizada: Python
# Para a interação, siga os passos a seguir:
# 1.Informe o caminho do arquivo txt que contém as informações sobre os processos
# 2.Escolha o tipo de processo que deseja testar (CPU-Bound(1), CPU-IO(2), Ambos(3));
# 3.Escolha qual dos algoritmos disponíveis p/ o processo deseja utilizar;
# 4.Caso o algoritmo necessite, informe o quantum desejado;
# 5.Por fim, veja o resultado da execução. 
# 6.Para visualizar o resultado do código em um arquivo txt abra a pasta onde o código está e o arquivo estará lá

import sys
import os
from contextlib import redirect_stdout

#definindo a estrutura de um processo na simulação através de uma classe
class Processo:
    def __init__(self, pid, chegada, duracao, prioridade, tipo):
        self.pid = pid                      #Identificador do processo                     
        self.chegada = chegada              #Tempo de chegada do processo
        self.duracao = duracao              #Duracao total do processo
        self.prioridade = prioridade        #Nível de prioridade do processo
        self.tipo = tipo                    #Tipo de processo (CPU-bound, I/O-bound ou Ambos)

        self.tempo_restante = duracao       #Tempo restante de execução 
        self.inicio = None                  #Tempo em que o processo começou a execução
        self.fim = None                     #Tempo em que o processo finalizou
        self.tempo_espera = 0               #Tempo total que o processo ficou esperando
        self.tempo_execucao = 0             #Tempo total desde a chegada até o fim da execução 

    def __repr__(self):
        return f"(PID={self.pid}, chegada={self.chegada}, duracao={self.duracao}, prioridade={self.prioridade}, tipo={self.tipo})"

def carregar_processos_txt(caminho_arquivo):
    processos = []
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()[1:]  # pula cabeçalho
        for linha in linhas:
            partes = linha.strip().split()
            pid = int(partes[0][1:])
            chegada = int(partes[1])
            duracao = int(partes[2])
            prioridade = int(partes[3])
            tipo = int(partes[4])
            processos.append(Processo(pid, chegada, duracao, prioridade, tipo))
    return processos

# FCFS para CPU-bound (tipo 1) - sem preempção
def fcfs(processos):
    processos = sorted(processos, key=lambda p: p.chegada) # ordena por tempo de chegada
    tempo = 0
    finalizados = []

    for p in processos:
        if tempo < p.chegada:
            tempo = p.chegada # espera o processo chegar
        p.inicio = tempo
        p.fim = tempo + p.duracao
        p.tempo_espera = p.inicio - p.chegada
        p.tempo_execucao = p.fim - p.chegada
        tempo = p.fim # avança o tempo global
        finalizados.append(p)
        print(f"Tempo {p.inicio}: Executando processo {p.pid} por {p.duracao} unidades")

    return finalizados

# SJF para CPU-bound (tipo 1)
def sjf(processos):
    prontos = sorted(processos, key=lambda p: p.chegada) # ordena por tempo de chegada
    fila = []
    finalizados = []
    tempo = 0

    while prontos or fila:
        # Adiciona à fila os processos que já chegaram até o tempo atual
        while prontos and prontos[0].chegada <= tempo:
            fila.append(prontos.pop(0))

        if fila:
            fila.sort(key=lambda p: p.duracao) # ordena por menor duração
            atual = fila.pop(0)
            atual.inicio = tempo
            atual.fim = tempo + atual.duracao
            atual.tempo_espera = atual.inicio - atual.chegada
            atual.tempo_execucao = atual.fim - atual.chegada
            print(f"Tempo {tempo}: Executando processo {atual.pid}")
            tempo = atual.fim
            finalizados.append(atual)
        else:
            tempo += 1 # se não houver processos prontos, avança tempo

    return finalizados

# RR para CPU-IO (tipo 2) - com quantum (preemptivo)
def rr(processos, quantum):
    prontos = sorted(processos, key=lambda p: p.chegada) # ordena por tempo de chegada
    fila = []
    finalizados = []
    tempo = 0

    while prontos or fila:
        # Move para a fila os processos que chegaram até o tempo atual
        while prontos and prontos[0].chegada <= tempo:
            fila.append(prontos.pop(0))

        if fila:
            atual = fila.pop(0) # pega o primeiro da fila (RR)
            if atual.inicio is None:
                atual.inicio = tempo # marca o tempo de inicio na primeira execução

            exec_time = min(quantum, atual.tempo_restante) # define quanto tempo vai executar agora
            print(f"Tempo {tempo}: Executando processo {atual.pid} por {exec_time} unidades")
            tempo += exec_time
            atual.tempo_restante -= exec_time

            # verifica se novos processos chegaram durante a execução
            while prontos and prontos[0].chegada <= tempo:
                fila.append(prontos.pop(0))

            if atual.tempo_restante > 0:
                fila.append(atual) # volta para a fila se ainda não terminou
            else:
                atual.fim = tempo
                atual.tempo_espera = (atual.fim - atual.chegada) - atual.duracao
                atual.tempo_execucao = atual.fim - atual.chegada
                finalizados.append(atual)
        else:
            tempo += 1

    return finalizados

# Priop para Ambos (tipo 3) - preemptivo com quantum
def priop(processos, quantum):
    prontos = sorted(processos, key=lambda p: p.chegada) # ordena por chegada
    fila = []
    finalizados = []
    tempo = 0

    while prontos or fila:
        # Adiciona à fila os processos que já chegaram
        while prontos and prontos[0].chegada <= tempo:
            fila.append(prontos.pop(0))

        if fila:
            fila.sort(key=lambda p: p.prioridade) # menor valor = maior prioridade
            atual = fila.pop(0)  # seleciona o de maior prioridade
            if atual.inicio is None:
                atual.inicio = tempo

            exec_time = min(quantum, atual.tempo_restante) # executa até quantum ou terminar
            print(f"Tempo {tempo}: Executando processo {atual.pid} (prioridade {atual.prioridade}) por {exec_time} unidades")
            tempo += exec_time
            atual.tempo_restante -= exec_time # atualiza tempo restante

            # Verifica se novos processos chegaram
            while prontos and prontos[0].chegada <= tempo:
                fila.append(prontos.pop(0))

            if atual.tempo_restante > 0:
                fila.append(atual) # volta para a fila se não terminou
            else:
                atual.fim = tempo
                atual.tempo_espera = (atual.fim - atual.chegada) - atual.duracao
                atual.tempo_execucao = atual.fim - atual.chegada
                finalizados.append(atual)
        else:
            tempo += 1 # avança tempo se nenhum processo pronto

    return finalizados

# SRTF para CPU I/O (tipo 2) - com quantum (preemptivo)
def srtf(processos, quantum):
    prontos = sorted(processos, key=lambda p: p.chegada) # ordena por chegada
    fila = []
    finalizados = []
    tempo = 0

    while prontos or fila:
        # Adiciona processos que chegaram até agora
        while prontos and prontos[0].chegada <= tempo:
            fila.append(prontos.pop(0))

        if fila:
            fila.sort(key=lambda p: p.tempo_restante) # menor tempo restante primeiro
            atual = fila.pop(0)
            if atual.inicio is None:
                atual.inicio = tempo

            exec_time = min(quantum, atual.tempo_restante) # executa até quantum ou fim
            print(f"Tempo {tempo}: Executando processo {atual.pid} por {exec_time} unidades (SRTF)")
            tempo += exec_time
            atual.tempo_restante -= exec_time # atualiza tempo restante

            # Verifica chegada de novos processos
            while prontos and prontos[0].chegada <= tempo:
                fila.append(prontos.pop(0)) 

            if atual.tempo_restante > 0:
                fila.append(atual) # volta para fila
            else:
                atual.fim = tempo
                atual.tempo_espera = (atual.fim - atual.chegada) - atual.duracao
                atual.tempo_execucao = atual.fim - atual.chegada
                finalizados.append(atual)
        else:
            tempo += 1 # se nenhum processo pronto, avança tempo
    return finalizados

# PrioC para Ambos (tipo 3) - prioridade cooperativo, não preemptivo
def prioc(processos):
    processos = sorted(processos, key=lambda p: (p.chegada, p.prioridade)) # ordena por chegada e prioridade
    tempo = 0
    finalizados = []
    fila = []

    while processos or fila:
        # Move para fila os que já chegaram
        while processos and processos[0].chegada <= tempo:
            fila.append(processos.pop(0))

        if fila:
            fila.sort(key=lambda p: p.prioridade) # menor valor = maior prioridade
            atual = fila.pop(0)
            if tempo < atual.chegada:
                tempo = atual.chegada # espera o processo chegar
            atual.inicio = tempo
            atual.fim = tempo + atual.duracao
            tempo = atual.fim
            atual.tempo_espera = atual.inicio - atual.chegada
            atual.tempo_execucao = atual.fim - atual.chegada
            print(f"Tempo {atual.inicio}: Executando processo {atual.pid} (prio coop) por {atual.duracao} unidades")
            finalizados.append(atual)
        else:
            tempo += 1 # se nenhum processo chegou, avança tempo

    return finalizados

# Calcula e exibe o tempo médio de espera e tempo médio de execução dos processos finalizados
def calcular_tempos_medios(processos):
    total_espera = sum(p.tempo_espera for p in processos)
    total_execucao = sum(p.tempo_execucao for p in processos)
    n = len(processos)
    media_espera = total_espera / n if n else 0
    media_execucao = total_execucao / n if n else 0
    print(f"\nTempo médio de espera: {media_espera:.2f}")
    print(f"Tempo médio de execução: {media_execucao:.2f}")

# Menu principal para escolha do tipo de processo
def menu_tipo():
    print("\nEscolha o tipo do processo:")
    print("1 - CPU-bound")
    print("2 - CPU I/O-bound")
    print("3 - CPU Ambos")
    print("0 - Sair")
    return input("Digite a opção: ")

# Menu para a escolha de algoritmos baseado no tipo de processo
def menu_algoritmo(tipo):
    if tipo == "1":
        print("\nEscolha o algoritmo para CPU-bound:")
        print("1 - FCFS")
        print("2 - SJF")
        return input("Digite a opção: ")
    elif tipo == "2":
        print("\nEscolha o algoritmo para CPU I/O-bound:")
        print("1 - RR")
        print("2 - SRTF")
        return input("Digite a opção: ")
    elif tipo == "3":
        print("\nEscolha o algoritmo para CPU Ambos:")
        print("1 - PrioC (cooperativo)")
        print("2 - Priop (preemptivo com quantum)")
        return input("Digite a opção: ")
    else:
        return None

class DuplicadorDeSaida:
    def __init__(self, arquivo):
        self.terminal = sys.__stdout__
        self.arquivo = arquivo

    def write(self, mensagem):
        self.terminal.write(mensagem)
        self.arquivo.write(mensagem)

    def flush(self):
        self.terminal.flush()
        self.arquivo.flush()

if __name__ == "__main__":
    # Nome do arquivo de log
    nome_arquivo_log = "saida_simulacao.txt"
    
    with open(nome_arquivo_log, "w", encoding="utf-8") as log_file:
        sys.stdout = DuplicadorDeSaida(log_file)

        # Solicita o caminho do arquivo de entrada (em formato txt)
        caminho = input("Digite o caminho do arquivo de entrada (.txt): ")
        processos_originais = carregar_processos_txt(caminho)

        while True:
            # Exibe menu para escolher o tipo de processo
            tipo = menu_tipo()
            if tipo == "0":
                print("Encerrando o programa.")
                break
            if tipo not in ["1", "2", "3"]:
                print("Tipo inválido. Tente novamente.")
                continue
            
            algoritmo = menu_algoritmo(tipo)
            if algoritmo not in ["1", "2"]:
                print("Algoritmo inválido. Tente novamente.")
                continue

            processos = [p for p in processos_originais if str(p.tipo) == tipo]

            quantum = None
            if (tipo == "2" and algoritmo in ["1", "2"]) or (tipo == "3" and algoritmo == "2"):
                quantum = int(input("Digite o quantum: "))

            if tipo == "1":
                if algoritmo == "1":
                    print("\nExecutando FCFS...")
                    finalizados = fcfs(processos)
                elif algoritmo == "2":
                    print("\nExecutando SJF...")
                    finalizados = sjf(processos)

            elif tipo == "2":
                if algoritmo == "1":
                    print("\nExecutando RR...")
                    finalizados = rr(processos, quantum)
                elif algoritmo == "2":
                    print("\nExecutando SRTF...")
                    finalizados = srtf(processos, quantum)

            elif tipo == "3":
                if algoritmo == "1":
                    print("\nExecutando PrioC (Cooperativo)...")
                    finalizados = prioc(processos)
                elif algoritmo == "2":
                    print("\nExecutando Priop (Preemptivo com quantum)...")
                    finalizados = priop(processos, quantum)

            else:
                print("Opção inválida.")
                continue

            calcular_tempos_medios(finalizados)

            continuar = input("\nDeseja realizar outra simulação? (s/n): ").lower()
            if continuar != 's':
                print("Programa encerrado.")
                break


