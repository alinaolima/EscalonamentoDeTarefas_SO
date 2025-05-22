def sjf(processos):
    prontos = sorted(processos, key=lambda p: p.chegada)
    fila = []
    finalizados = []
    tempo = 0

    while prontos or fila:
        while prontos and prontos[0].chegada <= tempo:
            fila.append(prontos.pop(0))
        
        if fila:
            fila.sort(key=lambda p: p.duracao)
            atual = fila.pop(0)

            atual.inicio = tempo
            atual.fim = tempo + atual.duracao
            atual.tempo_espera = atual.inicio - atual.chegada
            atual.tempo_execucao = atual.fim - atual.chegada
            print(f"Tempo {tempo}: Executando processo {atual.pid}")

            tempo = atual.fim
            finalizados.append(atual)

        else:
            tempo += 1
    
    return finalizados

def rr(processos, quantum):
    prontos = sorted(processos, key=lambda p: p.chegada)
    fila = []
    finalizados = []
    tempo = 0

    while prontos or fila:
        # Adiciona os processos que chegaram até o tempo atual
        while prontos and prontos[0].chegada <= tempo:
            fila.append(prontos.pop(0))

        if fila:
            atual = fila.pop(0)

            if atual.inicio is None:
                atual.inicio = tempo  # Marca o início da primeira execução

            exec_time = min(quantum, atual.tempo_restante)
            print(f"Tempo {tempo}: Executando processo {atual.pid} por {exec_time} unidades")

            tempo += exec_time
            atual.tempo_restante -= exec_time

            # Após executar, adiciona novos processos que chegaram durante a execução
            while prontos and prontos[0].chegada <= tempo:
                fila.append(prontos.pop(0))

            if atual.tempo_restante > 0:
                fila.append(atual)  # Volta para a fila
            else:
                atual.fim = tempo
                atual.tempo_espera = (atual.fim - atual.chegada) - atual.duracao
                finalizados.append(atual)

        else:
            tempo += 1  # Avança o tempo até que algum processo chegue

    return finalizados


def priop(processos):
    prontos = sorted(processos, key=lambda p: p.chegada)  # lista ordenada por chegada
    fila = []
    finalizados = []
    tempo = 0
    atual = None

    while prontos or fila or atual:
        # Adiciona processos que chegaram no tempo atual à fila, ordenada por prioridade
        while prontos and prontos[0].chegada <= tempo:
            p = prontos.pop(0)
            fila.append(p)
            fila.sort(key=lambda x: x.prioridade)  # menor prioridade primeiro (maior prioridade)

        # Verifica se o processo atual precisa ser preemptado
        if atual:
            if fila and fila[0].prioridade < atual.prioridade:
                # Preempção: coloca o atual de volta na fila
                fila.append(atual)
                fila.sort(key=lambda x: x.prioridade)
                atual = fila.pop(0)
                if atual.inicio is None:
                    atual.inicio = tempo
            # Continua executando o processo atual
        else:
            if fila:
                atual = fila.pop(0)
                if atual.inicio is None:
                    atual.inicio = tempo

        if atual:
            # Executa por 1 unidade de tempo
            atual.tempo_restante -= 1
            tempo += 1

            # Se terminou
            if atual.tempo_restante == 0:
                atual.fim = tempo
                atual.tempo_espera = (atual.fim - atual.chegada) - atual.duracao
                finalizados.append(atual)
                atual = None
        else:
            # Nenhum processo para executar, avança o tempo
            tempo += 1

    return finalizados

