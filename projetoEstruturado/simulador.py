from algoritmos import sjf, rr, priop

def simular(processos, quantum):
    cpu_bound = [p for p in processos if p.tipo == 1]
    io_bound = [p for p in processos if p.tipo == 2]
    ambos = [p for p in processos if p.tipo == 3]

    resultado_cpu = sjf(cpu_bound)
    resultado_io = rr(io_bound, quantum)
    resultado_ambos = priop(ambos, quantum)

    todos_resultados = resultado_cpu + resultado_io + resultado_ambos
    todos_resultados.sort(key=lambda p: p.inicio or 0)

    print("Ordem de execução dos processos:")
    for p in todos_resultados:
        print(f"PID={p.pid}, Início={p.inicio}, Fim={p.fim}, Tempo de Espera={p.tempo_espera}, Tempo de Execução={p.tempo_execucao}")
        
    return todos_resultados
