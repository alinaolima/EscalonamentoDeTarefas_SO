from processos import Processo

def carregar_processos_txt(caminho_arquivo):
    processos = []

    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()[1:]
        for linha in linhas:
            partes = linha.strip().split()
            pid = int(partes[0][1:  ])
            chegada = int(partes[1])
            duracao = int(partes[2])
            prioridade = int(partes[3])
            tipo = int(partes[4])
            p = Processo(pid, chegada, duracao, prioridade, tipo)
            processos.append(p)

    return processos