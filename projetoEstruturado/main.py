from algoritmos import sjf, rr, priop
from leitor import carregar_processos_txt
from simulador import simular

def escolher_e_executar(processos, quantum=None):
    # Filtra processos por tipo
    cpu_bound = [p for p in processos if p.tipo == 1]
    io_bound = [p for p in processos if p.tipo == 2]
    ambos = [p for p in processos if p.tipo == 3]

    print("Escolha o tipo de processo para simular:")
    print("1 - CPU-bound (SJF)")
    print("2 - I/O-bound (RR)")
    print("3 - Ambos (Priop ou FCFS)")
    escolha = input("Digite 1, 2 ou 3: ")

    if escolha == '1':
        print("Executando SJF para CPU-bound")
        resultado = sjf(cpu_bound)
    elif escolha == '2':
        if quantum is None:
            quantum = int(input("Digite o quantum para RR: "))
        print("Executando RR para I/O-bound")
        resultado = rr(io_bound, quantum)
    elif escolha == '3':
        print("Executando Priop para ambos")
        resultado = priop(ambos)
    else:
        print("Opção inválida")
        return None

    return resultado


if __name__ == "__main__":
    processos = carregar_processos_txt("exemplos/FCFS_SJF_6.txt")
    quantum = 1  # valor padrão, pode ser alterado no menu para RR

    # Chama o menu para escolher o algoritmo e executar
    resultado = escolher_e_executar(processos, quantum)

    if resultado is not None:
        for r in resultado:
            print(r)

        total_espera = sum(p.tempo_espera for p in resultado)
        total_execucao = sum((p.fim - p.chegada) for p in resultado if p.fim is not None)
        n = len(resultado)

        media_espera = total_espera / n if n else 0
        media_execucao = total_execucao / n if n else 0

        print(f"Tempo médio de espera: {media_espera:.2f}")
        print(f"Tempo médio de execução: {media_execucao:.2f}")



